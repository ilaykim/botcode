from urllib.parse import urlencode
import requests
import time
import hashlib
import hmac
import argparse
import ccxt
import json
import sqlite3
import sys
from datetime import datetime, timedelta
from prettytable import PrettyTable

# Define error codes
ERROR_CODES = {
    'generic': 1,
    'api_keys_error': 10,
    'api_connection_failure': 20,
    'db_error': 30,
    'arg_parse_error': 40,
}

# Initialize paths
passivbot_folder = '/home/stablesail/passivbot'
botcode_folder = '/home/stablesail/botcode'
api_keys_file = f'{passivbot_folder}/api-keys.json'
maindb_file = f'{botcode_folder}/website_data.db'
accounts_coins_file_template = f'{botcode_folder}/{{username}}_account_coins.json'

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Manage cryptocurrency account data.')
parser.add_argument('--account', type=str, help='Specific account to process. Processes all if not specified.')
args = parser.parse_args()

def load_api_keys():
    try:
        with open(api_keys_file, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f'Failed to load API keys: {e}')
        sys.exit(ERROR_CODES['api_keys_error'])

def init_db():
    try:
        conn = sqlite3.connect(maindb_file)
        conn.execute('''CREATE TABLE IF NOT EXISTS account_data (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            account_name TEXT UNIQUE,
                            total_balance REAL,
                            unrealized_pnl REAL,
                            _30day_gain REAL
                        )''')
        return conn
    except Exception as e:
        print(f'Failed to initialize database: {e}')
        sys.exit(ERROR_CODES['db_error'])

def fetch_exchange_data(api_keys, selected_account=None):
    exchanges = []
    for account_name, api in api_keys.items():
        if selected_account and account_name != selected_account:
            continue
        if api['exchange'] in ['binance', 'bybit']:
            try:
                exchange_class = getattr(ccxt, api['exchange'])
                exchanges.append((account_name, exchange_class({
                    'apiKey': api['key'],
                    'secret': api['secret']
                })))
            except Exception as e:
                print(f'Failed to connect to {api["exchange"]} for account {account_name}: {e}')
                sys.exit(ERROR_CODES['api_connection_failure'])
    return exchanges

def update_account_data_in_db(db_conn, account_name, total_balance, unrealized_pnl, _30day_gain):
    try:
        cursor = db_conn.cursor()
        cursor.execute('''INSERT INTO account_data (account_name, total_balance, unrealized_pnl, _30day_gain) 
                          VALUES (?, ?, ?, ?)
                          ON CONFLICT(account_name) 
                          DO UPDATE SET total_balance=excluded.total_balance, unrealized_pnl=excluded.unrealized_pnl, _30day_gain=excluded._30day_gain''',
                       (account_name, total_balance, unrealized_pnl, _30day_gain))
        db_conn.commit()
    except sqlite3.Error as e:
        print(f'Failed to update database for {account_name}: {e}')
        sys.exit(ERROR_CODES['db_error'])

def write_account_coins_file(account_name, positions):
    filepath = accounts_coins_file_template.format(username=account_name)
    try:
        with open(filepath, 'w') as file:
            json.dump(positions, file, indent=4)
    except Exception as e:
        print(f'Failed to write account coins file for {account_name}: {e}')
        sys.exit(ERROR_CODES['generic'])

def get_closed_pnl_bybit(api_key, api_secret, start_time, end_time):
    base_url = "https://api.bybit.com"
    endpoint = "/v5/position/closed-pnl"
    params = {
        "api_key": api_key,
        "category": "linear",
        "start_time": start_time,
        "end_time": end_time,
        "timestamp": int(time.time() * 1000)
    }

    # Create the signature
    query_string = "&".join([f"{key}={value}" for key, value in sorted(params.items())])
    signature = hmac.new(api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    params["sign"] = signature

    # Make the request
    response = requests.get(base_url + endpoint, params=params)
    return response.json()

def bybit_pnl(api_key, api_secret, username, period_days, filename="user_traded_symbols.json"):
    end_time = int(time.time() * 1000)
    start_time = end_time - (period_days * 24 * 60 * 60 * 1000)
    pnl_by_coin = {}
    total_pnl = 0

    # Read the existing data from the JSON file
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    # Get previously traded symbols for the user, if available
    previous_traded_symbols = data.get(username, {}).get("traded_symbols", [])
    traded_symbols = set(previous_traded_symbols)  # Use a set to avoid duplicates


    while start_time < end_time:
        batch_end_time = min(start_time + (7 * 24 * 60 * 60 * 1000), end_time)
        result = get_closed_pnl_bybit(api_key, api_secret, start_time, batch_end_time)

        if result['retCode'] == 0:
            for record in result['result']['list']:
                symbol = record['symbol']
                pnl = float(record['closedPnl'])
                pnl_by_coin[symbol] = pnl_by_coin.get(symbol, 0) + pnl
                total_pnl += pnl
                traded_symbols.add(symbol)  # Add symbol to the set of traded symbols
        else:
            print(f"Error: {result['retMsg']}")

        start_time = batch_end_time

    # Update the JSON file with the combined traded symbols
    data[username] = {
        "last_check_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "traded_symbols": list(traded_symbols)
    }
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    return {"total_pnl": total_pnl, "pnl_by_coin": pnl_by_coin}
       
def binance_signature(query_string, api_secret):
    return hmac.new(api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()

def get_binance_futures_trade_history(api_key, api_secret, symbol, start_time, end_time):
    base_url = "https://fapi.binance.com"
    endpoint = "/fapi/v1/userTrades"
    params = {
        "symbol": symbol,
        "startTime": start_time,
        "endTime": end_time,
        "timestamp": int(time.time() * 1000)
    }
    query_string = urlencode(params)
    signature = binance_signature(query_string, api_secret)
    params["signature"] = signature
    headers = {
        "X-MBX-APIKEY": api_key
    }
    response = requests.get(base_url + endpoint, params=params, headers=headers)
    data = response.json()
    if 'code' in data:
        print(f"Error fetching trades for {symbol}: {data['msg']}")
    return data

def get_traded_symbols_binance(api_key, api_secret, duration_days):
    end_time = int(time.time() * 1000)
    start_time = end_time - (duration_days * 24 * 60 * 60 * 1000)

    response = requests.get("https://fapi.binance.com/fapi/v1/exchangeInfo")
    symbols = [symbol['symbol'] for symbol in response.json()['symbols']]

    traded_symbols = set()
    for symbol in symbols:
        temp_start_time = start_time
        while temp_start_time < end_time:
            batch_end_time = min(temp_start_time + (7 * 24 * 60 * 60 * 1000), end_time)
            trades = get_binance_futures_trade_history(api_key, api_secret, symbol, temp_start_time, batch_end_time)
            if isinstance(trades, list) and len(trades) > 0:
                traded_symbols.add(symbol)
                break  # No need to check further if we already found trades for this symbol
            temp_start_time = batch_end_time

    return list(traded_symbols)

def binance_futures_pnl(api_key, api_secret, symbol, period_days):
    end_time = int(time.time() * 1000)
    start_time = end_time - (period_days * 24 * 60 * 60 * 1000)
    total_pnl = 0

    while start_time < end_time:
        batch_end_time = min(start_time + (24 * 60 * 60 * 1000), end_time)
        trades = get_binance_futures_trade_history(api_key, api_secret, symbol, start_time, batch_end_time)

        if isinstance(trades, list):
            for trade in trades:
                pnl = float(trade['realizedPnl'])
                total_pnl += pnl
        else:
            print(f"Error: {trades}")

        start_time = batch_end_time

    return total_pnl

def update_traded_symbols_binance(api_key, api_secret, username, filename="user_traded_symbols.json"):
    # Read the existing data from the JSON file
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    # Get the last check date and previously traded symbols for the user, if available
    user_data = data.get(username, {})
    last_check_date = user_data.get("last_check_date", None)
    previous_traded_symbols = user_data.get("traded_symbols", [])

    if last_check_date:
        last_check_datetime = datetime.strptime(last_check_date, "%Y-%m-%d %H:%M:%S")
        duration_days = (datetime.now() - last_check_datetime).days
    else:
        duration_days = 30  # Default to 30 days if no previous check date

    # Get traded symbols since the last check date
    traded_symbols = get_traded_symbols_binance(api_key, api_secret, duration_days)

    # Combine with previously traded symbols and remove duplicates
    combined_traded_symbols = list(set(traded_symbols + previous_traded_symbols))

    # Update the JSON file with the current datetime and combined traded symbols
    data[username] = {
        "last_check_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "traded_symbols": combined_traded_symbols
    }
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    return combined_traded_symbols

def calculate_pnl_binance(api_key, api_secret, traded_symbols, duration_days):
    pnl_by_coin = {}
    total_pnl = 0

    for symbol in traded_symbols:
        pnl = binance_futures_pnl(api_key, api_secret, symbol, duration_days)
        pnl_by_coin[symbol] = pnl
        total_pnl += pnl

    return pnl_by_coin, total_pnl

def fetch_and_update_account_data(exchange, account_name, db_conn):
    try:
        if exchange.id == 'bybit':
            balance = exchange.fetch_balance()
            total_balance = balance['total'].get('USDT', 0)
            pnl_result = bybit_pnl(api_key=exchange.apiKey, api_secret=exchange.secret, username=account_name, period_days=30)
            
        elif exchange.id == 'binance':
            balance = exchange.fetch_balance({'type': 'future'})
            total_balance = balance['info']['totalWalletBalance']
            traded_symbols = update_traded_symbols_binance(api_key=exchange.apiKey, api_secret=exchange.secret, username=account_name)
            pnl_result, pnl_result['total_pnl'] = calculate_pnl_binance(api_key=exchange.apiKey, api_secret=exchange.secret, traded_symbols=traded_symbols, duration_days=30)

        positions = exchange.fetch_positions()
        active_positions = [position for position in positions if position['contracts'] > 0]
 
        _30day_gain =  pnl_result['total_pnl']

        # Update the account data in the database
        update_account_data_in_db(db_conn, account_name, total_balance, sum(pos['unrealizedPnl'] for pos in active_positions), _30day_gain)

        # Prepare and write account-specific positions data
        accounts_coins_data = [{
            "symbol": pos['symbol'],
            "side": pos['side'],
            "num_of_contracts": pos['contracts'],
            "entry_price": pos['entryPrice'],
            "upnl": pos['unrealizedPnl'],
            "leverage": pos['leverage'],
            "daily_realized_pnl": sum(trade['profit'] for trade in exchange.fetch_my_trades(pos['symbol']) if 'profit' in trade)
        } for pos in active_positions]

        write_account_coins_file(account_name, accounts_coins_data)

        print(f"Updated {account_name}: Total Balance: {total_balance}, Active Positions: {len(active_positions)}")

    except Exception as e:
        print(f"Error updating account {account_name}: {e}")
        sys.exit(ERROR_CODES['generic'])

def main():
    api_keys = load_api_keys()
    db_conn = init_db()
    exchanges = fetch_exchange_data(api_keys, args.account)
    
    for account_name, exchange in exchanges:
        fetch_and_update_account_data(exchange, account_name, db_conn)
    
    db_conn.close()
    print(f'Operation completed. Accounts updated: {len(exchanges)}.')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        sys.exit(ERROR_CODES['generic'])


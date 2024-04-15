
# Update Account Data Script

This script manages account data for trading bots on Binance and Bybit exchanges. It fetches account balances, open positions, and calculates profit and loss (PnL) for the past 30 days.

## Files Used and Written

- **API Keys File**: `api-keys.json`
  - Contains API keys for connecting to the exchanges. Example:
    ```json
    {
      "binance_account": {
        "exchange": "binance",
        "key": "your_binance_api_key",
        "secret": "your_binance_api_secret"
      },
      "bybit_account": {
        "exchange": "bybit",
        "key": "your_bybit_api_key",
        "secret": "your_bybit_api_secret"
      }
    }
    ```

- **SQLite Database**: `website_data.db`
  - Stores account data, including total balance, unrealized PnL, and 30-day gain. Example schema:
    ```sql
    CREATE TABLE IF NOT EXISTS account_data (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      account_name TEXT UNIQUE,
      total_balance REAL,
      unrealized_pnl REAL,
      _30day_gain REAL
    )
    ```

- **Account Coins Files**: `<username>_account_coins.json`
  - Contains detailed position information for each account. Example:
    ```json
    {
      "symbol": "BTCUSDT",
      "side": "buy",
      "num_of_contracts": 10,
      "entry_price": 50000,
      "upnl": 1000,
      "leverage": 10,
      "daily_realized_pnl": 50
    }
    ```

## Overview

The script consists of several key parts:

1. **Initialization**: It loads API keys from `api-keys.json` and initializes the SQLite database `website_data.db`.

2. **Fetch Exchange Data**: It fetches account data from the exchanges using the CCXT library. For Bybit, it fetches closed PnL records, and for Binance, it fetches trade history for the past 30 days.

3. **Update Account Data**: It updates the SQLite database with the latest account balances, unrealized PnL, and 30-day gain for each account.

4. **Write Account Coins File**: It writes a JSON file `<username>_account_coins.json` containing detailed position information for each account.

## Usage

To update all accounts:

```sh
python update_account_data.py
```

To update a specific account:

```sh
python update_account_data.py --account <account_name>
```

## Cronjob Setup

To run the script as a cronjob every hour, add the following entry to your crontab:

```sh
0 * * * * /path/to/python /path/to/update_account_data.py
```

This will run the script at the beginning of every hour.

---


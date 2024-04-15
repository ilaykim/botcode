import ccxt
import argparse
import sys

def verify_api(api_key, api_secret, exchange_name):
    try:
        # Create the exchange object
        exchange_class = getattr(ccxt, exchange_name.lower())
        exchange = exchange_class({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True,  # Required for Binance
        })

        # Fetch the account balance
        if exchange_name.lower() == 'binance':
            balance = exchange.fetch_balance(params={'type': 'future'})
        elif exchange_name.lower() == 'bybit':
            balance = exchange.fetch_balance(params={'type': 'CONTRACT'})
        else:
            print('Invalid exchange name')
            sys.exit(400)

        if balance:
            print('API key is valid and account is open for trading')
            sys.exit(200)
        else:
            print('API key is valid but account is not open for trading')
            sys.exit(401)

    except ccxt.AuthenticationError:
        print('Invalid API key or secret')
        sys.exit(403)
    except ccxt.ExchangeError as e:
        print(f'Error: {e}')
        sys.exit(500)
    except AttributeError as e:
        print(f'Error: {e}. Did you mean: "bybit"?')
        sys.exit(400)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Verify API key for futures trading')
    parser.add_argument('-k', '--api_key', type=str, help='API key', required=True)
    parser.add_argument('-s', '--api_secret', type=str, help='API secret', required=True)
    parser.add_argument('-x', '--exchange_name', type=str, help='Exchange name (binance or bybit)', required=True)
    args = parser.parse_args()

    api_key = args.api_key
    api_secret = args.api_secret
    exchange_name = args.exchange_name

    if '--help' in sys.argv[1:]:
        print("Error Codes:\n"
              "  200 - API key is valid and account is open for trading\n"
              "  401 - API key is valid but account is not open for trading\n"
              "  403 - Invalid API key or secret\n"
              "  500 - Error occurred during API request")
    else:
        verify_api(api_key, api_secret, exchange_name)


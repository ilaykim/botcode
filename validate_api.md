# Validate API Script

This script verifies the validity of an API key for futures trading on Binance or Bybit exchanges.

## Usage

python validate_api.py -k <api_key> -s <api_secret> -x <exchange_name>

- -k, --api_key: Your API key
- -s, --api_secret: Your API secret
- -x, --exchange_name: Exchange name (binance or bybit)

## Return Codes

- 200: API key is valid and account is open for trading
- 401: API key is valid but account is not open for trading
- 403: Invalid API key or secret
- 500: Error occurred during API request
- 400: Invalid exchange name

The script exits with the corresponding error code if an issue is encountered.

Example:
python validate_api.py -k <api_key> -s <api_secret> -x invalid_exchange
Output:
Invalid exchange name
Exit code: 400

python validate_api.py -k <invalid_api_key> -s <api_secret> -x binance
Output:
Invalid API key or secret
Exit code: 403



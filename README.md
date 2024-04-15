# Botcode Project

## Adduser.py

The `adduser.py` script automates the process of adding new user API key information to an existing JSON file named `api-keys.json`.

### Command-Line Arguments

- `-u` or `--username`: The username to be added or updated in the JSON file.
- `-x` or `--exchange`: The exchange name associated with the user's API key.
- `-k` or `--key`: The API key.
- `-s` or `--secret`: The secret key associated with the API key.

## Update_account_data.py

This script manages account data for trading bots on Binance and Bybit exchanges. It fetches account balances, open positions, and calculates profit and loss (PnL) for the past 30 days.

### Files Used and Written

- **API Keys File:** `api-keys.json`
- **SQLite Database:** `website_data.db`
- **Account Coins Files:** `<username>_account_coins.json`

### Usage

- To update all accounts: `python update_account_data.py`
- To update a specific account: `python update_account_data.py --account <account_name>`

## Userconfigmanager.py

This script manages user configurations stored in YAML files. It facilitates adding, deleting, resetting user configurations, and listing users or matching configurations based on a template defined in a master YAML file.

### Usage

The script operates through command-line arguments, offering flexibility to perform various operations on user configurations stored in YAML files.

### Example Commands

- Adding a new user based on the master template: `python3 userconfigmanager.py --add_user -a newuser`
- Deleting a user from `config.yaml`: `python3 userconfigmanager.py --delete_user -a existinguser`
- Resetting a user's configuration to match the master template: `python3 userconfigmanager.py --reset_user -a existinguser`
- Listing all users and their symbol counts: `python3 userconfigmanager.py --list_users`
- Listing users with configurations matching the master template: `python3 userconfigmanager.py --list_matching_users`

## Validate_api.py

This script verifies the validity of an API key for futures trading on Binance or Bybit exchanges.

### Usage

`python validate_api.py -k <api_key> -s <api_secret> -x <exchange_name>`

- `-k`, `--api_key`: Your API key
- `-s`, `--api_secret`: Your API secret
- `-x`, `--exchange_name`: Exchange name (binance or bybit)

### Return Codes

- `200`: API key is valid and account is open for trading
- `401`: API key is valid but account is not open for trading
- `403`: Invalid API key or secret
- `500`: Error occurred during API request
- `400`: Invalid exchange name


# User Management

Here's a guide for managing users and their bots in the `passivbot` project:

1. **Adding a New User:**

   To add a new user, use the following command:

   ```bash
   userconfigmanager.py --add_user -a username
   ```

   This command adds a new user with the specified username. For more details and error codes, refer to the `userconfigmanager.md` file in the project folder.

2. **Running the Bot for a User:**

   To start the bot for a specific user, use the following command:

   ```bash
   python3 -c "import subprocess; subprocess.call(['python3', 'manager', 'start', 'username', '-y'], cwd='/home/stablesail/passivbot')"
   ```

   Replace `username` with the actual username. Note that this command does not include error catching. If the username does not match the one set in `adduser.py` or `userconfigmanager.py`, the bot will not start.

3. **Stopping the Bot for a User:**

   To stop the bot for a specific user, use the following command:

   ```bash
   python3 -c "import subprocess; subprocess.call(['python3', 'manager', 'stop', 'username', '-y'], cwd='/home/stablesail/passivbot')"
   ```

4. **Stopping or Starting the Bot for a Single Coin for a User:**

   To stop or start the bot for a single coin for a user, use the following command:

   ```bash
   python3 -c "import subprocess; subprocess.call(['python3', 'manager', 'stop', 'username-coinname', '-y'], cwd='/home/stablesail/passivbot')"
   ```

   Replace `username-coinname` with the combined username and coin name. For example, `john-btc` would be the username for user `john` trading the `BTC` coin.
import yaml
import argparse
import sys

# Constants for file paths
CONFIG_YAML = '/home/stablesail/passivbot/manager/config.yaml'

def read_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file '{file_path}': {e}", file=sys.stderr)
        sys.exit(2)

def find_user_entries(account_name, config_data):
    return [user for user in config_data.get('instances', []) if user and user.get('user') == account_name]

def list_coins(account_name):
    config_data = read_yaml(CONFIG_YAML)
    user_entries = find_user_entries(account_name, config_data)

    if not user_entries:
        print(f"User '{account_name}' not found.", file=sys.stderr)
        sys.exit(3)

    coins = []
    for entry in user_entries:
        coins.extend(entry.get('symbols', []))

    if not coins:
        print(f"No coins found for user '{account_name}'.")
    else:
        print(f"Coins for user '{account_name}':")
        for coin in set(coins):  # Use set to ensure uniqueness
            print(coin)

def main():
    parser = argparse.ArgumentParser(description="List all coins for a given user")
    parser.add_argument('-a', '--account', required=True, help="Account name")

    args = parser.parse_args()

    if args.account:
        list_coins(args.account)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()


import yaml
import argparse
from datetime import datetime
import sys
import os

# Constants for file paths
MASTER_YAML_FOLDER = '/home/stablesail/botcode/configtemplates/'
CONFIG_YAML = '/home/stablesail/passivbot/manager/config.yaml'
DEFAULT_MASTER_FILE = 'master.yaml'

def current_datetime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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

def write_yaml(data, file_path):
    try:
        with open(file_path, 'w') as file:
            yaml.dump(data, file, sort_keys=False)
    except Exception as e:
        print(f"Error writing to '{file_path}': {e}", file=sys.stderr)
        sys.exit(3)

def find_user(account_name, config_data):
    for user in config_data.get('instances', []):
        if user and user.get('user') == account_name:
            return user
    return None

def add_user(account_name, master_file_name=DEFAULT_MASTER_FILE, isreset=False):
    config_data = read_yaml(CONFIG_YAML) or {'instances': []}
    if find_user(account_name, config_data):
        print(f"User '{account_name}' already exists.", file=sys.stderr)
        sys.exit(4)

    master_data = read_yaml(os.path.join(MASTER_YAML_FOLDER, master_file_name))
    new_user_data = [data for data in master_data if data.get('user') == "accountname"]
    for data in new_user_data:
        data['user'] = account_name
        if not isreset:
            data['created_at'] = current_datetime()
        else:
            data['updated_at'] = current_datetime()

    config_data['instances'].extend(new_user_data)
    write_yaml(config_data, CONFIG_YAML)
    print(f"User '{account_name}' added successfully.")

def delete_user(account_name):
    config_data = read_yaml(CONFIG_YAML)
    if not find_user(account_name, config_data):
        print(f"User '{account_name}' not found.", file=sys.stderr)
        sys.exit(5)

    config_data['instances'] = [user for user in config_data.get('instances', []) if user.get('user') != account_name]
    write_yaml(config_data, CONFIG_YAML)
    print(f"User '{account_name}' deleted successfully.")

def reset_user(account_name, master_file_name=DEFAULT_MASTER_FILE):
    config_data = read_yaml(CONFIG_YAML)
    existing_user = find_user(account_name, config_data)
    if not existing_user:
        print(f"User '{account_name}' does not exist and cannot be reset.", file=sys.stderr)
        sys.exit(6)

    delete_user(account_name)
    add_user(account_name, master_file_name, isreset=True)

def list_users():
    config_data = read_yaml(CONFIG_YAML)
    user_symbol_counts = {}

    # Aggregate symbol counts for each user
    for user in config_data.get('instances', []):
        if user:
            user_name = user.get('user')
            symbol_count = len(user.get('symbols', []))
            if user_name in user_symbol_counts:
                user_symbol_counts[user_name] += symbol_count
            else:
                user_symbol_counts[user_name] = symbol_count

    # Print the aggregated symbol counts for each user
    for user_name, symbol_count in user_symbol_counts.items():
        print(f"User: {user_name} - Symbols: {symbol_count}")

def configs_match(master_config, user_config):
    for key, master_value in master_config.items():
        # Skip user comparison directly; focus on configurations
        if key == 'user': continue

        # Ensure the key exists in the user configuration
        if key not in user_config:
            return False
        
        user_value = user_config[key]
        
        # Special handling for lists: compare as sets for order-independent comparison
        if isinstance(master_value, list) and isinstance(user_value, list):
            if set(master_value) != set(user_value):
                return False
        # Direct comparison for other types
        elif master_value != user_value:
            return False
    return True

def all_master_configs_present(master_configs, user_configs):
    # Check if all master configs are matched in the user's configs
    return all(any(configs_match(m_config, u_config) for u_config in user_configs) for m_config in master_configs)

def list_matching_users(master_file_name=DEFAULT_MASTER_FILE):
    master_data = read_yaml(os.path.join(MASTER_YAML_FOLDER, master_file_name))
    config_data = read_yaml(CONFIG_YAML)

    # Filter configurations for 'accountname' in master_data
    master_configs = [config for config in master_data if config.get('user') == 'accountname']

    # Iterate through config_data 'instances', comparing configurations
    matching_users = []
    for config in config_data.get('instances', []):
        user = config.get('user')
        user_configs = [c for c in config_data.get('instances', []) if c.get('user') == user]

        if all_master_configs_present(master_configs, user_configs):
            matching_users.append(user)

    print("Matching Users:")
    for user in set(matching_users):  # Ensure uniqueness
        print(user)

def main():
    parser = argparse.ArgumentParser(description="Manage YAML User Configurations")
    parser.add_argument('-a', '--account', help="Account name")
    parser.add_argument('-m', '--master_file_name', default=DEFAULT_MASTER_FILE, help="Master YAML file name")
    parser.add_argument('--add_user', action='store_true', help="Add a new user")
    parser.add_argument('--delete_user', action='store_true', help="Delete an existing user")
    parser.add_argument('--reset_user', action='store_true', help="Reset user data to master configuration")
    parser.add_argument('--list_users', action='store_true', help="List all users and their symbol counts")
    parser.add_argument('--list_matching_users', action='store_true', help="List users matching the master configuration")

    args = parser.parse_args()

    if args.add_user and args.account:
        add_user(args.account, args.master_file_name, isreset=False)
    elif args.delete_user and args.account:
        delete_user(args.account)
    elif args.reset_user and args.account:
        reset_user(args.account, args.master_file_name)
    elif args.list_users:
        list_users()
    elif args.list_matching_users:
        list_matching_users(args.master_file_name)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

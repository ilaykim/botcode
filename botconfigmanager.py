import json
import os
import argparse
import sys

def create_default_user_config():
    return {
        "wallet risk": 1.0,
        "ema weight": 1.0,
        "wvma weight": 1.0,
        "leverage": 1.0,
        "time offset": 1.0,
        "price threshold": 1.0,
        "random forest": 1.0,
        "xgboost": 1.0,
        "long min markup": 1.0,
        "long markup weight": 1.0,
        "short min markup": 1.0,
        "short markup weight": 1.0
    }

def get_user_config_path(username):
    return f"./{username}_bot_function.json"

def manage_user_config(username, parameter=None, value=None):
    path = get_user_config_path(username)
    if not os.path.exists(path):
        config = create_default_user_config()
        with open(path, 'w') as f:
            json.dump(config, f, indent=4)
        print("New user file created.")
        sys.exit(0)  # Exit code 0: Successful operation
    
    if parameter and value is not None:
        with open(path, 'r+') as f:
            config = json.load(f)
            if parameter in config and 0 <= value <= 2:
                config[parameter] = value
                f.seek(0)
                f.truncate()
                json.dump(config, f, indent=4)
                print("Configuration updated.")
                sys.exit(0)  # Exit code 0: Successful operation
            elif parameter not in config:
                print(f"Error: Invalid parameter name '{parameter}'.")
                sys.exit(2)  # Exit code 2: Invalid parameter name
            else:
                print("Error: Value must be between 0 and 2.")
                sys.exit(3)  # Exit code 3: Invalid value range
    print("No change needed.")
    sys.exit(1)  # Exit code 1: No change needed

def main():
    parser = argparse.ArgumentParser(description="Manage Bot Function Configuration Files")
    parser.add_argument('--user', type=str, required=True, help="Username for the configuration file")
    parser.add_argument('--parameter', type=str, help="Configuration parameter to update")
    parser.add_argument('--value', type=float, help="New value for the parameter (0 to 2)")

    args = parser.parse_args()

    manage_user_config(args.user, args.parameter, args.value)

if __name__ == "__main__":
    main()

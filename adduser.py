import json
import argparse
import sys

def add_user_to_api_keys(filename, username, exchange, key, secret):
    try:
        # Load the existing data
        with open(filename, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(400)
    except json.JSONDecodeError:
        print("Error: The file could not be decoded from JSON.")
        sys.exit(500)

    # Check if the username already exists
    if username in data:
        print(f"Error: The username '{username}' already exists in the JSON data.")
        sys.exit(300)
    
    # Add the new user
    data[username] = {
        "exchange": exchange,
        "key": key,
        "secret": secret
    }

    # Save the updated data
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Error: Failed to write to the file '{filename}'. {str(e)}")
        sys.exit(505)

    print("Success")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Add a user to the API keys file.')
    parser.add_argument('-u', '--username', required=True, help='Username')
    parser.add_argument('-x', '--exchange', required=True, help='Exchange')
    parser.add_argument('-k', '--key', required=True, help='Key')
    parser.add_argument('-s', '--secret', required=True, help='Secret')
    args = parser.parse_args()

    if '--help' in sys.argv[1:]:
        print("Error Codes:\n"
              "  300 - The username already exists in the JSON data.\n"
              "  505 - Failed to write to the file.\n"
              "  400 - The file was not found.\n"
              "  500 - The file could not be decoded from JSON.")
    else:
        add_user_to_api_keys('../passivbot/api-keys.json', args.username, args.exchange, args.key, args.secret)



# adduser.py Script Explanation

The `adduser.py` script is designed to automate the process of adding new user API key information to an existing JSON file named `api-keys.json`. This document provides a detailed explanation of how the script operates, its features, and how to use it effectively.

## Overview

The primary function of the script is to read command-line arguments specifying user details, validate these inputs, and then update the `api-keys.json` file accordingly. It ensures data integrity by preventing duplicate usernames within the JSON file and provides user-friendly feedback in case of errors.

## Requirements

To run this script, you need:
- Python 3.x installed on your system.
- An existing `api-keys.json` file in the same directory as the script. This file should contain JSON-formatted API key information.

## Script Details

### Command-Line Arguments

The script accepts four mandatory arguments:
- `-u` or `--username`: The username to be added or updated in the JSON file.
- `-x` or `--exchange`: The exchange name associated with the user's API key.
- `-k` or `--key`: The API key.
- `-s` or `--secret`: The secret key associated with the API key.

### Operation

Upon execution, the script performs the following operations:
1. **Argument Parsing**: Collects user input from the command line.
2. **File Reading**: Opens and reads the `api-keys.json` file to load existing API key information.
3. **Validation**: Checks if the specified username already exists in the JSON data to avoid duplicates.
4. **Data Updating**: Adds the new user's details to the JSON data if the username is unique.
5. **File Writing**: Saves the updated JSON data back to the `api-keys.json` file.
6. **Success Confirmation**: Prints "Success" upon successful addition of the user details.

### Error Handling

The script includes error handling to provide meaningful feedback in various failure scenarios, such as:
- File not found.
- JSON decoding errors.
- Username duplication.
- File writing errors.

In any error case, the script prints an appropriate message and exits with a non-zero status code, indicating failure.

## Usage Example

To add a new user with the username `username`, exchange `bybit`, key `1111`, and secret `2222`, the following command would be used:

```sh
python3 adduser.py -u username -e bybit -k 1111 -s 2222
```

If the operation is successful, the script will print "Success" and exit with a zero status code. If an error occurs, a relevant error message is printed, and the script exits with a non-zero status code.

## Conclusion

The `adduser.py` script is a useful tool for managing API key information in a JSON file, ensuring data integrity, and simplifying the process of adding new users. By following the usage guidelines provided, you can effectively utilize this script for your API key management needs.

--


-

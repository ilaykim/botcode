# YAML User Configuration Management Tool

Manage user configurations. The script facilitates adding, deleting, resetting user configurations, and listing users or matching configurations based on a template defined in a master YAML file.

## Usage

The script operates through command-line arguments, offering flexibility to perform various operations on user configurations stored in YAML files.

### Command-Line Arguments

1. **Master File Name (`-m` or `--master_file_name`)**: Specifies the master YAML file to use as a template for user configurations. This argument is optional due to the default master file setting.
   
   Default: `master.yaml` located in `/home/stablesail/botcode/configtemplates/`

2. **Account Name (`-a` or `--account`)**: Required for `--add_user`, `--delete_user`, and `--reset_user` operations. Specifies the account name (user) to be added, deleted, or reset in the `config.yaml`.

3. **Operations**: The script supports five operations, selectable via the following options:
   - `--add_user`: Adds a new user configuration to `config.yaml` based on the master template.
   - `--delete_user`: Removes an existing user's configuration from `config.yaml`.
   - `--reset_user`: Resets an existing user's configuration to match the master template, updating or preserving dates as appropriate.
   - `--list_users`: Lists all users in `config.yaml`, showing the total number of symbols associated with each.
   - `--list_matching_users`: Lists users whose configurations in `config.yaml` fully match the template configurations for a placeholder user in the master file.

### Error Codes and Meanings

The script is designed to handle various errors gracefully, providing specific error codes for common issues:

- **Error Code 1**: File not found. This occurs if the specified YAML file cannot be located.
- **Error Code 2**: YAML parsing error. Indicates an issue with reading or interpreting the YAML file, possibly due to malformation.
- **Error Code 3**: Error writing to the YAML file. Could be due to permissions issues or disk space.
- **Error Code 4**: User already exists. Triggered during `--add_user` if the specified user is already present in `config.yaml`.
- **Error Code 5**: User not found. Occurs during `--delete_user` or `--reset_user` if the specified user cannot be located in `config.yaml`.
- **Error Code 6**: User does not exist and cannot be reset. Specific to `--reset_user` when attempting to reset a user that isn't in `config.yaml`.

### Example Commands

Adding a new user based on the master template:
```bash
python3 userconfigmanager.py --add_user -a newuser
```

Deleting a user from `config.yaml`:
```bash
python3 userconfigmanager.py --delete_user -a existinguser
```

Resetting a user's configuration to match the master template:
```bash
python3 userconfigmanager.py --reset_user -a existinguser
```

Listing all users and their symbol counts:
```bash
python3 userconfigmanager.py --list_users
```

Listing users with configurations matching the master template:
```bash
python3 userconfigmanager.py --list_matching_users
```

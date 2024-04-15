# Bot Configuration Manager Documentation

The `botconfigmanager.py` is a Python script designed to manage individual configuration files for bots. 

- **Create Configuration Files**: Automatically creates a new configuration file with default settings if one doesn't exist for a user.
- **Update Configuration Files**: Allows updates to specific configuration parameters within an existing file.
- **Validation**: Ensures all input parameters and values are valid and within specified ranges.
- **Error Handling**: Provides clear error messages and exit codes for various potential issues.

## File Format

Each user's configuration file is named using the pattern `<username>_bot_function.json` and contains the following parameters, each with default values set to `1.0`:

- `wallet risk`
- `ema weight`
- `wvma weight`
- `leverage`
- `time offset`
- `price threshold`
- `random forest`
- `xgboost`
- `long min markup`
- `long markup weight`
- `short min markup`
- `short markup weight`

### Options

- `--user`: Specifies the username associated with the bot configuration.
- `--parameter`: The configuration parameter to update.
- `--value`: The new value for the parameter (must be between 0 and 2).

### Examples

**Create or Check a User's Configuration File:**

```bash
python botconfigmanager.py --user johndoe
```

**Update a Configuration Parameter:**

```bash
python botconfigmanager.py --user johndoe --parameter "wallet risk" --value 1.2
```

## Error Codes

The script defines several exit codes to indicate the status of its execution:

- **0**: Success - The operation completed successfully.
- **1**: No Change Needed - The operation was executed but no changes were needed.
- **2**: Invalid Parameter - The specified parameter name does not exist.
- **3**: Invalid Value - The specified value is out of the allowable range (0 to 2).

import sys
import os
import json
def get_env_variable(var_name, check=True):
    try:
        return os.environ[var_name]
    except KeyError:
        if check:
            error_msg = f"Environment variable {var_name} is not set."
            print(error_msg)
            sys.exit(1)
        return None


def parse_config_file(config_file_path, config_type="json"):
    config_dict = None
    if config_type == "json":
        with open(config_file_path, "r") as f:
            config_dict = json.load(f)
    else:
        print(f"Unsupported config file type: {config_type}")
        sys.exit(1)
    return config_dict
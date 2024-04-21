import json


class ConfigManager:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if ConfigManager.__instance is None:
            ConfigManager.__instance = object.__new__(cls)
        return ConfigManager.__instance

    @staticmethod
    def get_instance():
        if ConfigManager.__instance is None:
            ConfigManager()
        return ConfigManager.__instance

    def __init__(self):
        self.config: dict = None
        self.config_path: str = None

    def load_config(self, config_path):
        self.config_path = config_path
        try:
            with open(config_path, "r") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print(f"Config file not found: {config_path}")
            exit(1)
        except json.JSONDecodeError:
            print(f"Config file is not a valid JSON file: {config_path}")
            exit(1)
        except Exception as e:
            print(f"Error occurred while reading config file: {config_path}")
            print(e)
            exit(1)
        return self.config


if __name__ == '__main__':
    config_manager = ConfigManager.get_instance()
    PROJECT_ROOT_PATH = "FinanceDataAPI"
    DEFAULT_CONFIG_PATH = "config.json"
    config = config_manager.load_config("config.json")
    print(config)

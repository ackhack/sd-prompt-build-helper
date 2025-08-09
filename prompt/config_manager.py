import os.path

from .util import pbh_get_config_file_path, pbh_get_source_dir
from .log_helper import pbh_log_exception, pbh_log_console
from .models.config import Config
import json

from collections import namedtuple


def pbh_jsonDecoder(dict):
    return namedtuple('JsonParsed', dict.keys())(*dict.values())


def from_dict(data_class, data):
    """Recursively convert dicts to dataclasses."""
    if isinstance(data, list):
        return [from_dict(data_class.__args__[0], i) for i in data]
    if hasattr(data_class, "__dataclass_fields__"):
        fieldtypes = {f: t for f, t in data_class.__annotations__.items()}
        return data_class(**{f: from_dict(fieldtypes[f], data[f]) for f in data})
    return data


class ConfigManager:
    def __pbh_get_config_from_disk(self) -> Config | None:
        try:
            path = pbh_get_config_file_path()
            # default to sample if no config is given
            if path is None:
                pbh_log_console("Loading sample config")
                path = pbh_get_source_dir() + "/sample_config.json"
            with open(path, 'r') as f:
                data = json.load(f)
                return from_dict(Config, data)
        except Exception as e:
            pbh_log_exception(e)
            return None

    def __pbh_save_config_to_disk(self, config: Config):
        self.config = config
        with open(pbh_get_config_file_path(), 'w') as f:
            json.dump(config, f)

    # Get current config
    def pbh_get_config(self) -> Config | None:
        return self.__pbh_get_config_from_disk()

    # Save config to manager and disk
    def pbh_save_config(self, config: Config):
        self.__pbh_save_config_to_disk(config)


instance = ConfigManager()


def pbh_get_config_manager() -> ConfigManager:
    return instance

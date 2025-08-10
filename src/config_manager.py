from .util import pbh_get_config_file_path, pbh_get_source_dir
from .log_helper import pbh_log_exception, pbh_log_console
from .prompt.models.config import Config
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
    # Get current config
    def pbh_get_config(self) -> Config | None:
        try:
            data = json.loads(self.pbh_get_config_as_string())
            return from_dict(Config, data)
        except Exception as e:
            pbh_log_exception(e)
            return None

    def pbh_get_config_as_string(self) -> str:
        path = pbh_get_config_file_path()
        # default to sample if no config is given
        if path is None:
            pbh_log_console("Loading sample config")
            path = pbh_get_source_dir() + "/sample_config.json"
        with open(path, 'r') as f:
            return f.read()

    # Save config to manager and disk
    def pbh_save_config(self, config: Config):
        self.pbh_save_config_from_string(json.dumps(config))

    def pbh_save_config_from_string(self, config: str):
        with open(pbh_get_config_file_path(), 'w') as f:
            f.write(config)


instance = ConfigManager()


def pbh_get_config_manager() -> ConfigManager:
    return instance

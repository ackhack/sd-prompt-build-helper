import os.path

from modules.scripts import basedir
from modules.paths import extensions_dir

source_dir = basedir()


def pbh_get_source_dir() -> str:
    return source_dir


data_dir = extensions_dir + "/prompt-build-helper"


def pbh_get_data_dir() -> str:
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir)
    return data_dir


config_file_path = pbh_get_data_dir() + "/config.json"


def pbh_get_config_file_path() -> str | None:
    if not os.path.isfile(config_file_path):
        return None
    return config_file_path


log_file = pbh_get_data_dir() + "/log.log"


def pbh_get_log_file_path() -> str:
    return log_file

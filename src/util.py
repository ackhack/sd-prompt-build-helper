import os.path
import re
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

gallery_folder = data_dir + "/gallery"

def pbh_get_gallery_folder() -> str:
    if not os.path.isdir(gallery_folder):
        os.makedirs(gallery_folder)
    return gallery_folder


def sanitize_folder_name(name: str, replacement="") -> str:
    """
    Sanitize a string to be safe as a folder name.

    - Replaces invalid characters with `replacement`.
    - Strips trailing spaces/dots (Windows limitation).
    """
    # Windows forbidden characters: <>:"/\|?*
    # Remove control characters (ASCII < 32)
    sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1F]', replacement, name)

    # Remove trailing spaces or dots (Windows limitation)
    sanitized = sanitized.rstrip(' .')

    return sanitized
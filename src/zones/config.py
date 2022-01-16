import configparser
from os import path
import pathlib

_CONFIG_FILE_NAME = "config.ini"

_parent_dir = pathlib.Path(__file__).parent.resolve()
_ini_file = path.join(_parent_dir, _CONFIG_FILE_NAME)


config = configparser.ConfigParser()
config.read(_ini_file)


def reload(new_ini_file):
    """Reload config using the specified ini file. Useful for testing."""
    global config
    config = configparser.ConfigParser()
    config.read(new_ini_file)

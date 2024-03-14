from configparser import ConfigParser
import os
from pathlib import Path

from bragir.tracing.logger import logger
from bragir.types import Config

CONFIG_PATH = "~/.bragir/cli/config.ini"


def create_config_file(target_path: Path):
    user_home_directory = os.path.expanduser("~")

    full_file_path = os.path.join(user_home_directory, ".bragir/cli/config.ini")

    os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

    # # Create a config file
    with open(target_path, "w+") as file:
        file.write(
            """# DONT CHANGE STRUCUTRE OF THIS FILE
[audio]
min_silence_len=1000
silence_thresh=-16 # dB (-40)
keep_silence=True

[logging]
logging_level='info'
"""
        )


def read_config(
    config_path: Path,
) -> Config:
    logger.info(f"Reading config from {config_path}")
    config_parser = ConfigParser()
    config_parser.read(config_path)

    config: Config = {}
    for category, values in config_parser.items():
        category_config = {
            category: {key: eval(value) for key, value in values.items()}
        }
        config = {**config, **category_config}

    return config


config = read_config(Path(CONFIG_PATH).expanduser())

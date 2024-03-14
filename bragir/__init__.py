import os
from pathlib import Path

from bragir.config.config import CONFIG_PATH, create_config_file, read_config
from bragir.tracing.logger import logger

path = Path(CONFIG_PATH).expanduser()

if not os.path.isfile(path):
    logger.info(f"Config file not found at: {CONFIG_PATH}")
    logger.info(f"Creating config file at: {CONFIG_PATH}")
    create_config_file(path)
    logger.info(f"Created config file at: {CONFIG_PATH}")


config = read_config(path)

import json
import logging.config
from pathlib import Path
from abc import ABC, abstractmethod


class LoggerStrategy(ABC):
    @abstractmethod
    def setup_logging(self):
        pass


class InfoLoggerStrategy(LoggerStrategy):
    def setup_logging(self):
        config_file_path = Path("logging_configs/info.json")
        with open(config_file_path) as f:
            logging_config = json.load(f)
        logging.config.dictConfig(config=logging_config)


class DebugLoggerStrategy(LoggerStrategy):
    def setup_logging(self):
        config_file_path = Path("logging_configs/debug.json")
        with open(config_file_path) as f:
            logging_config = json.load(f)
        logging.config.dictConfig(config=logging_config)

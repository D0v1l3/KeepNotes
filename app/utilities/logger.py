import logging
import sys

FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s — %(message)s")
LOG_FILE = "app.log"


def get_console_handler() -> logging.StreamHandler:

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler() -> logging.FileHandler:

    file_handler = logging.FileHandler(LOG_FILE, mode="a")
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name: str) -> logging.Logger:

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.propagate = False
    return logger

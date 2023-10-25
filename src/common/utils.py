import os
import re
import sys
import logging
import hashlib
import configparser
from datetime import datetime


# Get the parent directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
g_config = None


def get_ConfigParser():
    global g_config

    if g_config != None:
        return g_config

    g_config = configparser.ConfigParser()
    g_config.read(os.path.join(current_dir, "configurations.ini"))

    return g_config


def get_logger(module_name):
    config = get_ConfigParser()

    log_file_dir = ""
    log_file_name = ""
    log_level_str = ""

    if config.has_section("LOGGING"):
        if config.has_option("LOGGING", "LOG_FILE_PATH"):
            log_file_dir = config.get("LOGGING", "LOG_FILE_PATH")
        if config.has_option("LOGGING", "LOG_FILE_NAME"):
            log_file_name = config.get("LOGGING", "LOG_FILE_NAME")
        if config.has_option("LOGGING", "lOG_LEVEL"):
            log_level_str = config.get("LOGGING", "lOG_LEVEL")

    if log_file_dir:
        if not os.path.exists(log_file_dir):
            os.makedirs(log_file_dir)
    else:
        # Get the parent directory of the current script
        log_file_dir = os.path.dirname(os.path.abspath(__file__))

    if not log_file_name:
        log_file_name = "log_file.log"

    formatter = logging.Formatter(
        "%(asctime)s\t%(levelname)s\t[%(module)s:%(funcName)s]\t%(message)s",
        "%Y-%m-%d %H:%M:%S",
    )

    # Define a mapping from lowercase log level strings to actual logging levels
    log_level_mapping = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    # Default to INFO if the string is invalid
    log_level = logging.INFO

    # Check if the lowercase log level string is a valid log level
    if log_level_str in log_level_mapping:
        log_level = log_level_mapping[log_level_str]

    # Create a log file handler
    log_filename = os.path.join(log_file_dir, log_file_name)
    file_handler = logging.FileHandler(log_filename, mode="a")
    file_handler.setFormatter(formatter)

    # Create a console handler and set the formatter
    channel = logging.StreamHandler(sys.stdout)
    channel.setFormatter(formatter)

    logger = logging.getLogger(module_name)
    logger.setLevel(log_level)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(channel)

    return logger


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def url_to_str(url):
    # Define a regular expression pattern to match special characters
    pattern = r"[\.\/\?!@\$%^&*]"

    # Replace special characters with underscores
    url = url.removeprefix("https://")
    directory_name = re.sub(pattern, "_", url)

    return directory_name


def dir_bacup_helper(directory):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Rename the existing directory
    new_directory_name = f"{directory}_{timestamp}"
    os.rename(directory, new_directory_name)


def string_to_hash(input_string):
    sha1 = hashlib.sha1()
    sha1.update(input_string.encode("utf-8"))
    return sha1.hexdigest()

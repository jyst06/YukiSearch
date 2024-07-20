import configparser
import os


ROOT_PATH = os.getcwd()
CONFIG_FILE_NAME = 'settings.ini'
CONFIG_FILE_PATH = os.path.join(ROOT_PATH, "configs", CONFIG_FILE_NAME)


def read_settings() -> dict:
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)

    minimize_window = config.getboolean('Settings', 'minimize_window', fallback=True)

    return {
        "minimize_window": minimize_window
    }


def edit_settings(option: str, value: str | bool) -> None:
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)

    config.set("Settings", option, str(value))

    with open(CONFIG_FILE_PATH, 'w') as configfile:
        config.write(configfile)

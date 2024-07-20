import configparser
import os
from src.utils import get_writable_path


W_ROOT_PATH = get_writable_path()
CONFIG_FOLDER_PATH = os.path.join(W_ROOT_PATH, "configs")
CONFIG_FILE_NAME = 'settings.ini'
CONFIG_FILE_PATH = os.path.join(CONFIG_FOLDER_PATH, CONFIG_FILE_NAME)

DEFAULT_SETTINGS = {
    "minimize_window": False,
    "show_update_notification": True
}


def ensure_config_file_exists():
    """
    確保資料夾及文件存在
    """
    if not os.path.exists(CONFIG_FOLDER_PATH):
        os.makedirs(CONFIG_FOLDER_PATH)

    if not os.path.exists(CONFIG_FILE_PATH):
        config = configparser.ConfigParser()
        config['Settings'] = {key: str(value) for key, value in DEFAULT_SETTINGS.items()}

        with open(CONFIG_FILE_PATH, 'w') as configfile:
            config.write(configfile)


def read_settings() -> dict:
    ensure_config_file_exists()
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)

    minimize_window = config.getboolean('Settings', 'minimize_window', fallback=True)

    return {
        "minimize_window": minimize_window
    }


def edit_settings(option: str, value: str | bool) -> None:
    ensure_config_file_exists()
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)

    config.set("Settings", option, str(value))

    with open(CONFIG_FILE_PATH, 'w') as configfile:
        config.write(configfile)

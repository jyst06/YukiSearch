from src import show_main_window
from src.api.check_updates import check_latest_release
from src.utils import get_writable_path
import os


__version__ = '1.1.0'


W_ROOT_PATH = get_writable_path()
DATA_FOLDER_PATH = os.path.join(W_ROOT_PATH, 'data')


if __name__ == '__main__':
    os.makedirs(DATA_FOLDER_PATH, exist_ok=True)
    check_latest_release(__version__)
    show_main_window()

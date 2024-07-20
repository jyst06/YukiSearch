from src import show_main_window
from src.api.check_updates import check_latest_release


__version__ = '1.0.0'


if __name__ == '__main__':
    check_latest_release(__version__)
    show_main_window()

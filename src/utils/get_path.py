import os
import sys


def get_application_root_path():
    """
    獲取應用程序根目錄，適用於開發環境和打包後的環境
    """
    if getattr(sys, 'frozen', False):
        # 如果是打包後的程式
        return sys._MEIPASS
    else:
        # 回到上兩級目錄
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_writable_path():
    if getattr(sys, 'frozen', False):
        # 如果是打包後的程式
        return os.path.dirname(sys.executable)
    else:
        # 回到上兩級目錄
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


if __name__ == "__main__":
    print(f"app根目錄: {get_application_root_path()}")
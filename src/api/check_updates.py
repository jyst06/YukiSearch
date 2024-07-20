import requests
import webbrowser
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer
import sys
import time

from src.datamanager.utils import read_settings, edit_settings


def check_latest_release(current_version: str) -> bool:
    if not read_settings().get("show_update_notification", True):
        return False
    try:
        response = requests.get("https://api.github.com/repos/jyst06/YukiSearch/releases/latest")
        response.raise_for_status()
        latest_release = response.json()
        print(f"Latest Version: {latest_release['tag_name']}")
        if current_version != latest_release['tag_name']:
            app = QApplication(sys.argv)
            show_update_prompt(latest_release["assets"][0]["browser_download_url"])
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def show_update_prompt(url=None):
    msg_box = QMessageBox()
    msg_box.setWindowTitle("更新提示")
    msg_box.setText("有可用的更新。是否更新？")

    update_button = msg_box.addButton("更新", QMessageBox.ButtonRole.YesRole)
    later_button = msg_box.addButton("稍後", QMessageBox.ButtonRole.NoRole)
    dont_show_again_button = msg_box.addButton("不再顯示", QMessageBox.ButtonRole.RejectRole)

    msg_box.setIcon(QMessageBox.Icon.Information)

    msg_box.exec()

    clicked_button = msg_box.clickedButton()
    if clicked_button == update_button:
        if url:
            webbrowser.open(url)
        QTimer.singleShot(100, QApplication.quit)
    elif clicked_button == dont_show_again_button:
        edit_settings("show_update_notification", False)
        QTimer.singleShot(100, QApplication.quit)
    else:
        QTimer.singleShot(100, QApplication.quit)


if __name__ == "__main__":
    current_version = "1.0.0"
    check_latest_release(current_version)

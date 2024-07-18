import os
import sys
from random import choice
from PyQt6.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtCore import QSize, Qt, pyqtSignal, QThread

from src.window.main_window import Ui_MainWindow
from src.window.search_widget import SearchWidget
from src.window.home_widget import HomeWidget
from src.window.notification_box_widget import Notification

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.getcwd()

__all__ = ["show_main_window"]

class SearchThread(QThread):
    searchCompleted = pyqtSignal(str)

    def __init__(self, parent=None, search_query=""):
        super().__init__(parent)
        self.search_query = search_query

    def run(self):
        self.searchCompleted.emit(self.search_query)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        stylesheet_path = os.path.join(CURRENT_PATH, "style.css")
        with open(stylesheet_path, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        window_icon_path = os.path.join(ROOT_PATH, "assets/icons/icon.ico")
        self.setWindowIcon(QIcon(window_icon_path))

        self.init_widget_file_class()

        self.setupUi(self)
        self.setWindowTitle("YukiSearch")

        self.side_title_text.setText(" ")
        font = QFont('Arial', 16)
        font.setBold(True)
        self.side_title_text.setFont(font)
        self.side_title_text.setStyleSheet("color: #fff;")
        self.side_title_text.setFixedHeight(30)
        self.side_title_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.side_title_text.setContentsMargins(1, 1, 1, 1)

        self.side_title_icon.setText("")
        self.side_title_icon.setPixmap(QPixmap(os.path.join(ROOT_PATH, "assets/icons/icon.ico")))
        self.side_title_icon.setFixedSize(QSize(50, 40))
        self.side_title_icon.setContentsMargins(5, 1, 1, 1)

        self.listWidget_full_option.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.listWidget_icon.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.side_title_Button.setText("")
        self.side_title_Button.setIcon(QIcon(os.path.join(ROOT_PATH, "assets/icons/sidebar.svg")))
        self.side_title_Button.setFlat(True)
        self.side_title_Button.setFixedSize(QSize(42, 40))
        self.side_title_Button.setContentsMargins(1, 1, 1, 1)
        self.side_title_Button.setCheckable(True)
        self.side_title_Button.setChecked(True)

        self.init_side_menu_items()
        self.init_signal_slots()
        self.init_side_menu_widgets()
        self.init_stack_widgets()

        self.home_widget.searchSignal.connect(self.switch_to_search_and_execute)

    def init_widget_file_class(self):
        self.search_widget = SearchWidget()
        self.home_widget = HomeWidget()
        self.notification_box = Notification(self)

    def init_signal_slots(self):
        self.side_title_text.setHidden(True)
        self.side_title_icon.setHidden(True)
        self.listWidget_full_option.setHidden(True)
        self.listWidget_icon.setVisible(True)

        self.side_title_Button.clicked.connect(self.toggle_side_menu_visibility)
        self.listWidget_full_option.currentRowChanged["int"].connect(self.stackedWidget.setCurrentIndex)
        self.listWidget_icon.currentRowChanged["int"].connect(self.stackedWidget.setCurrentIndex)
        self.listWidget_full_option.currentRowChanged["int"].connect(self.listWidget_icon.setCurrentRow)
        self.listWidget_icon.currentRowChanged["int"].connect(self.listWidget_full_option.setCurrentRow)

    def toggle_side_menu_visibility(self):
        self.side_title_text.setHidden(not self.side_title_text.isHidden())
        self.side_title_icon.setHidden(not self.side_title_icon.isHidden())
        self.listWidget_full_option.setHidden(not self.listWidget_full_option.isHidden())
        self.listWidget_icon.setVisible(not self.listWidget_icon.isVisible())

        if self.side_title_text.isHidden():
            self.set_random_emoji_text()

    def set_random_emoji_text(self):
        self.side_title_text.setText(choice([" ㅇㅅㅇ  ", "(｡･ω･｡)  "]))

    def init_side_menu_widgets(self):
        self.listWidget_icon.clear()
        self.listWidget_full_option.clear()

        self.listWidget_full_option.setSpacing(10)
        self.listWidget_icon.setSpacing(10)

        for item in self.side_menu_list:
            listWidgetIcon = QListWidgetItem()
            listWidgetIcon.setIcon(QIcon(item["icon"]))
            listWidgetIcon.setSizeHint(QSize(40, 40))
            self.listWidget_icon.addItem(listWidgetIcon)
            self.listWidget_icon.setCurrentRow(0)

            listWidgetFull = QListWidgetItem()
            listWidgetFull.setText(item["name"])
            listWidgetFull.setSizeHint(QSize(40, 40))
            self.listWidget_full_option.addItem(listWidgetFull)
            self.listWidget_full_option.setCurrentRow(0)

    def init_stack_widgets(self):
        widget_list = self.stackedWidget.findChildren(QWidget)
        for widget in widget_list:
            self.stackedWidget.removeWidget(widget)

        for item in self.side_menu_list:
            self.stackedWidget.addWidget(item["widget"])

    def init_side_menu_items(self):
        self.side_menu_list = [
            {
                "name": "主頁",
                "icon": os.path.join(ROOT_PATH, "assets/icons/home.svg"),
                "widget": self.home_widget
            },
            {
                "name": "搜尋",
                "icon": os.path.join(ROOT_PATH, "assets/icons/search.svg"),
                "widget": self.search_widget
            },
            {
                "name": "篩選",
                "icon": os.path.join(ROOT_PATH, "assets/icons/filter.svg"),
                "widget": QLabel("篩選 Coming soon")
            },
            {
                "name": "收藏",
                "icon": os.path.join(ROOT_PATH, "assets/icons/bookmark.svg"),
                "widget": QLabel("收藏 Coming soon")
            },
            {
                "name": "紀錄",
                "icon": os.path.join(ROOT_PATH, "assets/icons/clock.svg"),
                "widget": QLabel("紀錄 Coming soon")
            },
            {
                "name": "設定",
                "icon": os.path.join(ROOT_PATH, "assets/icons/settings.svg"),
                "widget": QLabel("設定 Coming soon")
            }
        ]

    def switch_to_search_and_execute(self, search_query):
        self.notification_box.show_notification("提示", "正在搜尋...", font_color="green")

        # Create and start search thread
        self.search_thread = SearchThread(search_query=search_query)
        self.search_thread.searchCompleted.connect(self.search_completed)
        self.search_thread.start()

    def search_completed(self, search_query):
        search_page_index = next(i for i, item in enumerate(self.side_menu_list) if item["name"] == "搜尋")
        self.stackedWidget.setCurrentIndex(search_page_index)
        self.listWidget_full_option.setCurrentRow(search_page_index)
        self.listWidget_icon.setCurrentRow(search_page_index)

        self.search_widget.search_input.setText(search_query)
        self.search_widget.search()


def show_main_window():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    show_main_window()

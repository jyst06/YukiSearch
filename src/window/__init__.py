import os
import sys
from random import choice
from PyQt6.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QWidget, QVBoxLayout, QLabel, QSplashScreen, \
    QProgressBar
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtCore import QSize, Qt, pyqtSignal, QThread, QTimer

from src.window.main_window import Ui_MainWindow
from src.window.search_widget import SearchWidget
from src.window.home_widget import HomeWidget
from src.window.notification_box_widget import Notification


CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.getcwd()


class LoadingScreen(QSplashScreen):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)

        # 載入自訂圖片
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"警告: 無法載入圖片 {image_path}")
            pixmap = QPixmap(400, 200)  # 創建一個空白的 pixmap 作為後備
            pixmap.fill(Qt.GlobalColor.white)  # 填充為白色背景
        else:
            pixmap = pixmap.scaled(400, 200, Qt.AspectRatioMode.KeepAspectRatio,
                                   Qt.TransformationMode.SmoothTransformation)

        self.setPixmap(pixmap)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(0, self.height() - 50, self.width(), 20)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 10px;
                margin: 1px;
            }
        """)

    def progress(self):
        current_value = self.progress_bar.value()
        if current_value < 100:
            self.progress_bar.setValue(current_value + 1)
        else:
            self.close()


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

        # 使用自訂的加載圖片
        loading_image_path = os.path.join(ROOT_PATH, "assets/pics/img.png")
        self.loading_screen = LoadingScreen(loading_image_path)
        self.loading_screen.show()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.initialize_app)
        self.timer.start(30)  # 每30毫秒更新一次加載進度

    def initialize_app(self):
        if self.loading_screen.progress_bar.value() >= 100:
            self.timer.stop()
            self.loading_screen.close()
            self.show()
        else:
            self.loading_screen.progress()
            if self.loading_screen.progress_bar.value() == 30:
                self.init_widget_file_class()
            elif self.loading_screen.progress_bar.value() == 80:
                self.complete_initialization()

    def init_widget_file_class(self):
        self.search_widget = SearchWidget()
        self.home_widget = HomeWidget()
        self.notification_box = Notification(self)

    def complete_initialization(self):
        stylesheet_path = os.path.join(CURRENT_PATH, "style.css")
        with open(stylesheet_path, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        window_icon_path = os.path.join(ROOT_PATH, "assets/icons/icon.ico")
        self.setWindowIcon(QIcon(window_icon_path))

        self.setupUi(self)
        self.setWindowTitle("YukiSearch")

        self.setup_ui_elements()
        self.init_side_menu_items()
        self.init_signal_slots()
        self.init_side_menu_widgets()
        self.init_stack_widgets()

        self.home_widget.searchSignal.connect(self.switch_to_search_and_execute)

    def setup_ui_elements(self):
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
    sys.exit(app.exec())


if __name__ == '__main__':
    show_main_window()
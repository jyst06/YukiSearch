import os
import sys
from random import choice
from PyQt6.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QWidget, QVBoxLayout, QLabel, QSplashScreen, \
    QProgressBar, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QPixmap, QFont, QAction
from PyQt6.QtCore import QSize, Qt, pyqtSignal, QThread, QTimer, QMetaObject

from src.window.main_window import Ui_MainWindow
from src.window.search_widget import SearchWidget
from src.window.home_widget import HomeWidget
from src.window.notification_box_widget import Notification
from src.window.bookmark_widget import BookMarkWidget
from src.window.add_history_widget import AddHistoryWidget
from src.window.history_widget import HistoryWidget
from src.window.setting_widget import SettingWidget
from src.datamanager.utils import read_settings
from src.utils import get_application_root_path


ROOT_PATH = get_application_root_path()
CURRENT_PATH = os.path.join(ROOT_PATH, "src", "window")
STYLESHEET_PATH = os.path.join(CURRENT_PATH, "style.qss")


class LoadingScreen(QSplashScreen):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)

        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"警告: 無法載入圖片 {image_path}")
            pixmap = QPixmap(400, 200)
            pixmap.fill(Qt.GlobalColor.white)
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


class NotificationThread(QThread):
    notificationReady = pyqtSignal(dict)

    def __init__(self, parent=None, notification=None):
        super().__init__(parent)
        self.notification = notification

    def run(self):
        self.notificationReady.emit(self.notification)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, version: str):
        super().__init__()

        self.version = version
        loading_image_path = os.path.join(ROOT_PATH, "assets/pics/img.png")
        self.loading_screen = LoadingScreen(loading_image_path)
        self.loading_screen.show()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.initialize_app)
        self.timer.start(30)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(os.path.join(ROOT_PATH, "assets/icons/icon.ico")))

        tray_menu = QMenu(self)
        restore_action = QAction("恢復", self)
        quit_action = QAction("退出", self)

        restore_action.triggered.connect(self.show)
        quit_action.triggered.connect(QApplication.instance().quit)

        tray_menu.addAction(restore_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        self.tray_icon.show()

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show()
            self.raise_()
            self.activateWindow()

    def closeEvent(self, event):
        if read_settings().get("minimize_window") and self.tray_icon.isVisible():
            self.hide()
            event.ignore()
            print("最小化")

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
        self.bookmark_widget = BookMarkWidget()
        self.history_widget = HistoryWidget()
        self.setting_widget = SettingWidget()

    def complete_initialization(self):
        with open(STYLESHEET_PATH, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        window_icon_path = os.path.join(ROOT_PATH, "assets/icons/icon.ico")
        self.setWindowIcon(QIcon(window_icon_path))

        self.setupUi(self)
        self.setWindowTitle(f"YukiSearch {self.version}")
        self.resize(1500, 900)

        self.setup_ui_elements()
        self.init_side_menu_items()
        self.init_signal_slots()
        self.init_side_menu_widgets()
        self.init_stack_widgets()
        self.connect_signals()

    def connect_signals(self):
        self.home_widget.searchSignal.connect(self.switch_to_search_and_execute)
        self.stackedWidget.currentChanged.connect(self.on_page_changed)
        self.search_widget.notification_signal.connect(self.notification_signal_receive)
        self.search_widget.add_history_signal.connect(self.show_add_history_from_signal)
        self.bookmark_widget.bookmark_remove_msg_signal.connect(self.notification_signal_receive)
        self.bookmark_widget.add_history_signal.connect(self.show_add_history_from_signal)
        self.history_widget.history_remove_msg_signal.connect(self.notification_signal_receive)
        self.history_widget.add_history_signal.connect(self.show_add_history_from_signal)

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
                "name": "收藏",
                "icon": os.path.join(ROOT_PATH, "assets/icons/bookmark.svg"),
                "widget": self.bookmark_widget
            },
            {
                "name": "紀錄",
                "icon": os.path.join(ROOT_PATH, "assets/icons/clock.svg"),
                "widget": self.history_widget
            },
            {
                "name": "設定",
                "icon": os.path.join(ROOT_PATH, "assets/icons/settings.svg"),
                "widget": self.setting_widget
            }
        ]

    def switch_to_search_and_execute(self, search_query):
        self.notification_box.show_notification("提示", "正在跳轉搜尋...", font_color="green", duration=500)

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

    def on_page_changed(self, index):
        current_widget = self.stackedWidget.widget(index)
        if current_widget == self.bookmark_widget:
            self.bookmark_widget.load_bookmarks()
        elif current_widget == self.history_widget:
            self.history_widget.load_histories()

    def notification_signal_receive(self, notification):
        self.notification_thread = NotificationThread(notification=notification)
        self.notification_thread.notificationReady.connect(self.show_notification_from_signal)
        self.notification_thread.start()

    def show_notification_from_signal(self, notification):
        """
        :param notification: {"title": str, "msg": str, "color": str, "time": int}
        """
        try:
            title = notification["title"]
            message = notification["msg"]

            try:
                color = notification["color"]
            except:
                color = "white"

            try:
                duration = notification["time"]
            except:
                duration = 2000

            self.notification_box.show_notification(title, message, font_color=color, duration=duration)
        except Exception as e:
            print(f"Error in show_notification_from_signal: {e}")

    def show_add_history_from_signal(self, kwargs):
        """
        :param kwargs:
            ani_name (str): 動漫名稱
            source (str): 來源
            ani_url (str): 動漫 URL
            image_url (str): 動漫封面圖
        """
        add_history_widget = AddHistoryWidget(self, **kwargs)
        add_history_widget.show()


def show_main_window(version: str):
    app = QApplication(sys.argv)
    window = MainWindow(version)
    sys.exit(app.exec())


if __name__ == '__main__':
    show_main_window()
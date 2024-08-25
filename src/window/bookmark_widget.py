import sys, os
import webbrowser
import requests
import requests_cache
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QComboBox, QScrollArea, QGridLayout, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QPixmap

from src.datamanager import BookMark
from src.datamanager import History
from src.utils import get_application_root_path, get_writable_path


W_ROOT_PATH = get_writable_path()
ROOT_PATH = get_application_root_path()
CURRENT_PATH = os.path.join(ROOT_PATH, "src", "window")
STYLESHEET_PATH = os.path.join(CURRENT_PATH, "style.qss")
NA_PIC_PATH = os.path.join(ROOT_PATH, "assets/pics", "na.jpg")
CACHE_PATH = os.path.join(W_ROOT_PATH, "data", "image_cache")

requests_cache.install_cache(CACHE_PATH, backend='sqlite', expire_after=2592000)


class BookMarkBox(QWidget):
    bookmark_remove_signal = pyqtSignal(bool)
    add_history_signal = pyqtSignal(dict)

    def __init__(self, **kwargs):
        """
        書籤物件區塊

        :param kwargs:
            id (str): 動漫 ID
            ani_name (str): 動漫名稱
            source (str): 來源
            episodes (str): 集數
            time (str): 觀看時間
            ani_url (str): 動漫 URL
            image_url (str): 封面圖 URL
        """
        super().__init__()

        self.bookmark = BookMark()

        self.id = kwargs.get("id")
        self.image_url = kwargs.get("image_url")
        self.ani_name = kwargs.get("ani_name")
        self.ani_url = kwargs.get("ani_url")
        self.source = "來源 : " + kwargs.get("source")
        self.episodes = "觀看至第 " + kwargs.get("episodes") + " 集 " if kwargs.get("episodes") else ""
        self.time = "時間 : " + kwargs.get("time") if kwargs.get("time") else "尚未觀看"

        try:
            self.initUI()
        except Exception as e:
            print(f"Error initializing UI: {e}")

    def initUI(self):
        try:
            with open(STYLESHEET_PATH, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Error loading stylesheet: {e}")

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Image area (left side)
        self.image_label = QLabel()
        self.image_label.setFixedSize(100, 170)
        self.image_label.setStyleSheet("background-color: white;")
        self.load_image(self.image_url)
        layout.addWidget(self.image_label)

        # Labels area (center)
        label_layout = QVBoxLayout()

        anime_name_label = QLabel(self.ani_name)
        label_layout.addWidget(anime_name_label)
        anime_name_label.setStyleSheet(f"font-size: 30px;")

        anime_source_label = QLabel(self.source)
        label_layout.addWidget(anime_source_label)
        anime_source_label.setStyleSheet(f"font-size: 20px;")

        watched_episodes_label = QLabel(self.episodes)
        label_layout.addWidget(watched_episodes_label)
        watched_episodes_label.setStyleSheet(f"font-size: 20px;")

        watched_time_label = QLabel(self.time)
        label_layout.addWidget(watched_time_label)
        watched_time_label.setStyleSheet(f"font-size: 20px;")

        label_layout.setContentsMargins(10, 0, 10, 0)
        label_layout.setSpacing(5)
        layout.addLayout(label_layout, 5)

        button_layout = QVBoxLayout()
        button_layout.setContentsMargins(10, 0, 0, 0)
        button_layout.setSpacing(5)

        watch_button = QPushButton("觀看")
        watch_button.clicked.connect(self.watch_on_click)
        watch_button.setMinimumWidth(100)
        button_layout.addWidget(watch_button)

        remove_button = QPushButton("取消收藏")
        remove_button.clicked.connect(lambda: self.remove_bookmark_on_click(self.id))
        remove_button.setMinimumWidth(100)
        button_layout.addWidget(remove_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.setMinimumWidth(500)
        self.setFixedHeight(200)

    def load_image(self, source):
        try:
            if os.path.isfile(source):  # 檢查是否為本地文件
                pixmap = QPixmap(source)
                if pixmap.isNull():
                    raise ValueError(f"Error loading local image: {source}")
                print(f"Loaded local image: {source}")

            elif self.source == "來源 : 囧次元":
                print("跳過囧次元")
                pixmap = QPixmap(NA_PIC_PATH)
                self.image_label.setPixmap(pixmap.scaled(100, 170, Qt.AspectRatioMode.KeepAspectRatio))

            else:  # 假設是從網路上讀取的
                response = requests.get(source, timeout=1.5)
                response.raise_for_status()
                image_data = response.content
                pixmap = QPixmap()
                pixmap.loadFromData(image_data)
                print(f"Loaded image from URL: {source}")

            self.image_label.setPixmap(pixmap.scaled(100, 170, Qt.AspectRatioMode.KeepAspectRatio))

        except (requests.RequestException, ValueError, Exception) as e:
            print(f"Error loading image: {e}")
            pixmap = QPixmap(NA_PIC_PATH)
            self.image_label.setPixmap(pixmap.scaled(100, 170, Qt.AspectRatioMode.KeepAspectRatio))

    def watch_on_click(self):
        try:
            if "http" not in self.ani_url:
                pass
            else:
                webbrowser.open(self.ani_url)

            data = {
                "ani_name": self.ani_name,
                "ani_url": self.ani_url,
                "source": self.source.split(": ")[1],
                "image_url": self.image_url
            }

            self.add_history_signal.emit(data)
        except Exception as e:
            print(f"Error opening URL or emitting signal: {e}")

    def remove_bookmark_on_click(self, ani_id):
        try:
            self.bookmark.delete_bookmark(ani_id)
            self.bookmark_remove_signal.emit(True)
        except Exception as e:
            print(f"Error removing bookmark or emitting signal: {e}")

class BookMarkWidget(QWidget):
    bookmark_remove_msg_signal = pyqtSignal(dict)
    add_history_signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.bookmarks_format = {
            "id": "",
            "ani_name": "",
            "source": "",
            "episodes": "",
            "time": "",
            "ani_url": "",
            "image_url": ""
        }

        self.bookmark = BookMark()
        self.history = History()

        self.current_filter = 0

        try:
            self.initUI()
        except Exception as e:
            print(f"Error initializing UI: {e}")

    def initUI(self):
        try:
            with open(STYLESHEET_PATH, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Error loading stylesheet: {e}")

        main_layout = QVBoxLayout()

        # Top bar
        top_bar = QHBoxLayout()

        top_bar.addStretch()  # 將 stretch 添加到最左側，使下拉選單靠右

        filter_combo = QComboBox()
        filter_combo.addItems(["全部", "未觀看", "已觀看"])
        filter_combo.currentIndexChanged.connect(lambda: self.load_bookmarks(ani_filter=filter_combo.currentIndex()))
        top_bar.addWidget(filter_combo)

        main_layout.addLayout(top_bar)

        # Scroll area for BookMarkBoxes
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.scroll_layout = QGridLayout(scroll_content)
        self.scroll_layout.setHorizontalSpacing(20)
        self.scroll_layout.setVerticalSpacing(20)

        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

        try:
            self.load_bookmarks()
        except Exception as e:
            print(f"Error loading bookmarks: {e}")

    def load_bookmarks(self, ani_filter=0):
        """
        :param ani_filter: 0代表篩選為全部, 1代表篩選未觀看內容, 2代表篩選已觀看內容
        :return:
        """
        try:
            self.current_filter = ani_filter
            bookmark_dict = []

            # 清除現有的所有書籤
            for i in reversed(range(self.scroll_layout.count())):
                widget = self.scroll_layout.itemAt(i).widget()
                if widget is not None:
                    widget.setParent(None)

            read_bookmark_dict = self.bookmark.read_all_bookmark()

            if read_bookmark_dict:
                # 加入模板
                for item in read_bookmark_dict:
                    history = self.history.find_history_by_id(item["id"])

                    bookmark = self.bookmarks_format.copy()
                    bookmark["id"] = item["id"]
                    bookmark["ani_name"] = item["ani_name"]
                    bookmark["source"] = item["source"]
                    bookmark["episodes"] = history["episodes"] if history else ""
                    bookmark["time"] = history["time"] if history else ""
                    bookmark["ani_url"] = item["ani_url"]
                    bookmark["image_url"] = item["image_url"]

                    bookmark_dict.append(bookmark)

                # 篩選
                if ani_filter == 1:
                    bookmark_dict = [b for b in bookmark_dict if b["episodes"] == ""]
                elif ani_filter == 2:
                    bookmark_dict = [b for b in bookmark_dict if b["episodes"] != ""]

            if bookmark_dict:
                for i in range(len(bookmark_dict)):
                    box = BookMarkBox(**bookmark_dict[i])
                    box.bookmark_remove_signal.connect(self.bookmark_remove_signal_receive)
                    box.add_history_signal.connect(self.add_history_signal_receive)
                    row = i // 2
                    col = i % 2
                    self.scroll_layout.addWidget(box, row, col)
            else:
                no_bookmark_label = QLabel("目前沒有任何收藏內容")
                no_bookmark_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                no_bookmark_label.setStyleSheet("font-size: 18px; color: #888;")
                self.scroll_layout.addWidget(no_bookmark_label, 0, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)
        except Exception as e:
            print(f"Error loading bookmarks: {e}")

    def bookmark_remove_signal_receive(self):
        try:
            self.bookmark_remove_msg_signal.emit({"title": "提示", "msg": "已移出收藏列表", "color": "green", "time": 1500})
            self.load_bookmarks(self.current_filter)
        except Exception as e:
            print(f"Error handling bookmark remove signal: {e}")

    def add_history_signal_receive(self, kwargs):
        try:
            self.add_history_signal.emit(kwargs)
        except Exception as e:
            print(f"Error handling add history signal: {e}")

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        widget = BookMarkWidget()
        widget.resize(900, 600)
        widget.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error running application: {e}")

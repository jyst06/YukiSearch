import sys, os
import requests
import requests_cache
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QComboBox, QScrollArea, QGridLayout, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap


ROOT_PATH = os.getcwd()
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
STYLESHEET_PATH = os.path.join(CURRENT_PATH, "style.css")
NA_PIC_PATH = os.path.join(CURRENT_PATH, "na.png")  # 请确保这个路径是正确的
CACHE_PATH = r"C:\Users\guguc\PycharmProjects\AnimeSearcher\data\image_cache"#os.path.join(ROOT_PATH, "data", "image_cache")


requests_cache.install_cache(CACHE_PATH, backend='sqlite', expire_after=2592000)


class BookMarkBox(QWidget):
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

        self.id = kwargs.get("id")
        self.image_url = kwargs.get("image_url")
        self.ani_name = kwargs.get("ani_name")
        self.ani_url = kwargs.get("ani_url")
        self.source = "來源 : " + kwargs.get("source")
        self.episodes = "觀看至第 " + kwargs.get("episodes") + " 集 " if kwargs.get("episodes") else ""
        self.time = "時間 : " + kwargs.get("time") if kwargs.get("time") else "尚未觀看"

        self.initUI()

    def initUI(self):
        with open(STYLESHEET_PATH, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)  # 设置外边距
        layout.setSpacing(10)  # 设置内部控件间距

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
        layout.addLayout(label_layout, 1)

        # Buttons area (right side)
        button_layout = QVBoxLayout()
        button_layout.setContentsMargins(10, 0, 0, 0)  # 设置按钮区块的外边距
        button_layout.setSpacing(5)  # 设置按钮之间的间距

        remove_button = QPushButton("觀看")
        remove_button.setMinimumWidth(100)
        button_layout.addWidget(remove_button)

        watch_button = QPushButton("取消收藏")
        watch_button.setMinimumWidth(100)
        button_layout.addWidget(watch_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.setFixedSize(500, 200)

    def load_image(self, source):
        try:
            if os.path.isfile(source):  # 檢查是否為本地文件
                pixmap = QPixmap(source)
                if pixmap.isNull():
                    raise ValueError(f"Error loading local image: {source}")
                print(f"Loaded local image: {source}")
            else:  # 假設是從網路上讀取的
                response = requests.get(source)
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

class BookMarkWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        with open(STYLESHEET_PATH, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        main_layout = QVBoxLayout()

        # Top bar
        top_bar = QHBoxLayout()
        top_bar.addStretch()

        filter_combo = QComboBox()
        filter_combo.addItems(["無", "未觀看", "已觀看"])
        top_bar.addWidget(filter_combo)

        filter_button = QPushButton("篩選")
        top_bar.addWidget(filter_button)

        main_layout.addLayout(top_bar)

        # Scroll area for BookMarkBoxes
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QGridLayout(scroll_content)
        scroll_layout.setHorizontalSpacing(20)
        scroll_layout.setVerticalSpacing(20)

        # Add BookMarkBoxes to the grid
        test_dict = {
            "id": "123",
            "ani_name": "有希我婆",
            "source": "我家",
            "episodes": "5",
            "time": "6:09",
            "ani_url": "none",
            "image_url": "https://img.lzzyimg.com/upload/vod/20240703-1/7e664a01462469461c9f5e86830100c1.jpg"
            }
        for i in range(5):
            box = BookMarkBox(**test_dict)
            row = i // 2
            col = i % 2
            scroll_layout.addWidget(box, row, col)

        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def get_bookmarks(self) -> list[dict] | bool:
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = BookMarkWidget()
    widget.resize(900, 600)
    widget.show()
    sys.exit(app.exec())

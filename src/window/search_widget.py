import sys
import os
import requests
import requests_cache
import webbrowser
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QScrollArea, QLabel, QVBoxLayout, QComboBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal

from src.api import Search
from src.datamanager import BookMark
from src.datamanager.utils import generate_id


ROOT_PATH = os.getcwd()
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
NA_PIC_PATH = r"C:\Users\guguc\PycharmProjects\AnimeSearcher\assets\pics\na.jpg"#os.path.join(os.getcwd(), "assets/pics/na.jpg")
CACHE_PATH = r"C:\Users\guguc\PycharmProjects\AnimeSearcher\data\image_cache"#os.path.join(ROOT_PATH, "data", "image_cache")


requests_cache.install_cache(CACHE_PATH, backend='sqlite', expire_after=2592000)


class ResultBox(QWidget):
    notification_signal = pyqtSignal(dict)
    add_history_signal = pyqtSignal(dict)

    def __init__(self, image_url, name, source, ani_url):
        super().__init__()

        self.image_url = image_url
        self.ani_name = name
        self.source = source
        self.ani_url = ani_url

        self.bookmark = BookMark()

        self.setFixedHeight(150)

        # Create main layout
        main_layout = QHBoxLayout()

        # Create preview image label
        self.image_label = QLabel()
        self.image_label.setFixedSize(100, 100)
        self.image_label.setScaledContents(True)
        self.load_image(image_url)

        # Create name and source layout
        text_layout = QVBoxLayout()
        self.name_label = QLabel(name)
        self.name_label.setStyleSheet("color: white; font-size: 25px; padding: 5px 5px; font-weight: bold;")
        self.source_label = QLabel('來源 : ' + source)
        self.source_label.setStyleSheet("color: white; font-size: 18px; padding: 5px 5px;")
        text_layout.addWidget(self.name_label)
        text_layout.addWidget(self.source_label)

        # Create buttons layout
        buttons_layout = QHBoxLayout()
        self.favorite_button = QPushButton("收藏")
        self.favorite_button.clicked.connect(lambda: self.add_bookmark(ani_name=self.ani_name, source=self.source,
                                                                       ani_url=self.ani_url, image_url=self.image_url))
        self.watch_button = QPushButton("觀看")
        self.watch_button.clicked.connect(self.watch_on_click)
        buttons_layout.addWidget(self.favorite_button)
        buttons_layout.addWidget(self.watch_button)

        # Add widgets to main layout
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(text_layout)
        main_layout.addLayout(buttons_layout)

        # Set layout to this widget
        self.setLayout(main_layout)

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

            self.image_label.setPixmap(pixmap)
            self.image_label.setFixedHeight(170)
            self.image_label.setFixedWidth(100)

        except (requests.RequestException, ValueError, Exception) as e:
            print(f"Error loading image: {e}")
            pixmap = QPixmap(NA_PIC_PATH)
            self.image_label.setPixmap(pixmap)
            self.image_label.setFixedHeight(170)
            self.image_label.setFixedWidth(100)

    def add_bookmark(self, ani_name, source, ani_url, image_url):
        if self.bookmark.find_bookmark_by_id(generate_id(ani_name + source)):
            self.notification_signal.emit({"title": "警告", "msg": "已經收藏過了", "color": "red"})
            return

        bookmark = {
            "id": generate_id(ani_name + source),
            "ani_name": ani_name,
            "source": source,
            "ani_url": ani_url,
            "image_url": image_url
        }

        self.bookmark.add_bookmark(**bookmark)
        self.notification_signal.emit({"title": "提示", "msg": "已加入收藏", "color": "green"})

    def watch_on_click(self):
        try:
            webbrowser.open(self.ani_url)

            data = {
                "ani_name": self.ani_name,
                "ani_url": self.ani_url,
                "source": self.source,
                "image_url": self.image_url
            }

            self.add_history_signal.emit(data)
        except Exception as e:
            print(f"Error opening URL or emitting signal: {e}")


class SearchWidget(QWidget):
    notification_signal = pyqtSignal(dict)
    add_history_signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        stylesheet_path = os.path.join(CURRENT_PATH, "style.css")
        with open(stylesheet_path, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        self.setWindowTitle("搜尋範例")
        self.setGeometry(100, 100, 800, 600)

        # 主佈局
        main_layout = QVBoxLayout(self)

        # 搜尋區域
        search_layout = QHBoxLayout()
        search_layout.setContentsMargins(10, 10, 10, 10)  # padding
        search_layout.setSpacing(10)  # 控件之間的間距

        self.search_input = QLineEdit(self)
        self.search_input.setFixedHeight(40)  # 增加高度

        self.search_button = QPushButton("搜尋", self)
        self.search_button.setFixedHeight(40)  # 增加高度
        self.search_button.clicked.connect(self.search)

        # 下拉選單
        self.site_selector = QComboBox(self)
        self.site_selector.addItems(["全部", "動畫瘋", "囧次元", "Anime1", "櫻花"])
        self.site_selector.setFixedHeight(40)  # 增加高度
        self.site_selector.setFixedWidth(125)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.site_selector)
        search_layout.addWidget(self.search_button)

        # 結果區域
        self.result_area = QScrollArea(self)
        self.result_area.setWidgetResizable(True)
        self.result_widget = QWidget()
        self.result_layout = QVBoxLayout(self.result_widget)
        self.result_layout.setContentsMargins(10, 10, 10, 10)  # padding
        self.result_layout.setSpacing(10)  # 控件之間的間距
        self.result_layout.addStretch()  # Add a stretch at the end to push widgets up
        self.result_widget.setLayout(self.result_layout)
        self.result_area.setWidget(self.result_widget)

        # 添加到主佈局
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.result_area)

    def search(self):
        if not self.search_input.text():
            self.display_no_results()
            return

        results = []

        # 刪除舊的內容
        for i in reversed(range(self.result_layout.count() - 1)):
            widget_to_remove = self.result_layout.itemAt(i).widget()
            self.result_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        selected_site = self.site_selector.currentText()
        sites = {
            "全部": ["ani_gamer", "nineciyuan", "anime1", "sakura"],
            "動畫瘋": ["ani_gamer"],
            "囧次元": ["nineciyuan"],
            "Anime1": ["anime1"],
            "櫻花": ["sakura"]
        }

        flag = False
        try:
            for site in sites[selected_site]:
                search = Search(self.search_input.text(), site)
                search_results = search()

                if search_results is None or len(search_results) == 0:
                    continue
                else:
                    flag = True

                for index in search_results:
                    results.append(
                        {"image": search_results[index]['image_url'], "name": search_results[index]['ani_name'],
                         "source": search_results[index]['source'], "ani_url": search_results[index]['ani_url']})
        except Exception as e:
            print(f"Error during search: {e}")

        if not flag:
            self.display_no_results()
            return

        try:
            for result in results:
                custom_widget = ResultBox(result["image"], result["name"], result["source"], result["ani_url"])
                custom_widget.notification_signal.connect(self.notification_signal_receive)
                custom_widget.add_history_signal.connect(self.add_history_signal_receive)
                self.result_layout.insertWidget(self.result_layout.count() - 1,
                                                custom_widget)
        except Exception as e:
            print(f"Error adding result widgets: {e}")

    def display_no_results(self):
        no_results_label = QLabel("無搜尋結果")
        no_results_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        no_results_label.setStyleSheet("font-size: 18px; color: #888; margin: 20px 0;")

        self.result_layout.addWidget(no_results_label)

        self.result_layout.addStretch()

    def notification_signal_receive(self, notification):
        self.notification_signal.emit(notification)

    def add_history_signal_receive(self, kwargs):
        try:
            self.add_history_signal.emit(kwargs)
        except Exception as e:
            print(f"Error handling add history signal: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    search_widget = SearchWidget()
    search_widget.show()
    sys.exit(app.exec())

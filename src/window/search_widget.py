import sys
import requests
import webbrowser
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QScrollArea, QLabel, QVBoxLayout
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from src.api import Search


class ResultBox(QWidget):
    def __init__(self, image_url, name, source, ani_url):
        super().__init__()

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
        self.source_label = QLabel(source)
        text_layout.addWidget(self.name_label)
        text_layout.addWidget(self.source_label)

        # Create buttons layout
        buttons_layout = QHBoxLayout()
        self.favorite_button = QPushButton("收藏")
        self.watch_button = QPushButton("觀看")
        self.watch_button.clicked.connect(lambda: webbrowser.open(ani_url))
        buttons_layout.addWidget(self.favorite_button)
        buttons_layout.addWidget(self.watch_button)

        # Add widgets to main layout
        main_layout.addWidget(self.image_label)
        main_layout.addLayout(text_layout)
        main_layout.addLayout(buttons_layout)

        # Set layout to this widget
        self.setLayout(main_layout)

    def load_image(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            image_data = response.content
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            self.image_label.setPixmap(pixmap)
            self.image_label.setFixedHeight(150)

        except requests.RequestException as e:
            print(f"Error downloading image: {e}")


class SearchWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
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
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #4CAF50;
                padding: 5px;
                border-radius: 10px;
            }
        """)
        self.search_button = QPushButton("搜尋", self)
        self.search_button.setFixedHeight(40)  # 增加高度
        self.search_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                border-radius: 10px;
                border: 1px solid #ccc;
                background-color: #87CEEB;  # 淺藍色背景
            }
            QPushButton:hover {
                background-color: #00BFFF;  # 深藍色背景
            }
        """)
        self.search_button.clicked.connect(self.search)
        search_layout.addWidget(self.search_input)
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
        results = []
        # Clean old results
        for i in reversed(range(self.result_layout.count() - 1)):  # exclude the stretch
            widget_to_remove = self.result_layout.itemAt(i).widget()
            self.result_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        try:
            for site in ["ani_gamer"]:
                search = Search(self.search_input.text(), site)
                search_results = search()

                if search_results is None or len(search_results) == 0:
                    self.display_no_results()
                    return

                for index in search_results:
                    results.append({"image": search_results[index]['image_url'], "name": search_results[index]['ani_name'],
                                    "source": search_results[index]['source'], "ani_url": search_results[index]['ani_url']})
        except Exception as e:
            print(f"Error during search: {e}")

        try:
            for result in results:
                custom_widget = ResultBox(result["image"], result["name"], result["source"], result["ani_url"])
                self.result_layout.insertWidget(self.result_layout.count() - 1, custom_widget)  # Insert before the stretch
        except Exception as e:
            print(f"Error adding result widgets: {e}")

    def display_no_results(self):
        no_results_label = QLabel("無搜尋結果")
        self.result_layout.insertWidget(self.result_layout.count() - 1, no_results_label)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    search_widget = SearchWidget()
    search_widget.show()
    sys.exit(app.exec())


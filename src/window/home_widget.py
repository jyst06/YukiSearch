import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from src.api.week_anime import SearchWeekAnime


CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
STYLESHEET_PATH = os.path.join(CURRENT_PATH, "style.css")


class AnimeBoxWidget(QWidget):
    def __init__(self, title, search_action=None, parent=None):
        super(AnimeBoxWidget, self).__init__(parent)

        with open(STYLESHEET_PATH, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        self.layout = QHBoxLayout()

        self.title_label = QLabel(title)
        self.search_button = QPushButton("搜尋")
        self.search_button.clicked.connect(lambda: search_action(title) if search_action else None)

        self.layout.addWidget(self.title_label)
        self.layout.addStretch()
        self.layout.addWidget(self.search_button)

        self.setLayout(self.layout)
        self.setFixedHeight(70)  # 設定固定高度

    def sizeHint(self):
        return QSize(0, 50)


class HomeWidget(QWidget):
    searchSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        with open(STYLESHEET_PATH, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        week_anime = SearchWeekAnime()
        self.anime_data = week_anime()

        # Set up the main layout
        self.main_layout = QVBoxLayout()

        # Title
        self.title = QLabel("每週更新列表")
        self.title.setStyleSheet("font-size: 24px;")
        self.main_layout.addWidget(self.title, stretch=2)

        # Buttons
        self.button_layout = QHBoxLayout()
        self.day_titles = {
            "週日": "Sun",
            "週一": "Mon",
            "週二": "Tue",
            "週三": "Wed",
            "週四": "Thu",
            "週五": "Fri",
            "週六": "Sat"
        }

        self.buttons = {}
        self.selected_button = None

        for day, key in self.day_titles.items():
            button = QPushButton(day)
            button.clicked.connect(lambda checked, key=key, btn=button: self.update_content(key, btn))
            self.buttons[key] = button
            self.button_layout.addWidget(button)
        self.main_layout.addLayout(self.button_layout, stretch=2)

        # Scrollable area for second widgets
        self.scroll_area = QScrollArea()
        self.scroll_area_widget = QWidget()
        self.scroll_area_layout = QVBoxLayout()
        self.scroll_area_layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # 向上靠齊

        self.second_widgets = []
        self.scroll_area_widget.setLayout(self.scroll_area_layout)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area.setWidgetResizable(True)
        self.main_layout.addWidget(self.scroll_area, stretch=12)

        self.setLayout(self.main_layout)
        self.setWindowTitle("PyQt6 範例")
        self.setGeometry(100, 100, 800, 600)

    def update_content(self, day_key, btn):
        # 更新選中的按鈕樣式
        if self.selected_button:
            self.selected_button.setStyleSheet("")
        btn.setStyleSheet("background-color: #4CAF50;")
        self.selected_button = btn

        # Clear previous widgets
        for widget in self.second_widgets:
            self.scroll_area_layout.removeWidget(widget)
            widget.deleteLater()
        self.second_widgets.clear()

        # Add new widgets
        if day_key in self.anime_data:
            for title in self.anime_data[day_key]:
                second_widget = AnimeBoxWidget(title, search_action=self.search_action)
                self.second_widgets.append(second_widget)
                self.scroll_area_layout.addWidget(second_widget)

    def search_action(self, title):
        print(f"搜尋按鈕被按下，標題是：{title}")
        self.searchSignal.emit(title)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = HomeWidget()
    main_window.show()
    sys.exit(app.exec())

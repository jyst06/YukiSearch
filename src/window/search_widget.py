import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QScrollArea, QLabel, QVBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor


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
                padding: 10px;
                border-radius: 10px;
                border: 1px solid #ccc;
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
        self.result_widget.setLayout(self.result_layout)
        self.result_area.setWidget(self.result_widget)

        # 添加到主佈局
        main_layout.addLayout(search_layout)
        main_layout.addWidget(self.result_area)

    def search(self):
        # 清空以前的結果
        for i in reversed(range(self.result_layout.count())):
            widget_to_remove = self.result_layout.itemAt(i).widget()
            self.result_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        # 模擬一些搜尋結果
        results = ["結果1", "結果2", "結果3", "結果4", "結果5"]
        for result in results:
            result_label = QLabel(result, self)
            result_label.setStyleSheet("""
                QLabel {
                    padding: 10px;
                    border-radius: 5px;
                    border: 1px solid #ccc;
                    background-color: #f0f0f0;
                }
            """)
            self.result_layout.addWidget(result_label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    search_widget = SearchWidget()
    search_widget.show()
    sys.exit(app.exec())

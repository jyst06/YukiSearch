import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QMainWindow, QPushButton
from PyQt6.QtCore import Qt, QTimer

class Notification(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.container = QWidget(self)
        self.container.setStyleSheet("background-color: rgba(0, 0, 0, 360); border-radius: 10px;")

        self.title_label = QLabel(self.container)
        self.message_label = QLabel(self.container)

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(self.title_label)
        layout.addWidget(self.message_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.hide)

    def show_notification(self, title, message, font_color="white", duration=3000):
        self.timer.stop()  # 停止任何正在運行的計時器

        self.title_label.setText(title)
        self.message_label.setText(message)
        self.title_label.setStyleSheet(f"font-family: Microsoft JhengHei; "
                                       f"color: {font_color}; "
                                       f"padding: 5px; "
                                       f"font-size: 20px;"
                                       f"font-weight: bold;")
        self.message_label.setStyleSheet(f"font-family: Microsoft JhengHei; "
                                         f"color: {font_color}; "
                                         f"padding: 5px; "
                                         f"font-size: 16px;")

        self.container.adjustSize()
        self.setFixedSize(self.container.size())
        self.update_position()

        self.show()
        self.timer.start(duration)

    def update_position(self):
        parent = self.parent()
        if parent:
            parent_geometry = parent.geometry()
            self.move(parent_geometry.right() - self.width() - 10,
                      parent_geometry.bottom() - self.height() - 10)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Notification Test")
        self.resize(800, 600)

        self.button = QPushButton("顯示提示", self)
        self.button.clicked.connect(self.show_notification)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.button)
        self.setCentralWidget(central_widget)

        self.notification = Notification(self)

    def show_notification(self):
        self.notification.show_notification("警告", "已新增過此部動漫", font_color="red", duration=3000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
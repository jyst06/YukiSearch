import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QMainWindow, QPushButton
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QRect


class Notification(QWidget):
    def __init__(self, parent, title, message, font_color="white"):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Container widget
        container = QWidget(self)
        container.setStyleSheet("background-color: rgba(0, 0, 0, 180); border-radius: 10px;")

        self.title_label = QLabel(title, container)
        self.message_label = QLabel(message, container)

        self.title_label.setStyleSheet(f"font-family: Microsoft JhengHei; "
                                       f"color: {font_color}; "
                                       f"padding: 5px; "
                                       f"font-size: 20px;"
                                       f"font-weight: bold;")
        self.message_label.setStyleSheet(f"font-family: Microsoft JhengHei; "
                                         f"color: {font_color}; "
                                         f"padding: 5px; "
                                         f"font-size: 16px;")

        layout = QVBoxLayout(container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(self.title_label)
        layout.addWidget(self.message_label)

        container.adjustSize()
        self.setFixedSize(container.size())
        self.update_position(parent)

        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.close_notification)
        self.timer.start(2000)

    def update_position(self, parent):
        parent_geometry = parent.geometry()
        self.move(parent_geometry.right() - self.width() - 10, parent_geometry.bottom() - self.height() - 10)

    def show_notification(self):
        self.show()
        self.animation.start()

    def close_notification(self):
        self.timer.stop()
        self.animation.setDirection(QPropertyAnimation.Direction.Backward)
        self.animation.start()
        self.animation.finished.connect(self.close)


class _TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("test")
        self.resize(800, 600)

        self.button = QPushButton("顯示提示", self)
        self.button.clicked.connect(self.show_notification)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.button)
        self.setCentralWidget(central_widget)

    def show_notification(self):
        notification = Notification(self, "警告", "已新增過此部動漫", font_color="red")
        notification.show_notification()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = _TestWindow()
    main_window.show()
    sys.exit(app.exec())

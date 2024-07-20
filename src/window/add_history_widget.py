import sys, os
import requests
import requests_cache
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                             QSpacerItem, QSizePolicy, QFrame, QMainWindow)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal

from src.datamanager.utils import generate_id
from src.datamanager import History

ROOT_PATH = os.getcwd()
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
NA_PIC_PATH = os.path.join(ROOT_PATH, "assets/pics/na.jpg")
CACHE_PATH = os.path.join(ROOT_PATH, "data", "image_cache")
STYLESHEET_PATH = os.path.join(CURRENT_PATH, "style.qss")

requests_cache.install_cache(CACHE_PATH, backend='sqlite', expire_after=2592000)

class AddHistoryWidget(QWidget):
    # closed = pyqtSignal()

    def __init__(self, parent=None, **kwargs):
        """
        :param parent:
        :param kwargs:
            ani_name (str): 動漫名稱
            source (str): 來源
            ani_url (str): 動漫 URL
            image_url (str): 動漫封面圖
        """
        super().__init__(parent, Qt.WindowType.Window)
        self.data_dict = kwargs
        self.history = History()

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

        # 上方的兩行 Label
        upper_layout = QVBoxLayout()

        label1 = QLabel('添加觀看紀錄')
        label1.setFixedHeight(50)
        self.set_label_style(label1, size=25)
        upper_layout.addWidget(label1)

        label_layout = QHBoxLayout()
        label2 = QLabel(f'名稱 : {self.data_dict["ani_name"]}')
        label2.setFixedHeight(50)
        label2.setMinimumWidth(500)
        self.set_label_style(label2, size=20)
        label_layout.addWidget(label2)

        label3 = QLabel(f'來源 : {self.data_dict["source"]}')
        label3.setFixedHeight(50)
        label3.setMinimumWidth(300)
        self.set_label_style(label3, size=20)
        label_layout.addWidget(label3)

        upper_layout.addLayout(label_layout)

        main_layout.addLayout(upper_layout)

        # 添加分隔線
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("background-color: gray;")
        main_layout.addWidget(line)

        main_layout.addSpacing(30)

        # 中間區塊
        middle_layout = QHBoxLayout()

        self.image_label = QLabel()
        self.image_label.setFixedSize(100, 100)
        self.image_label.setScaledContents(True)
        self.load_image(self.data_dict['image_url'])
        middle_layout.addWidget(self.image_label)

        input_layout = QHBoxLayout()
        input_layout.addStretch()

        label_pre = QLabel('第')
        self.set_label_style(label_pre)
        input_layout.addWidget(label_pre)

        self.episode_input = QLineEdit()
        self.episode_input.setFixedHeight(50)
        self.episode_input.setFixedWidth(100)
        input_layout.addWidget(self.episode_input)

        label4 = QLabel('集')
        self.set_label_style(label4)
        input_layout.addWidget(label4)

        input_layout.addSpacing(20)

        self.min_input = QLineEdit()
        self.min_input.setFixedHeight(50)
        self.min_input.setFixedWidth(80)
        input_layout.addWidget(self.min_input)

        label5 = QLabel('分')
        self.set_label_style(label5)
        input_layout.addWidget(label5)

        input_layout.addSpacing(20)

        self.sec_input = QLineEdit()
        self.sec_input.setFixedHeight(50)
        self.sec_input.setFixedWidth(80)
        input_layout.addWidget(self.sec_input)

        label6 = QLabel('秒')
        self.set_label_style(label6)
        input_layout.addWidget(label6)

        middle_layout.addLayout(input_layout)

        main_layout.addLayout(middle_layout)

        main_layout.addSpacing(30)

        main_layout.addSpacerItem(QSpacerItem(0, 100, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # 最下方的按鈕
        button_layout = QHBoxLayout()

        button_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        button1 = QPushButton('保存')
        button1.setFixedHeight(50)
        button1.clicked.connect(self.save_and_close)
        button_layout.addWidget(button1)

        button2 = QPushButton('取消')
        button2.setFixedHeight(50)
        button2.clicked.connect(self.close)
        button_layout.addWidget(button2)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.setWindowTitle('添加觀看紀錄')
        self.setGeometry(100, 100, 800, 300)

    def set_label_style(self, label, size=15):
        try:
            label.setStyleSheet(f"""
                QLabel {{
                    font-size: {size}pt;
                    font-weight: bold;
                }}
            """)
        except Exception as e:
            print(f"Error setting label style: {e}")

    def save_and_close(self):
        try:
            data = {
                'id': generate_id(self.data_dict['ani_name'] + self.data_dict['source']),
                'ani_name': self.data_dict['ani_name'],
                'source': self.data_dict['source'],
                'ani_url': self.data_dict['ani_url'],
                'image_url': self.data_dict['image_url'],
                'episodes': self.episode_input.text(),
                'time': self.min_input.text() + ":" + self.sec_input.text()
            }
            if self.history.find_history_by_id(generate_id(self.data_dict['ani_name'] + self.data_dict['source'])):
                self.history.edit_history(generate_id(self.data_dict['ani_name'] + self.data_dict['source']), **data)
            else:
                self.history.add_history(**data)

            self.close()
        except Exception as e:
            print(f"Error saving history: {e}")

    # def closeEvent(self, event):
    #     self.closed.emit()
    #     super().closeEvent(event)

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

class _TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('主窗口')
        self.setGeometry(100, 100, 300, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        btn = QPushButton('打開添加歷史記錄窗口', self)
        btn.clicked.connect(self.show_add_history)
        layout.addWidget(btn)

    def show_add_history(self):
        try:
            test_data = {
                'ani_name': '2.5次元的誘惑', 'source': '動畫瘋', 'image_url': 'https://p2.bahamut.com.tw/B/ACG/c/81/0000134781.JPG'
            }
            self.add_history_widget = AddHistoryWidget(self, **test_data)
            # self.add_history_widget.closed.connect(self.on_add_history_closed)
            self.add_history_widget.show()
        except Exception as e:
            print(f"Error showing add history widget: {e}")

    # def on_add_history_closed(self):
    #     print("添加歷史記錄窗口已關閉")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = _TestWindow()
    main_window.show()
    sys.exit(app.exec())

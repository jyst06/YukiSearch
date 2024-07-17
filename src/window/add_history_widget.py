import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
    QGridLayout, QSpacerItem, QSizePolicy


class CustomWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 創建主佈局
        main_layout = QVBoxLayout()

        # 上方的兩行 Label
        upper_layout = QVBoxLayout()

        # 第一行 Label
        label1 = QLabel('Label 1')
        label1.setFixedHeight(50)
        upper_layout.addWidget(label1)

        # 第二行兩個 Label
        label_layout = QHBoxLayout()
        label2 = QLabel('Label 2')
        label2.setFixedHeight(50)
        label_layout.addWidget(label2)

        label3 = QLabel('Label 3')
        label3.setFixedHeight(50)
        label_layout.addWidget(label3)

        upper_layout.addLayout(label_layout)

        main_layout.addLayout(upper_layout)

        # 中間分隔線
        main_layout.addSpacing(30)  # 8:3比例的間距

        # 中間的 ComboBox 和 EntryBox
        middle_layout = QGridLayout()

        combobox1 = QComboBox()
        combobox1.setFixedHeight(50)
        middle_layout.addWidget(combobox1, 0, 0)

        label4 = QLabel('Label 4')
        label4.setFixedHeight(50)
        middle_layout.addWidget(label4, 0, 1)

        middle_layout.addItem(QSpacerItem(20, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum), 0, 2)

        entrybox1 = QLineEdit()
        entrybox1.setFixedHeight(50)
        middle_layout.addWidget(entrybox1, 0, 3)

        label5 = QLabel('Label 5')
        label5.setFixedHeight(50)
        middle_layout.addWidget(label5, 0, 4)

        middle_layout.addItem(QSpacerItem(20, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum), 0, 5)

        entrybox2 = QLineEdit()
        entrybox2.setFixedHeight(50)
        middle_layout.addWidget(entrybox2, 0, 6)

        middle_layout.addItem(QSpacerItem(20, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum), 0, 7)

        label6 = QLabel('Label 6')
        label6.setFixedHeight(50)
        middle_layout.addWidget(label6, 0, 8)

        middle_layout.addItem(QSpacerItem(20, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum), 0, 9)

        combobox2 = QComboBox()
        combobox2.setFixedHeight(50)
        middle_layout.addWidget(combobox2, 0, 10)

        main_layout.addLayout(middle_layout)

        # 中間下方分隔線
        main_layout.addSpacing(30)  # 8:3比例的間距

        # 增加下方區域與底部的距離
        main_layout.addSpacerItem(QSpacerItem(0, 100, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # 最下方的按鈕
        button_layout = QHBoxLayout()

        button_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        button1 = QPushButton('Button 1')
        button1.setFixedHeight(50)
        button_layout.addWidget(button1)

        button2 = QPushButton('Button 2')
        button2.setFixedHeight(50)
        button_layout.addWidget(button2)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.setWindowTitle('Custom Layout')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CustomWidget()
    sys.exit(app.exec())

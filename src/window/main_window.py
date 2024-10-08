from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1344, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.side_title_frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.side_title_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.side_title_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.side_title_frame.setObjectName("side_title_frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.side_title_frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.side_title_icon = QtWidgets.QLabel(parent=self.side_title_frame)
        self.side_title_icon.setObjectName("side_title_icon")
        self.horizontalLayout.addWidget(self.side_title_icon)
        self.side_title_text = QtWidgets.QLabel(parent=self.side_title_frame)
        self.side_title_text.setObjectName("side_title_text")
        self.horizontalLayout.addWidget(self.side_title_text)
        self.side_title_Button = QtWidgets.QPushButton(parent=self.side_title_frame)
        self.side_title_Button.setObjectName("side_title_Button")
        self.horizontalLayout.addWidget(self.side_title_Button)
        self.gridLayout.addWidget(self.side_title_frame, 0, 0, 1, 2)
        self.stackedWidget = QtWidgets.QStackedWidget(parent=self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.stackedWidget.addWidget(self.page_2)
        self.gridLayout.addWidget(self.stackedWidget, 0, 2, 2, 1)
        self.listWidget_icon = QtWidgets.QListWidget(parent=self.centralwidget)
        self.listWidget_icon.setMaximumSize(QtCore.QSize(55, 16777215))
        self.listWidget_icon.setObjectName("listWidget_icon")
        self.gridLayout.addWidget(self.listWidget_icon, 1, 0, 1, 1)
        self.listWidget_full_option = QtWidgets.QListWidget(parent=self.centralwidget)
        self.listWidget_full_option.setMaximumSize(QtCore.QSize(200, 16777215))
        self.listWidget_full_option.setObjectName("listWidget_full_option")
        self.gridLayout.addWidget(self.listWidget_full_option, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1344, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.side_title_icon.setText(_translate("MainWindow", "TextLabel"))
        self.side_title_text.setText(_translate("MainWindow", "TextLabel"))
        self.side_title_Button.setText(_translate("MainWindow", "PushButton"))
import sys
import os
import shutil
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QCheckBox,
                             QMessageBox, QFileDialog, QGroupBox, QFormLayout, QHBoxLayout)
from PyQt6.QtCore import Qt

from src.datamanager.utils import read_settings, edit_settings


CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.getcwd()
DATA_PATH = os.path.join(ROOT_PATH, "data")
STYLESHEET_PATH = os.path.join(CURRENT_PATH, "style.qss")


class SettingWidget(QWidget):
    def __init__(self):
        super().__init__()

        try:
            with open(STYLESHEET_PATH, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            print(f"Error loading stylesheet: {e}")

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Windows 系統選項區塊
        windows_group = QGroupBox("Windows 系統選項")
        windows_layout = QFormLayout()

        self.background_checkbox = QCheckBox("關閉後留在背景")
        self.background_checkbox.setChecked(read_settings()["minimize_window"])
        self.background_checkbox.stateChanged.connect(lambda: edit_settings("minimize_window", self.background_checkbox.isChecked()))
        windows_layout.addRow(self.background_checkbox)

        windows_group.setLayout(windows_layout)
        main_layout.addWidget(windows_group)

        # 導出選項區塊
        export_group = QGroupBox("導出選項")
        export_layout = QVBoxLayout()

        export_bookmarks_button = QPushButton("導出收藏")
        export_bookmarks_button.setFixedHeight(50)
        export_bookmarks_button.setFixedWidth(200)
        export_bookmarks_button.clicked.connect(self.export_bookmarks)
        export_layout.addWidget(export_bookmarks_button)

        export_history_button = QPushButton("導出紀錄")
        export_history_button.setFixedHeight(50)
        export_history_button.setFixedWidth(200)
        export_history_button.clicked.connect(self.export_history)
        export_layout.addWidget(export_history_button)

        export_group.setLayout(export_layout)
        main_layout.addWidget(export_group)

        # 導入選項區塊
        import_group = QGroupBox("導入選項")
        import_layout = QVBoxLayout()

        import_bookmarks_button = QPushButton("導入收藏")
        import_bookmarks_button.setFixedHeight(50)
        import_bookmarks_button.setFixedWidth(200)
        import_bookmarks_button.clicked.connect(self.import_bookmarks)
        import_layout.addWidget(import_bookmarks_button)

        import_history_button = QPushButton("導入紀錄")
        import_history_button.setFixedHeight(50)
        import_history_button.setFixedWidth(200)
        import_history_button.clicked.connect(self.import_history)
        import_layout.addWidget(import_history_button)

        import_group.setLayout(import_layout)
        main_layout.addWidget(import_group)

        self.setLayout(main_layout)
        self.setWindowTitle("設定")
        self.setGeometry(100, 100, 550, 400)  # 設定窗口大小和位置

    def export_bookmarks(self):
        folder_path = QFileDialog.getExistingDirectory(self, "選擇儲存資料夾")
        if folder_path:
            src_path = os.path.join(DATA_PATH, "bookmark.json")
            dst_path = os.path.join(folder_path, "bookmark.json")
            try:
                shutil.copy(src_path, dst_path)
                QMessageBox.information(self, "導出收藏", f"收藏已成功導出到 {dst_path}。")
            except FileNotFoundError:
                QMessageBox.warning(self, "錯誤", "收藏檔案不存在。")
            except Exception as e:
                QMessageBox.critical(self, "錯誤", f"導出收藏失敗: {e}")

    def export_history(self):
        folder_path = QFileDialog.getExistingDirectory(self, "選擇儲存資料夾")
        if folder_path:
            src_path = os.path.join(DATA_PATH, "history.json")
            dst_path = os.path.join(folder_path, "history.json")
            try:
                shutil.copy(src_path, dst_path)
                QMessageBox.information(self, "導出紀錄", f"紀錄已成功導出到 {dst_path}。")
            except FileNotFoundError:
                QMessageBox.warning(self, "錯誤", "紀錄檔案不存在。")
            except Exception as e:
                QMessageBox.critical(self, "錯誤", f"導出紀錄失敗: {e}")

    def import_bookmarks(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "選擇要導入的收藏檔案", "", "JSON Files (*.json)")
        if file_path:
            if os.path.basename(file_path) == "bookmark.json":
                dst_path = os.path.join(DATA_PATH, "bookmark.json")
                try:
                    shutil.copy(file_path, dst_path)
                    QMessageBox.information(self, "導入收藏", f"收藏已成功導入到 {dst_path}。")
                except Exception as e:
                    QMessageBox.critical(self, "錯誤", f"導入收藏失敗: {e}")
            else:
                QMessageBox.warning(self, "錯誤", "檔案名稱不正確，請選擇名為 'bookmark.json' 的檔案。")

    def import_history(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "選擇要導入的紀錄檔案", "", "JSON Files (*.json)")
        if file_path:
            if os.path.basename(file_path) == "history.json":
                dst_path = os.path.join(DATA_PATH, "history.json")
                try:
                    shutil.copy(file_path, dst_path)
                    QMessageBox.information(self, "導入紀錄", f"紀錄已成功導入到 {dst_path}。")
                except Exception as e:
                    QMessageBox.critical(self, "錯誤", f"導入紀錄失敗: {e}")
            else:
                QMessageBox.warning(self, "錯誤", "檔案名稱不正確，請選擇名為 'history.json' 的檔案。")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = SettingWidget()
    widget.show()
    sys.exit(app.exec())

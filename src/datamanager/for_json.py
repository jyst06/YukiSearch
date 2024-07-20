import json
import os
from src.utils import get_writable_path


W_ROOT_PATH = get_writable_path()
CONFIG_FOLDER_PATH = os.path.join(W_ROOT_PATH, "data")


class JsonDataManager:
    def __init__(self, data_file):
        self.data_file = data_file
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """
        檢查資料夾跟json在不在
        """
        os.makedirs(CONFIG_FOLDER_PATH, exist_ok=True)
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w") as file:
                json.dump({"items": []}, file)

    def _load_data(self) -> dict:
        with open(self.data_file, "r") as file:
            data = json.load(file)
        return data

    def _save_data(self, data: dict):
        with open(self.data_file, "w") as file:
            json.dump(data, file, indent=4)

    def find(self, key: str, value: str) -> dict | None:
        """
        查找符合條件的數據
        :param key: 要查找的鍵
        :param value: 要查找的值
        :return: 找到的數據或 None
        """
        data = self._load_data()
        for item in data["items"]:
            if item.get(key) == value:
                return item
        return None

    def add(self, new_item: dict) -> bool:
        """
        添加新數據
        :param new_item: 要添加的新數據
        :return: 是否添加成功
        """
        data = self._load_data()
        data["items"].append(new_item)
        self._save_data(data)
        return True

    def delete(self, key: str, value: str) -> bool:
        """
        刪除符合條件的數據
        :param key: 要刪除的數據的鍵
        :param value: 要刪除的數據的值
        :return: 是否刪除成功
        """
        data = self._load_data()
        initial_length = len(data["items"])
        data["items"] = [item for item in data["items"] if item.get(key) != value]
        if len(data["items"]) < initial_length:
            self._save_data(data)
            return True
        return False

    def update(self, key: str, value: str, updated_data: dict) -> bool:
        """
        修改符合條件的數據
        :param key: 要修改的數據的鍵
        :param value: 要修改的數據的值
        :param updated_data: 更新後的數據
        :return: 是否修改成功
        """
        data = self._load_data()
        for item in data["items"]:
            if item.get(key) == value:
                item.update(updated_data)
                self._save_data(data)
                return True
        return False

    def read_all(self) -> list:
        """
        讀取所有數據
        :return: 所有數據的列表
        """
        data = self._load_data()
        return data["items"]


if __name__ == '__main__':
    data_manager = JsonDataManager("data.json")

    # 添加數據
    # new_item = {"name": "item1", "value": 30}
    # print("Add result:", data_manager.add(new_item))
    #
    # 查找數據
    # found_item = data_manager.find("name", "item1")
    # print("Found item:", found_item)
    #
    # 更新數據
    # # update_result = data_manager.update("name", "item1", {"value": 200})
    # # print("Update result:", update_result)
    #
    # 讀取所有數據
    all_items = data_manager.read_all()
    print("All items:", all_items)

    # 刪除數據
    # delete_result = data_manager.delete("value", 20)
    # print("Delete result:", delete_result)
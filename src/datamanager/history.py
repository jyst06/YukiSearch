from src.datamanager import JsonDataManager
import os


ROOT_PATH = os.getcwd()
HISTORY_PATH = r"C:\Users\guguc\PycharmProjects\AnimeSearcher\data\history.json" #os.path.join(ROOT_PATH, 'data', 'history.json')


class History:
    def __init__(self):
        self.data_manager = JsonDataManager(HISTORY_PATH)
        self.data_format = {
            "id": "",
            "ani_name": "",
            "source": "",
            "episodes": "",
            "time": "",
            "ani_url": "",
            "image_url": ""
        }

    def add_history(self, **kwargs) -> bool:
        """
        添加動漫觀看歷史記錄

        :param kwargs:
            id (str): 動漫 ID
            ani_name (str): 動漫名稱
            source (str): 來源
            episodes (str): 集數
            time (str): 觀看時間
            ani_url (str): 動漫 URL
            image_url (str): 封面圖 URL

        :return:
            bool: 添加是否成功
        """
        data = self.data_format.copy()
        data["id"] = kwargs.get("id")
        data["ani_name"] = kwargs.get("ani_name")
        data["source"] = kwargs.get("source")
        data["episodes"] = kwargs.get("episodes")
        data["time"] = kwargs.get("time")
        data["ani_url"] = kwargs.get("ani_url")
        data["image_url"] = kwargs.get("image_url")
        return self.data_manager.add(data)

    def edit_history(self, ani_id: str, **kwargs) -> bool:
        """
        更新歷史數據

        :param ani_id: 資料ID
        :param kwargs:
            id (str): 動漫 ID
            ani_name (str): 動漫名稱
            source (str): 來源
            episodes (str): 集數
            time (str): 觀看時間
            ani_url (str): 動漫 URL
            image_url (str): 封面圖 URL
        :return: 更新是否成功
        """
        return self.data_manager.update("id", ani_id, kwargs)

    def read_all_history(self) -> list[dict] | None:
        """
        讀取全部紀錄

        :return:
            list: [
            {
            "id": "",
            "ani_name": "",
            "source": "",
            "episodes": "",
            "time": "",
            "ani_url": "",
            "image_url": ""
            },...
            ]
            or None: 如果沒有歷史
        """

        res = self.data_manager.read_all()

        return res if res else None

    def delete_history(self, ani_id: str) -> bool:
        """
        刪除紀錄

        :param ani_id: 動漫 ID
        :return: 刪除是否成功
        """
        return self.data_manager.delete("id", ani_id)

    def find_history_by_id(self, ani_id: str) -> dict | None:
        """
        ID查詢歷史紀錄

        :param ani_id: 動漫ID
        :return:
            dict: 找到的歷史紀錄
            or None: 如果找不到
        """
        return self.data_manager.find("id", ani_id)


if __name__ == '__main__':
    history = History()

    # 測試添加歷史記錄
    test_data = {
        "id": "1",
        "ani_name": "測試動漫",
        "source": "測試來源",
        "episodes": "1",
        "time": "15:30",
        "ani_url": "ani url",
        "image_url": "img url"
    }

    print("測試添加歷史記錄:")
    add_result = history.add_history(**test_data)
    print(f"添加結果: {'成功' if add_result else '失敗'}")

    # 測試讀取所有歷史記錄
    print("\n測試讀取所有歷史記錄:")
    all_history = history.read_all_history()
    print(f"歷史記錄數量: {len(all_history)}")
    print("最後一條記錄:")
    print(all_history[-1] if all_history else "無記錄")

    # 測試編輯歷史記錄
    print("\n測試編輯歷史記錄:")
    edit_data = {
        "episodes": "2",
        "time": "16:00"
    }
    edit_result = history.edit_history(test_data["id"], **edit_data)
    print(f"編輯結果: {'成功' if edit_result else '失敗'}")

    # 再次讀取以驗證編輯結果
    all_history = history.read_all_history()
    edited_entry = next((item for item in all_history if item["id"] == test_data["id"]), None)
    if edited_entry:
        print("編輯後的記錄:")
        print(edited_entry)
    else:
        print("未找到編輯後的記錄")

    # 測試刪除歷史記錄
    print("\n測試刪除歷史記錄:")
    delete_result = history.delete_history(test_data["id"])
    print(f"刪除結果: {'成功' if delete_result else '失敗'}")

    # 最後再次讀取以驗證刪除結果
    all_history = history.read_all_history()
    deleted_entry = next((item for item in all_history if item["id"] == test_data["id"]), None)
    if deleted_entry:
        print("記錄未被成功刪除")
    else:
        print("記錄已成功刪除")


"""管理書籤(收藏)"""
from src.datamanager import JsonDataManager
import os


ROOT_PATH = os.getcwd()
BOOKMARK_PATH = r"C:\Users\guguc\PycharmProjects\AnimeSearcher\data\bookmark.json" #os.path.join(ROOT_PATH, 'data', 'history.json')


class BookMark:
    def __init__(self):
        self.data_manager = JsonDataManager(BOOKMARK_PATH)
        self.data_format = {
            "id": "",
            "ani_name": "",
            "source": "",
            "ani_url": "",
            "image_url": ""
        }

    def add_bookmark(self, **kwargs) -> bool:
        """
        添加書籤

        :param kwargs:
            id (str): 動漫 ID
            ani_name (str): 動漫名稱
            source (str): 來源
            ani_url (str): 動漫 URL
            image_url (str): 封面圖 URL

        :return:
            bool: 添加是否成功
        """
        data = self.data_format.copy()
        data["id"] = kwargs.get("id")
        data["ani_name"] = kwargs.get("ani_name")
        data["source"] = kwargs.get("source")
        data["ani_url"] = kwargs.get("ani_url")
        data["image_url"] = kwargs.get("image_url")
        return self.data_manager.add(data)

    def edit_bookmark(self, ani_id: str, **kwargs) -> bool:
        """
        更新書籤

        :param ani_id: 資料ID
        :param kwargs:
            id (str): 動漫 ID
            ani_name (str): 動漫名稱
            source (str): 來源
            ani_url (str): 動漫 URL
            image_url (str): 封面圖 URL
        :return: 更新是否成功
        """
        return self.data_manager.update("id", ani_id, kwargs)

    def read_all_bookmark(self) -> list[dict] | None:
        """
        讀取全部書籤

        :return:
            list: [
            {
            "id": "",
            "ani_name": "",
            "source": "",
            "ani_url": "",
            "image_url": ""
            },...
            ]
            or None: 如果沒有書籤
        """
        res = self.data_manager.read_all()

        return res if res else None

    def delete_bookmark(self, ani_id: str) -> bool:
        """
        刪除書籤

        :param ani_id: 動漫 ID
        :return: 刪除是否成功
        """
        return self.data_manager.delete("id", ani_id)


if __name__ == '__main__':
    bookmark = BookMark()
    print(bookmark.read_all_bookmark())

    # # 測試添加書籤
    # test_data = {
    #     "id": "1",
    #     "ani_name": "測試動漫",
    #     "source": "測試來源",
    #     "ani_url": "ani url",
    #     "image_url": "img url"
    # }
    #
    # print("測試添加書籤:")
    # add_result = bookmark.add_bookmark(**test_data)
    # print(f"添加結果: {'成功' if add_result else '失敗'}")
    #
    # # 測試讀取所有書籤
    # print("\n測試讀取所有書籤:")
    # all_bookmark = bookmark.read_all_bookmark()
    # print(f"書籤數量: {len(all_bookmark)}")
    # print("最後一條書籤:")
    # print(all_bookmark[-1] if all_bookmark else "無書籤")
    #
    # # 測試編輯書籤
    # print("\n測試編輯書籤:")
    # edit_data = {
    #     "ani_name": "69"
    # }
    # edit_result = bookmark.edit_bookmark(test_data["id"], **edit_data)
    # print(f"編輯結果: {'成功' if edit_result else '失敗'}")
    #
    # # 再次讀取以驗證編輯結果
    # all_bookmark = bookmark.read_all_bookmark()
    # edited_entry = next((item for item in all_bookmark if item["id"] == test_data["id"]), None)
    # if edited_entry:
    #     print("編輯後的書籤:")
    #     print(edited_entry)
    # else:
    #     print("未找到編輯後的書籤")
    #
    # # 測試刪除書籤
    # print("\n測試刪除書籤:")
    # delete_result = bookmark.delete_bookmark(test_data["id"])
    # print(f"刪除結果: {'成功' if delete_result else '失敗'}")
    #
    # # 最後再次讀取以驗證刪除結果
    # all_bookmark = bookmark.read_all_bookmark()
    # deleted_entry = next((item for item in all_bookmark if item["id"] == test_data["id"]), None)
    # if deleted_entry:
    #     print("書籤未被成功刪除")
    # else:
    #     print("書籤已成功刪除")


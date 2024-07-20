"""管理書籤(收藏)"""
from src.datamanager import JsonDataManager
import os
from src.utils import get_writable_path


W_ROOT_PATH = get_writable_path()
BOOKMARK_PATH = os.path.join(W_ROOT_PATH, 'data', 'bookmark.json')


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

    def find_bookmark_by_id(self, ani_id: str) -> dict | None:
        """
        ID查詢書籤

        :param ani_id: 動漫ID
        :return:
            dict: 找到的書籤
            or None: 如果找不到
        """
        return self.data_manager.find("id", ani_id)


if __name__ == '__main__':
    bookmark = BookMark()
    print(bookmark.read_all_bookmark())

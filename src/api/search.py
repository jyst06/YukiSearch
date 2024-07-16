import requests
from bs4 import BeautifulSoup
from src.api.utils import generate_user_agent
from src.api.utils import chinese_traditional_to_simplified
from src.api.utils import read_search_apis, read_video_apis


class Search:
    def __init__(self, ani_name: str, site_name: str):
        """
        :param ani_name: 動漫名
        :param site_name: 網站名 ["ani_gamer", "nineciyuan", "anime1", "sakura"]
        """

        self.search_apis = read_search_apis()
        self.video_apis = read_video_apis()

        self.allow_sites = {
            "ani_gamer": {
                "search_url": self.search_apis["ani_gamer"],
                "ch_name": "巴哈姆特-動畫瘋",
                "lang": "zh-TW"
            },
            "nineciyuan": {
                "search_url": self.search_apis["nineciyuan"],
                "ch_name": "囧次元",
                "lang": "zh-CN"
            },
            "anime1": {
                "search_url": self.search_apis["anime1"],
                "ch_name": "anime1",
                "lang": "zh-TW"
            },
            "sakura": {
                "search_url": self.search_apis["sakura"],
                "ch_name": "櫻花",
                "lang": "zh-CN"
            }
        }

        if site_name not in self.allow_sites:
            raise ValueError('(Search) site_name must be in ["ani_gamer", "nineciyuan", "anime1", "sakura"]')

        if self.allow_sites[site_name]["lang"] == "zh-TW":
            self.url = self.allow_sites[site_name]["search_url"].format(name=ani_name)
        elif self.allow_sites[site_name]["lang"] == "zh-CN":
            self.url = self.allow_sites[site_name]["search_url"].format(name=chinese_traditional_to_simplified(ani_name))

        self.headers = generate_user_agent()
        self.site_name = site_name
        self.site_name_ch = self.allow_sites[site_name]["ch_name"]
        self.template_format = {"ani_name": "", "image_url": "", "source": self.site_name_ch, "ani_url": "", "episodes": 0}

    def get_html(self) -> str:
        response = requests.get(self.url, headers=self.headers)

        if response.status_code == 200:
            return response.text

        else:
            raise Exception(f"Error: {response.status_code}")

    def parse_html(self, html) -> dict | None:
        if self.site_name == "ani_gamer":
            result_dict = {}
            soup = BeautifulSoup(html, 'html.parser')

            ani_name = soup.find_all('p', class_='theme-name')
            ani_url = soup.find_all('a', class_='theme-list-main')
            image_url = soup.find_all('img', class_='theme-img lazyload')

            if not ani_name:
                return None

            for index, img in enumerate(image_url):
                self.template_format["ani_name"] = ani_name[index].text.strip()
                self.template_format["image_url"] = img['data-src']
                self.template_format["ani_url"] = self.video_apis["ani_gamer"].format(url=ani_url[index]['href'])

                result_dict[index] = self.template_format.copy()

            return result_dict

    def __call__(self) -> dict | None:
        """
        :return: {index: {"ani_name": "", "source": "", "image_url": "", "ani_url": ""}, ...n} or None
        """
        return self.parse_html(self.get_html())


if __name__ == '__main__':
    search = Search("青春", "ani_gamer")
    print(search())

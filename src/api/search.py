import requests
import re
import os
from bs4 import BeautifulSoup
from src.api.utils import generate_user_agent
from src.api.utils import chinese_traditional_to_simplified
from src.api.utils import read_search_apis, read_video_apis
from src.datamanager.utils import generate_id


NA_PIC_PATH = r"C:\Users\guguc\PycharmProjects\AnimeSearcher\assets\pics\na.jpg"#os.path.join(os.getcwd(), "assets/pics/na.jpg")


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
        self.template_format = {
            "id": "",
            "ani_name": "",
            "image_url": "",
            "source": self.site_name_ch,
            "ani_url": ""
        }

    def get_html(self) -> str:
        response = requests.get(self.url, headers=self.headers)

        if response.status_code == 200:
            return response.text

        else:
            raise Exception(f"Error: {response.status_code}")

    from bs4 import BeautifulSoup

    def parse_html(self, html) -> dict | None:
        def remove_brackets(text) -> str:
            cleaned_text = re.sub(r'\[.*?\]', '', text)
            return cleaned_text.strip()

        def format_template(site_name, index) -> None:
            self.template_format["id"] = generate_id(ani_name[index] + self.site_name_ch)
            self.template_format["ani_name"] = ani_name[index]

            if image_url:
                self.template_format["image_url"] = image_url[index]
            else:
                self.template_format["image_url"] = NA_PIC_PATH

            if self.video_apis[site_name]:
                self.template_format["ani_url"] = self.video_apis[site_name].format(url=ani_url[index])
            else:
                self.template_format["ani_url"] = ani_url[index]

            result_dict[index] = self.template_format.copy()

        result_dict = {}
        ani_url = []
        ani_name = []
        image_url = []

        soup = BeautifulSoup(html, 'html.parser')
        # ------------------------動畫瘋------------------------
        if self.site_name == "ani_gamer":
            names = soup.find_all('p', class_='theme-name')
            urls = soup.find_all('a', class_='theme-list-main')
            images = soup.find_all('img', class_='theme-img lazyload')

            for name, url, img in zip(names, urls, images):
                ani_name.append(name.text.strip())
                ani_url.append(url['href'])
                image_url.append(img['data-src'])

            if not ani_name:
                return None

            for index in range(len(ani_name)):
                format_template("ani_gamer", index)
        # ------------------------囧次元------------------------
        elif self.site_name == "nineciyuan":
            h3 = soup.find_all('h3')
            div = soup.find_all('div', class_="img-wrapper lazyload img-wrapper-pic")

            for h3_item, div_item in zip(h3, div):
                ani_url.append(h3_item.find('a')['href'])
                ani_name.append(h3_item.find('a')['title'].strip())
                image_url.append(div_item['data-original'])

            if not ani_name:
                return None

            for index in range(len(ani_name)):
                format_template("nineciyuan", index)
        # ------------------------anime1------------------------
        elif self.site_name == "anime1":
            url = soup.find_all('a', rel="category tag")
            name = soup.find_all('a', rel="bookmark")

            for item in url:
                href = item['href']
                if href not in ani_url:
                    ani_url.append(href)

            for item in name:
                if item.find('time'):
                    continue
                n = remove_brackets(item.text)
                if n not in ani_name:
                    ani_name.append(n)

            if not ani_name:
                return None

            for index in range(len(ani_url)):
                format_template("anime1", index)

        return result_dict

    def __call__(self) -> dict | None:
        """
        :return: {index: {"ani_name": "", "source": "", "image_url": "", "ani_url": ""}, ...n} or None
        """
        return self.parse_html(self.get_html())


if __name__ == '__main__':
    ani_gamer = Search("青春豬", "ani_gamer")
    print(ani_gamer())
    nineciyuan = Search("青春豬", "nineciyuan")
    print(nineciyuan())
    anime1 = Search("2.5次元", "anime1")
    print(anime1())

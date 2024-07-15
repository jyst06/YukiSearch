import requests
from bs4 import BeautifulSoup
from src.api.utils import generate


ALLOWED_SITES = {
            "ani_gamer": {
                "search_url": "https://ani.gamer.com.tw/search.php?keyword={name}",
                "ch_name": "巴哈姆特-動畫瘋"
            }
        }


class Search:
    def __init__(self, ani_name: str, site_name: str):
        """
        :param ani_name: 動漫名
        :param site_name: 網站名 ["ani_gamer", ]
        """

        if site_name not in ALLOWED_SITES:
            raise ValueError("(Search) site_name must be in ['ani_gamer']")

        self.headers = generate()
        self.site_name = site_name
        self.site_name_ch = ALLOWED_SITES[site_name]["ch_name"]
        self.url = ALLOWED_SITES[site_name]["search_url"].format(name=ani_name)
        self.template_format = {"ani_name": "", "image_url": "", "source": self.site_name_ch, "ani_url": ""}

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
                self.template_format["ani_url"] = "https://ani.gamer.com.tw/" + ani_url[index]['href']

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

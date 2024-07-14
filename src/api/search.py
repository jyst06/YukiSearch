import requests
from bs4 import BeautifulSoup
from src.api.utils import generate


class Search:
    def __init__(self, ani_name: str, site_name: str):
        """
        :param ani_name: 動漫名
        :param site_name: 網站名 ["ani_gamer", ]
        """
        allowed_sites = {
            "ani_gamer": "https://ani.gamer.com.tw/search.php?keyword={name}",
        }

        if site_name not in allowed_sites:
            raise ValueError("(Search) site_name must be in ['ani_gamer']")

        self.headers = generate()
        self.url = allowed_sites[site_name].format(name=ani_name)

    def get_html(self) -> str:
        response = requests.get(self.url, headers=self.headers)

        if response.status_code == 200:
            return response.text

        else:
            raise Exception(f"Error: {response.status_code}")

    @staticmethod
    def parse_html(html) -> list:
        result_list = []
        soup = BeautifulSoup(html, 'html.parser')
        results = soup.find_all('p', class_='theme-name')

        for name in results:
            result_list.append(name.text.strip())

        return result_list

    def __call__(self):
        return self.parse_html(self.get_html())


if __name__ == '__main__':
    search = Search("青春", "ani_gamer")
    print(search())

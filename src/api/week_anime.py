import time
from bs4 import BeautifulSoup
import requests
import requests_cache
from src.api.utils import generate_user_agent
from src.api.utils import chinese_simplified_to_traditional


class SearchWeekAnime:
    def __init__(self):
        self.url = 'https://bangumi.tv/calendar'
        self.headers = generate_user_agent()
        self.days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

    def get_html(self):
        try:
            with requests_cache.disabled():
                response = requests.get(self.url, headers=self.headers)
                response.encoding = 'utf-8'
                response.raise_for_status()
                return response.text
        except requests.RequestException as e:
            print(f"Error fetching the URL: {e}")
            return None

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        anime_dict = {day: [] for day in self.days}

        for day_name in self.days:
            dd = soup.find_all('dd', class_=day_name.capitalize())
            for item in dd:
                li_tags = item.find_all('li')
                for li in li_tags:
                    info_div = li.find('div', class_='info')
                    p_tag = info_div.find('p')
                    a_content = p_tag.find('a').text.strip()
                    if a_content:
                        anime_name = a_content
                    else:
                        small_content = info_div.find('small').text.strip()
                        anime_name = small_content

                    anime_dict[day_name].append(chinese_simplified_to_traditional(anime_name))
                    time.sleep(0.05)

        return anime_dict

    def __call__(self) -> dict | None:
        html = self.get_html()
        if html:
            return self.parse_html(html)
        return None


if __name__ == '__main__':
    search_week_anime = SearchWeekAnime()
    result = search_week_anime()
    print(result)
from datetime import datetime

import requests
from bs4 import BeautifulSoup as bs


def get_data(link, year):
    r = requests.get(f'{link}/result{year}-{year + 1}.php')
    if r.ok:
        soup = bs(r.text, "html.parser")
        table = soup.find('table')
        hrefs = table.find_all('a', href=True)
        for href in hrefs:
            url = f"{link}/{href['href'][1:]}"
            resp = requests.get(url)
            if resp.ok:
                print(resp.content)
                return None


def parse_matlab() -> dict:
    start_year = 2021
    now = datetime.now()
    address = 'https://serjmak.com/2students'

    courses = ['matlaba', 'matlabma']

    res = dict()
    # todo: ну ты понял в res все типо {'https://serjmak.com/2students/matlaba/test2/2021-2022/Abulhanov.txt': 'content', ...}
    for course in courses:
        for year in range(start_year, now.year):
            get_data(f'{address}/{course}', year)

    return res

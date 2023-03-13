from datetime import datetime

import requests
from bs4 import BeautifulSoup as bs


def get_data(link, year) -> list[tuple[str, str]]:
    r = requests.get(f'{link}/result{year}-{year + 1}.php')
    if r.ok:
        soup = bs(r.text, "html.parser")
        table = soup.find('table')
        hrefs = table.find_all('a', href=True)
        res = []
        for href in hrefs:
            url = f"{link}/{href['href'][1:]}"
            resp = requests.get(url)
            if resp.ok:
                resp.encoding = 'utf8'
                res.append((url, resp.text))

                # todo: убрать потом
                if len(res) == 10:
                    return res

        return res


def parse_matlab() -> dict:
    start_year = 2021
    now = datetime.now()
    address = 'https://serjmak.com/2students'

    courses = ['matlaba', 'matlabma']

    res = dict()
    for course in courses:
        for year in range(start_year, now.year - 1):
            link = f'{address}/{course}'
            data = get_data(link, year)
            for url, content in data:
                res[url] = content

    return res

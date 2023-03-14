import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup as bs


def get_data(link, year):
    r = requests.get(f'{link}/result{year}-{year + 1}.php')
    res = []
    if r.ok:
        soup = bs(r.text, "html.parser")
        table = soup.find('table')
        hrefs = table.find_all('a', href=True)

        for href in hrefs:
            hr = href['href']
            index = hr.find('/')
            url = f"{link}/{hr[index + 1:]}"
            resp = requests.get(url)
            if resp.ok:
                resp.encoding = 'utf-8'
                res.append((url, resp.text))
            time.sleep(0.1)
    return res


def parse_matlab(start_year=2014):
    now = datetime.now()
    address = 'https://serjmak.com/2students'
    courses = ['matlaba', 'matlabma']
    res = dict()
    for course in courses:
        print(f'=================={course.upper()}==================')
        for year in range(start_year, now.year - 1):
            print(f'{year}')
            link = f'{address}/{course}'
            data = get_data(link, year)
            for url, content in data:
                res[url] = content
    return res


def get_content(url):
    resp = requests.get(url)
    if resp.ok:
        resp.encoding = 'utf-8'
        return resp.text
    return ''


def parse_text(url, encoding):
    r = requests.get(url)
    if r.ok:
        r.encoding = encoding
        return r.text
    else:
        return 'Не удалось получить текст. Проверьте ссылку.'

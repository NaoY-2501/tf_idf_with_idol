import csv
import logging
import os
import re
import shutil
import sys
import time
import traceback

import chromedriver_binary # 76.0.3809.132に合わせて76.0.3809.126.0をインストール

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

BASE_URL = 'https://ameblo.jp'
LIST_URL = BASE_URL + '/soratobsakana/theme{page}-10088247761.html'
DATE_PAT = re.compile(r'(?P<year>[\d]+)年(?P<month>[\d]+)月(?P<day>[\d]+)日[(\w)]+ (?P<hour>[\d]+)時(?P<minute>[\d]+)分')
IMG_PAT = re.compile(r'この画像をシェア')
MAX_PAGES = 12
URL_FILE = 'article_urls.txt'
CSV_FILE = 'code/mana_blog.csv'
BACKUP = f'{CSV_FILE}.bk'
FIELDNAMES = ['date', 'url', 'title', 'body']

logging.basicConfig(filename='scraping.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def init_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    return driver


def get_soup(driver: webdriver.Chrome, url: str) -> bs:
    driver.get(url)
    html = driver.page_source
    return bs(html, 'html.parser')


def get_article_list(soup: bs) -> list:
    article_list = soup.find_all('li', class_='skin-borderQuiet')
    links = []
    for item in article_list:
        links.append(BASE_URL + item.find('a')['href'])
    return links


def parse_post_date(soup: bs) -> str:
    post_date = soup.find('time').text
    g = DATE_PAT.search(post_date)
    return f"{g['year']}/{g['month']}/{g['day']} {g['hour']}:{g['minute']}"


def get_article_title(soup: bs) -> str:
    return soup.find('a', class_='skinArticleTitle').text


def get_article_body(soup: bs) -> str:
    article = soup.find('div', class_='skin-entryBody')
    children = article.children
    # 空文字を除去する
    rows = list(
        filter(
            lambda x: len(x) > 0,
            [child.strip() if isinstance(child, str) else child.text for child in children]
            )
        )
    # 画像の位置に表示される"この画像をシェア"を除去
    subed_rows = [re.sub(IMG_PAT, '', row) for row in rows]
    return '\n'.join(subed_rows)


def get_extracted_url() -> list:
    with open(CSV_FILE, 'r') as f:
        dates = []
        reader = csv.DictReader(f, fieldnames=FIELDNAMES)
        for row in reader:
            dates.append(row['url'])
    return dates


def get_collected_urls() -> list:
    with open(URL_FILE, 'r') as f:
        urls = []
        for url in f:
            urls.append(url.strip())
    return urls


def main():
    driver = init_driver()
    collected_urls = []  # 収集済みURL
    extracted_urls = [] # 抽出済みURL

    if os.path.exists(URL_FILE):
        collected_urls = get_collected_urls()
    if os.path.exists(CSV_FILE):
        extracted_urls = get_extracted_url()
        # バックアップ
        shutil.copyfile(CSV_FILE, BACKUP)

    print('Collect article URL.')
    with open(URL_FILE, 'a') as f:
        for page in tqdm(range(MAX_PAGES, 0, -1)):
            list_url = LIST_URL.format(page=page)
            soup = get_soup(driver, list_url)
            for url in get_article_list(soup)[::-1]:
                if url not in collected_urls:
                    f.write(url + '\n')
                    logging.info('%s collected', url)

    with open(URL_FILE, 'r') as f:
        article_urls = [url.strip() for url in f.readlines()]

    time.sleep(5)

    print('Extract data from each articles.')
    with open(CSV_FILE, 'a') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not extracted_urls:
            writer.writeheader()
        for article_url in tqdm(article_urls):
            if article_url not in extracted_urls:
                logging.info('%s has extracted.', article_url)
            else:
                continue
            soup = get_soup(driver, article_url)
            try:
                post_date = parse_post_date(soup)
            except AttributeError as e:
                logging.error("%s can't extracted %s", article_url, e)
                logging.error(traceback.format_exc())
                print(traceback.format_exc())
                sys.exit()
            title = get_article_title(soup)
            body = get_article_body(soup)
            writer.writerow({
                'date': post_date,
                'url': article_url,
                'title': title,
                'body': body
            })
            time.sleep(5)
    # バックアップ削除
    if os.path.exists(BACKUP):
        os.remove(BACKUP)


if __name__ == '__main__':
    main()

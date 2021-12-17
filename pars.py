import requests
import json
import pymysql
from bs4 import BeautifulSoup
from constants import *
from secondary_function import *


def select_leagues_url(url):
    data = []
    try:
        connection = pymysql.connect(host='141.8.192.193',
                                     user='a0595563',
                                     password='kaifamumig',
                                     db='a0595563_Transfer',
                                     cursorclass=pymysql.cursors.DictCursor)
        print('Success!')

        try:
            with connection.cursor() as cursor:
                sql = "SELECT id, url, type, is_parse, date_parse FROM leagues_url"
                cursor.execute(sql, data)
                data = cursor.fetchall()

        finally:
            connection.close()
        return list(data)

    except Exception as ex:
        print(ex, select_leagues_url.__name__)


def get_pagination_leagues(url):
    try:
        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        pagination = soup.find(class_='tm-pagination__list-item tm-pagination__list-item--icon-last-page').find(
            'a').get('href')
        pagination_leagues_number = int(pagination.split('=')[-1])
        return pagination_leagues_number + 1

    except AttributeError as ex: #пагинаций не обнаружено
        return 2
    except Exception as ex:
        print(ex, type(ex), get_pagination_leagues.__name__)


def parsing_leagues_url(url, urls):
    try:
        new_urls = []
        if urls is None:
            urls = []
        # if get_pagination_leagues(url)
        for pagination in range(1, get_pagination_leagues(url)):
            new_url = f'{url}?page={pagination}'
            req = requests.get(new_url, headers=headers)
            src = req.text
            soup = BeautifulSoup(src, 'lxml')
            leagues_page = soup.find_all(class_='inline-table')
            for league in leagues_page:
                link = getFullURL(league.find('tr').contents[-2].find('a').get('href'))
                id = link.split('/')[-1]
                x = False
                for elem in urls:
                    if elem['id'] == id:
                        x = True
                        break
                if x:
                    continue
                new_urls.append({'id': id, 'url': link, 'type': 'l', 'is_parse': 0, 'date_parse': '0000-00-00'})
        return new_urls


    except Exception as ex:
        print(ex, parsing_leagues_url.__name__)


def insert_urls_after_parse_in_bd(urls):
    try:
        connection = pymysql.connect(host='141.8.192.193',
                                     user='a0595563',
                                     password='kaifamumig',
                                     db='a0595563_Transfer',
                                     cursorclass=pymysql.cursors.DictCursor)
        print('Success!')

        try:
            count = 0
            for league in urls:
                try:
                    with connection.cursor() as cursor:
                        sql = "INSERT INTO leagues_url (`id`, `url`, `type`, `is_parse`, `date_parse`) VALUES (%s, %s, %s, %s, %s)"
                        cursor.execute(sql, (
                        league['id'], league['url'], league['type'], league['is_parse'], league['date_parse']))
                        print(f"Для лиги {league['id']} изменено(а) {cursor.rowcount} строк(а)")
                        connection.commit()
                        count += 1
                except pymysql.err.IntegrityError as ex:
                    print(f"Ключ {league['id']} существует")
        finally:
            connection.close()
            print(f'Изменено {count} строк')

    except Exception as ex:
        print(ex, insert_urls_after_parse_in_bd.__name__)


def main_parsing(continent=['europa', 'asian', 'amerika', 'afrika']):

    try:

        for elem in continent:

            url = f'https://www.transfermarkt.ru/wettbewerbe/{elem}'

            leagues_url_from_db = select_leagues_url(url)  # получили список лиг из базы данных

            leagues_url_not_db = parsing_leagues_url(url, leagues_url_from_db)  # получаем список лиг которых нет в базе данных

            insert_urls_after_parse_in_bd(leagues_url_not_db)  # загружаем недостающие лиги в базу данных

    except Exception as ex:
        print(ex, main_parsing.__name__)


main_parsing()


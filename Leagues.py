import requests
from bs4 import BeautifulSoup
import datetime as DT
import re
import time
from random import randrange
import pymysql
import json
from loguru import logger

logger.add('leagues_debug.log', format='{time} {level} {message}', level="DEBUG")

headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Mobile Safari/537.36 Edg/95.0.1020.40"
}

url = 'https://www.transfermarkt.ru/wettbewerbe/europa'

list = []
leagues = []

@logger.catch()
def get_pagination(url):
    try:
        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        pagination = soup.find(class_='tm-pagination__list-item tm-pagination__list-item--icon-last-page').find('a').get('href')
        pagination_number = int(pagination.split('=')[-1])
    except Exception as ex:
        logger.exception(ex)

@logger.catch()
def parsing_leagues(url):
    try:
        for pagination in range(2):
            url = f'https://www.transfermarkt.ru/wettbewerbe/europa?page={pagination}'
            count_leagues = 0
            req = requests.get(url, headers=headers)
            src = req.text
            soup = BeautifulSoup(src, 'lxml')
            leagues_page = soup.find(class_='items').find_all('a')

            for league in leagues_page:
                league_src = league.find_all('img')
                for src in league_src:
                    list.append({'src': src.get('src')})

                if not league.find('img'):
                    list.append( {
                        'name': league.get('title'),
                        'link': getFullURL(league.get('href'))
                    })

        for dict in range(0, len(list), 2):
            leagues.append({**list[dict], **list[dict + 1]})

    except Exception as ex:
        logger.exception(ex)

getFullURL = lambda url: f"https://www.transfermarkt.ru{url}"

get_pagination(url)
parsing_leagues(url)

json.dump(leagues, open('leagues.json', 'w', encoding='utf-8'), indent = 2, ensure_ascii=False)











import requests
import json
from bs4 import BeautifulSoup
from loguru import logger
from secondary_function import headers
from secondary_function import getFullURL

logger.add('leagues_debug.log', format='{time} {level} {message}', level="DEBUG")

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
        return pagination_number

    except Exception as ex:
        logger.exception(ex)


@logger.catch()
def parsing_leagues(url):
    try:
        # for pagination in range(1, get_pagination(url)):
        for pagination in range(1, 2):
            new_url = f'{url}?page={pagination}'
            req = requests.get(new_url, headers=headers)
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
                        'link': getFullURL(league.get('href')),
                        'key' : league.get('href').split('/')[-1]
                    })
            print(f'{new_url} ОК')
        for dict in range(0, len(list), 2):
            leagues.append({**list[dict], **list[dict + 1]})

    except Exception as ex:
        logger.exception(ex)

def main(url):

    get_pagination(url)
    parsing_leagues(url)

    json.dump(leagues, open('leagues.json', 'w', encoding='utf-8'), indent = 2, ensure_ascii=False)

main('https://www.transfermarkt.ru/wettbewerbe/europa')

# https://www.transfermarkt.ru/wettbewerbe/europaJugend
# https://www.transfermarkt.ru/wettbewerbe/europa










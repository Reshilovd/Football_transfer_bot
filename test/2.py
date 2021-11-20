import requests
from bs4 import BeautifulSoup
import datetime as DT
import re
import time
from random import randrange
import pymysql
from loguru import logger
headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Mobile Safari/537.36 Edg/95.0.1020.40"
}

logger.add('debug.log', format='{time} {level} {message}', level="DEBUG")

@logger.catch()
def parsing_player_info(url):
    info  = {}
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    try:
        try:
            photo = soup.find(rel="preload").get('href')
            info['photo'] = photo
        except AttributeError:
            logger.exception(f'Фото не найдено: {url}')

        try:
            name = soup.find(class_='dataName')
            last_name = name.find('b').text
            # first_name = ' '.join(name.find('h1').text.split()[:-1 * len(last_name.split())])
            first_name = ' '.join(filter(lambda x: not x in last_name.split(), name.find('h1').text.split()))
            info['first_name'] = first_name
            info['last_name'] = last_name
        except IndexError:
            #Если только имя
            info['first_name'] = name[0]
            info['last_name'] = ''
        except AttributeError:
            #Если имя вообще нет
            info['first_name'] = ''
            info['last_name'] = ''
            logger.exception(f'Имя не найдено: {url}')


        try:
            birthday = soup.find(class_='dataValue').text.split()
            day = birthday[0]
            month = getMonthByName(birthday[1])
            year = birthday[2]
            date = year + month + day
            date = DT.datetime.strptime(date, '%Y%m%d').date()
            info['birthday'] = str(date)
        except AttributeError:
            info['birthday'] = '1000-01-01'
            logger.exception(f'Дата рождения не найдена: {url}')

        except KeyError:
            info['birthday'] = '1000-01-01'
            logger.exception(f'Ошибка ключа: {url}')

        except TypeError:
            info['birthday'] = '1000-01-01'
            logger.exception(f'Ошибка типа: {url}')

        try:
            death_date = soup.find(itemprop="deathDate").text.split()
            del death_date[-1]
            death_date = death_date[0]
            death_date = death_date.split('.')
            day = death_date[0]
            month = death_date[1]
            year = death_date[2]
            date = year + month + day
            date = DT.datetime.strptime(date, '%Y%m%d').date()
            info['death_date'] = str(date)

        except AttributeError:
            info['death_date'] = ''
            logger.exception(f'Дата смерти не найдена {url}')


        try:
            height = soup.find(itemprop="height").text
            height = height.replace(',','.').replace('м','')
            height = float(height)*100
            info['height'] = height

        except AttributeError:
            logger.exception(f'Рост не найден {url}')

        try:
            nation = soup.find(class_='info-table').find_all(class_='flaggenrahmen')
            list_nation = []

            for i in nation:
                if not i.get('alt') in list_nation:
                    list_nation.append(i.get('alt'))
            info['nation'] = list_nation
            if len(list_nation) > 2:
                logger.exception(f'Подозрительное количество наций {url}')


        except AttributeError:
            info['nation'] = ''
            logger.exception(f'Нация не найдена {url}')


        try:
            position = soup.find(class_='detail-position__position').text
            info['position'] = position
        except AttributeError:
            info['position'] = ''
            logger.exception(f'Позиция не найдена {url}')

        try:
            national_team = soup.find(class_='flaggenrahmen flagge').get('title')
            info['national_team'] = national_team
        except AttributeError:

            logger.exception(f'Сборная не найдена: {url}')

        try:
            status = soup.find(class_='hauptpunkt').text.strip()
            if status == 'окончание':
                info['end_career'] = True
                info['free_agent'] = False
            elif status == 'Без клуба':
                info['end_career'] = False
                info['free_agent'] = True
            else:
                info['end_career'] = False
                info['free_agent'] = False

        except AttributeError:
            logger.exception(f'Не удалось определить статус игрока {url}')

        try:
            rent = soup.find(class_='info-table').find_all('span')
            boll = False
            for i in rent:
                if boll:
                    id = i.find('a').get('href')
                    new_id = id.split('/')[-1]
                    info['rent_from'] = new_id
                    boll = False
                if i.text == 'в аренде из:':
                    boll = True


        except AttributeError:
            logger.exception(f'Не удалось найти из какого клуба пришел {url}')

        try:
            price = soup.find(class_='right-td').text
            price = convert_price(price)
            info['price'] = price[0]
            info['currency'] = price[1]
        except AttributeError:
            info['price'] = ''
            info['currency'] = ''
            logger.exception(f'Стоимость не найдена {url}')

        except ValueError:
            info['price'] = ''
            info['currency'] = ''
            logger.exception(f'Стоимость не найдена {url}')

    except Exception as ex:
        logger.exception(f'ex, {url}')
    time.sleep(randrange(1, 2))
    print(info)

def getMonthByName(s):
    monthes = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
    nStr = s.lower().strip()
    for i in range(len(monthes)):
        if re.match(monthes[i], nStr) != None: return ('0' + str(i + 1))[-2:]  # Если нашли то возвращаем номер месяца в формате 01, 02

    return None

def convert_price(price):
    price = price.split()
    coast = float(price[0].replace(',','.'))
    coast = coast * (1_000_000 if re.match('млн', price[1]) else 1_000)
    currency = price[2]
    return int(coast), currency


parsing_player_info('https://www.transfermarkt.ru/antoine-griezmann/profil/spieler/125781')
# https://www.transfermarkt.ru/antoine-griezmann/profil/spieler/125781
#https://www.transfermarkt.ru/vincent-kompany/profil/spieler/9594
# https://www.transfermarkt.ru/guilherme/profil/spieler/55369
# # https://www.transfermarkt.ru/nicolas-pepe/profil/spieler/343052
# https://www.transfermarkt.ru/sebastian-cristoforo/profil/spieler/188157


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

store = {
    'clubs': {

    },
    'clubs_link': {


    },
    'stadiums': {

    }
}

list_url =[]
stadium_list = []

getFullURL = lambda url: f"https://www.transfermarkt.ru{url}"

def parsing_from_page_club(url):
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    name = soup.find(class_='dataBild').find('img').get('alt')
    logo = soup.find(class_='dataBild').find('img').get('src')
    stadium_name = soup.find_all(class_='dataValue')
    for i in stadium_name:
        try:
            if i.find('a').get('title') == name:
                stadium_url = i.find('a').get('href')
                stadium_name = i.find('a').text
        except Exception as ex:
            print(ex)
    store['clubs'][id]['name'] = name
    store['clubs'][id]['logo'] = logo

    stadium_id = find_or_create_stadium(stadium_name)

    store['stadiums'][stadium_id] = {}
    store['stadiums'][stadium_id]['name'] = stadium_name
    store['stadiums'][stadium_id]['url'] = getFullURL(stadium_url)

    player_url = soup.find_all(class_='di nowrap')
    for i in player_url:
        print(i)

def parsing_player_info(url):
    info  = {}
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    try:
        try:
            photo = soup.find(class_="modal-trigger").find('img').get('src')
            info['photo'] = photo
        except AttributeError:
            err = f'Фото не найдено: {url}'
            print(err)

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
            err = f'Имя не найдено: {url}'
            print(err)


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
            err = f'Дата рождения не найдена: {url}'
            print(err)

        except KeyError:
            info['birthday'] = '1000-01-01'
            err = f'Ошибка ключа: {url}'
            print(err)

        except TypeError:
            info['birthday'] = '1000-01-01'
            err = f'Ошибка типа: {url}'
            print(err)

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
            err = f' {url}'
            print(err)
            info['death_date'] = ''


        try:
            height = soup.find(itemprop="height").text
            height = height.replace(',','.').replace('м','')
            height = float(height)*100
            info['height'] = height

        except AttributeError:
            err = f' {url}'
            print(err)

        try:
            nation = soup.find(class_='info-table').find_all(class_='flaggenrahmen')
            list_nation = []

            for i in nation:
                if not i.get('alt') in list_nation:
                    list_nation.append(i.get('alt'))
            info['nation'] = list_nation
            if len(list_nation) > 2:
                err = f'Подозрительное количество наций {url}'
                print(err)



        except AttributeError:
            info['nation'] = ''
            err = f'Нация не найдена {url}'
            print(err)


        try:
            position = soup.find(class_='detail-position__position').text
            info['position'] = position
        except AttributeError:
            info['position'] = ''
            err = f'Позиция не найдена {url}'
            print(err)

        try:
            national_team = soup.find(class_='flaggenrahmen flagge').get('title')
            info['national_team'] = national_team
        except AttributeError:

            err = f'Сборная не найдена: {url}'
            print(err)

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
            err = f'Не удалось определить статус игрока {url}'
            print(err)

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
            err = f'Не удалось найти из какого клуба пришел {url}'
            print(err)


        try:
            price = soup.find(class_='right-td').text
            price = convert_price(price)
            info['price'] = price[0]
            info['currency'] = price[1]
        except AttributeError:
            info['price'] = ''
            info['currency'] = ''

            err = f'Стоимость не найдена {url}'
            print(err)

        except ValueError:
            info['price'] = ''
            info['currency'] = ''

            err = f'Стоимость не найдена {url}'
            print(err)
    except Exception as ex:
        print(ex, url)
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

def find_or_create_stadium(stadium_name):
    return find_or_create(stadium_list,stadium_name)


def find_or_create(list, name):
    if name not in list:
        list.append(name)

    return list.index(name)+1



parsing_player_info('https://www.transfermarkt.ru/antoine-griezmann/profil/spieler/125781')

# https://www.transfermarkt.ru/antoine-griezmann/profil/spieler/125781
#https://www.transfermarkt.ru/vincent-kompany/profil/spieler/9594
# https://www.transfermarkt.ru/guilherme/profil/spieler/55369
# # https://www.transfermarkt.ru/nicolas-pepe/profil/spieler/343052
# https://www.transfermarkt.ru/sebastian-cristoforo/profil/spieler/188157


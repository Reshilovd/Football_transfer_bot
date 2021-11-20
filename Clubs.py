import requests
from bs4 import BeautifulSoup
import datetime as DT
import re
import time
from random import randrange
import pymysql
import json


headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Mobile Safari/537.36 Edg/95.0.1020.40"
}

# url = 'https://www.transfermarkt.ru/%D0%A3%D0%9F%D0%9B/startseite/wettbewerb/UKR1'

store = {
    'clubs': {

    },
    'clubs_link': {


    },
    'stadiums': {

    },

    'players_link': {

    },

    'players_info': {

    }

}

list_url =[]
stadium_list = []

getFullURL = lambda url: f"https://www.transfermarkt.ru{url}"

def club_init(id):
    return {
        'name': '',
        'logo': '',
    }

def parsing_clubs_id_and_url(url):
    count_clubs = 0
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    clubs = soup.find(class_='items').find_all(class_='hauptlink no-border-links show-for-small show-for-pad')

    for club in clubs:
        link = club.find('a').get('href')
        id = link.split('/')[-3]

        if id != None and id not in store['clubs'].keys():
            count_clubs += 1
            store['clubs_link'][id] = getFullURL(link)
            store['clubs'][id] = club_init(id)

    print(url, ': найдено ', count_clubs, ' клубов')

def parsing_from_page_club(id, url):
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
        try:
            name_player = i.find(class_='show-for-small').find('a').get('title')
            url_player = getFullURL(i.find(class_='show-for-small').find('a').get('href'))
            id_player = url_player.split('/')[-1]
            store['players_link'][id_player] = url_player
        except Exception as ex:
            print(ex)

# def parsing_players_info(list):
#     # id: {'url': link}
#     # вот тут я файл подключал и это получалась локальная переменная и дальше на это ругалось
#     for id in list.keys():
#         players_info[id] = parsing_player_info(list[id])
#         break

def parsing_player_info(id, url):
    store['players_info'][id] = {}
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    try:
        try:
            photo = soup.find(class_="modal-trigger").find('img').get('src')

            store['players_info'][id]['photo'] = photo

        except AttributeError:
            print('take photo  not OK')
            err = f'Фото не найдено: {url}'
            store['players_info'][id]['photo'] = ''
            print(err)

        try:
            name = soup.find(class_='dataName')
            last_name = name.find('b').text
            # first_name = ' '.join(name.find('h1').text.split()[:-1 * len(last_name.split())])
            first_name = ' '.join(filter(lambda x: not x in last_name.split(), name.find('h1').text.split()))
            store['players_info'][id]['first_name'] = first_name
            store['players_info'][id]['last_name'] = last_name
        except IndexError:
            #Если только имя
            store['players_info'][id]['first_name'] = ''
            store['players_info'][id]['last_name'] = ''
        except AttributeError:
            #Если имя вообще нет
            store['players_info'][id]['first_name'] = ''
            store['players_info'][id]['last_name'] = ''

            err = f'Имя не найдено: {url}'
            print(err)

        try:
            birthday = soup.find(class_='dataValue').text.split()
            day = birthday[0]
            month = getMonthByName(birthday[1])
            year = birthday[2]
            date = year + month + day
            date = DT.datetime.strptime(date, '%Y%m%d').date()
            store['players_info'][id]['birthday'] = str(date)
        except AttributeError:
            store['players_info'][id]['birthday'] = '1000-01-01'

            err = f'Дата рождения не найдена: {url}'
            print(err)
        except KeyError:
            store['players_info'][id]['birthday'] = '1000-01-01'

            err = f'Ошибка ключа: {url}'
            print(err)
        except TypeError:
            store['players_info'][id]['birthday'] = '1000-01-01'

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
            store['players_info'][id]['death_date'] = str(date)

        except AttributeError:
            err = f' {url}'
            print(err)
            store['players_info'][id]['death_date'] = ''


        try:
            height = soup.find(itemprop="height").text
            height = height.replace(',','.').replace('м','')
            height = float(height)*100
            store['players_info'][id]['height'] = height

        except AttributeError:
            err = f' {url}'
            store['players_info'][id]['height'] = ''
            print(err)


        try:
            nation = soup.find(class_='info-table').find_all(class_='flaggenrahmen')
            list_nation = []
            for i in nation:
                if not i.get('alt') in list_nation:
                    list_nation.append(i.get('alt'))
            store['players_info'][id]['nation'] = list_nation
            if len(list_nation) > 2:
                err = f'Подозрительное количество наций {url}'
                print(err)

        except AttributeError:
            store['players_info'][id]['nation'] = ''
            err = f'Нация не найдена {url}'
            print(err)


        try:
            position = soup.find(class_='detail-position__position').text
            store['players_info'][id]['position'] = position
        except AttributeError:
            store['players_info'][id]['position'] = ''

            err = f'Позиция не найдена {url}'
            print(err)


        try:
            national_team = soup.find(class_='flaggenrahmen flagge').get('title')
            store['players_info'][id]['national_team'] = national_team

        except AttributeError:
            err = f'Сборная не найдена: {url}'
            print(err)


        try:
            status = soup.find(class_='hauptpunkt').text.strip()
            if status == 'окончание':
                store['players_info'][id]['end_career'] = True
                store['players_info'][id]['free_agent'] = False
            elif status == 'Без клуба':
                store['players_info'][id]['end_career'] = False
                store['players_info'][id]['free_agent'] = True
            else:
                store['players_info'][id]['end_career'] = False
                store['players_info'][id]['free_agent'] = False

        except AttributeError:
            err = f'Не удалось определить статус игрока {url}'
            print(err)
            store['players_info'][id]['end_career'] = ''
            store['players_info'][id]['free_agent'] = ''


        try:
            rent = soup.find(class_='info-table').find_all('span')
            boll = False
            for i in rent:
                if boll:
                    id = i.find('a').get('href')
                    new_id = id.split('/')[-1]
                    store['players_info'][id]['rent_from'] = new_id
                    boll = False
                if i.text == 'в аренде из:':
                    boll = True

        except AttributeError:
            err = f'Не удалось найти из какого клуба пришел {url}'
            print(err)
            store['players_info'][id]['rent_from'] = ''


        try:
            price = soup.find(class_='right-td').text
            price = convert_price(price)

            store['players_info'][id]['price'] = price[0]
            store['players_info'][id]['currency'] = price[1]
        except AttributeError:
            store['players_info'][id]['price'] = ''
            store['players_info'][id]['currency'] = ''

            err = f'Стоимость не найдена {url}'
            print(err)

        except ValueError:
            store['players_info'][id]['price'] = ''
            store['players_info'][id]['currency'] = ''

            err = f'Стоимость не найдена {url}'
            print(err)

    except Exception as ex:
        print(ex, url)
    time.sleep(randrange(1, 2))


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

# def find_or_create_leage(leage_name):
#     return find_or_create(leage_list ,leage_name)
# def decorate(func):
#     def decorated(name):
#         func()

def find_or_create(list, name):
    if name not in list:
        list.append(name)

    return list.index(name)+1

leagues = json.load(open('leagues.json', 'r', encoding='utf-8'))

for elem in leagues[:5]: #собираем id и url клубов со страниц лиг
    url = elem['link']
    parsing_clubs_id_and_url(url)
    break

for id, url in store['clubs_link'].items(): #собираем данные со страниц клубов
    parsing_from_page_club(id, url)
    break

for id, url in store['players_link'].items():
    parsing_player_info(id, url)


json.dump(store, open('clubs.json', 'w', encoding='utf-8'),indent=2,ensure_ascii=False)


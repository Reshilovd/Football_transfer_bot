import re
from constants import *
import datetime
import json
import requests
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar

def get_pagination_leagues(url):
    try:
        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        pagination = soup.find(class_='tm-pagination__list-item tm-pagination__list-item--icon-last-page').find('a').get('href')
        pagination_leagues_number = int(pagination.split('=')[-1])
        return pagination_leagues_number

    except Exception as ex:
        print(ex)

def parsing_leagues(url):
    try:
        list_leagues = []
        # bar = IncrementalBar('Parsing leagues id...', max=len(get_pagination_leagues(url)))
        for pagination in range(1, get_pagination_leagues(url)):
        # for pagination in range(1, 2):
            new_url = f'{url}?page={pagination}'
            req = requests.get(new_url, headers=headers)
            src = req.text
            soup = BeautifulSoup(src, 'lxml')
            leagues_page = soup.find_all(class_='inline-table')
            # bar.next()
            for league in leagues_page:
                id = league.find('tr').contents[-2].find('a').get('href').split('/')[-1]
                link = getFullURL(league.find('tr').contents[-2].find('a').get('href'))
                name = league.find('tr').contents[-2].find('a').get('title')
                # store['leagues'][id] = {}
                # store['leagues'][id]['name'] = name
                # store['leagues'][id]['link'] = link
                list_leagues.append(id)
        # bar.finish()
    except Exception as ex:
        print(ex)

    return list_leagues

def parsing_from_page_club(league_id, club_id, url):
    try:
        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')

        full_name = soup.find(class_='dataBild').find('img').get('alt')
        logo = soup.find(class_='dataBild').find('img').get('src')

        store[league_id][club_id]['full_name'] = full_name
        store[league_id][club_id]['logo'] = logo
        store[league_id][club_id]['url'] = url
        stadium_name, stadium_url = get_stadium_name(soup)
        stadium_id = get_stadium_id(stadium_name)
        store['stadiums'][stadium_id]['name'] = stadium_name
        store['stadiums'][stadium_id]['url'] = getFullURL(stadium_url)
        store['clubs_stadiums']



        player_url = soup.find_all(class_='di nowrap')
        for i in player_url:
            try:
                name_player = i.find(class_='show-for-small').find('a').get('title')
                url_player = getFullURL(i.find(class_='show-for-small').find('a').get('href'))
                id_player = url_player.split('/')[-1]
                store['players_link'][id_player] = url_player
                store['clubs_players'].add((id, id_player, True))
            except Exception as ex:
                print(ex)
        print('success', url)
    except Exception as ex:
        print(ex)

def parsing_player_info(id, url):
    try:
        info = {}
        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        info['photo'] = get_photo(soup, url, id)
        info['first_name'], info['last_name'] = get_name(soup, url, id) or ['', '']
        info['birthday'] = get_birthday(soup, url, id) or '1000-01-01'
        info['death_date'] = get_death_date(soup, url, id)
        info['height'] = get_height(soup, url, id)
        info['end_career'], info['free_agent'] = get_end_career_and_free_agent(soup, url, id) or ['', '']
        info['rent_from'] = get_rent_from(soup, url, id)
        # store['clubs_players'].add((info['rent_from'], id, False))
        info['price'], info['currency'] = get_price_and_currency(soup, url, id) or ['', '']
        for nation in get_nation(soup, url, id): store['nations_players'].add(nation)
        store['positions_players'].add(get_position(soup, url, id))
        store['national_team_players'].add(get_national_team(soup, url, id))
        store['players_info'][id] = info

    except Exception as ex:
        print(ex, url)
    # time.sleep(randrange(1, 2))

def get_date(s):
    s = s.split()
    day = s[0]
    month = getMonthByName(s[1])
    year = s[2]
    date = year + month + day
    date = datetime.datetime.strptime(date, '%Y%m%d').date()
    return str(date)

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

def club_init(id):
    return {
        'name': '',
        'logo': '',
    }

def player_init(id):
    return {
        'name': '',
        'logo': '',
    }

getFullURL = lambda url: f"https://www.transfermarkt.ru{url}"

def logger(func):
    def wrapper(soup, url, id):
        try:
            res = func(soup, url, id)
            return res
        except Exception as ex:
            template = "\n##########################"
            template += "\n" + str(datetime.datetime.now())
            template += "\nURL: " + url
            template += "\nФункция: " + func.__name__
            template += "\nОшибка типа: {0}.\nАргументы: {1}"
            message = template.format(type(ex).__name__, ex.args)
            file = open('log/log.txt', 'a+')
            file.write(message)
            file.close()
            return ""
    return wrapper

@logger
def get_photo(soup, url, id):
    return soup.find(class_="modal-trigger").find('img').get('src')

@logger
def get_name(soup, url, id):
    name = soup.find(class_='dataName')
    last_name = name.find('b').text
    first_name = ' '.join(filter(lambda x: not x in last_name.split(), name.find('h1').text.split()))
    return first_name, last_name

@logger
def get_birthday(soup, url, id):
    # store['players_info'][id]['birthday'] = '1000-01-01'
    birthday = soup.find(class_='dataValue').text.split()
    day = birthday[0]
    month = getMonthByName(birthday[1])
    year = birthday[2]
    date = year + month + day
    date = datetime.datetime.strptime(date, '%Y%m%d').date()
    return str(date)

@logger
def get_death_date(soup, url, id):
    if soup.find(itemprop="deathDate") is not None:
        death_date = soup.find(itemprop="deathDate").text.split()
        del death_date[-1]
        death_date = death_date[0]
        death_date = death_date.split('.')
        day = death_date[0]
        month = death_date[1]
        year = death_date[2]
        date = year + month + day
        date = datetime.datetime.strptime(date, '%Y%m%d').date()
        return str(date)
    else:
        return ''

@logger
def get_height(soup, url, id):
    height = soup.find(itemprop="height").text
    height = height.replace(',', '.').replace('м', '')
    height = float(height) * 100
    return height

@logger
def get_nation(soup, url, id):
    nation_set = set()
    container = soup.find(class_='info-table').find_all('span')
    boll = False
    for i in container:
        if boll:
            nation = i.find_all(class_='flaggenrahmen')
            for j in nation:
                nation_id = get_nation_id(j.get('alt'))
                nation_set.add((nation_id, id))
        if i.text == 'Национальность:':
            boll = True
    return nation_set


def get_nation_id(nation):
    countries = json.load(open('C:\Football_transfer_bot\json\countries.json', 'r'))
    for country in countries:
        if country['name'] == nation:
            return country['id']
    return None


def get_position_id(position_name):
    positions = [
    "Вратарь",
    "Центр. защитник",
    "Левый защитник",
    "Правый защитник",
    "Опорный полузащитник",
    "Центр. полузащитник",
    "Атак. полузащитник",
    "Левый Вингер",
    "Правый Вингер",
    "Центральный нап.",
    "Левый полузащитник",
    "Правый полузащитник",
    "Оттянутый нап."
]
    for index, name in enumerate(positions):
        if positions[name] == position_name:
            return index + 1
    return "Не найдена"

@logger
def get_position(soup, url, id):
    position_name = soup.find(class_='detail-position__position').text
    position_id = get_position_id(position_name)
    # store['positions'][position_id] = position_name
    return position_id, id

@logger
def get_national_team(soup: object, url: object, id: object) -> object:
    national_team = soup.find(class_='flaggenrahmen flagge').get('title')
    national_team_id = get_nation_id(national_team)
    return national_team_id, id

@logger
def get_end_career_and_free_agent(soup, url, id):
    status = soup.find(class_='hauptpunkt').text.strip()
    if status == 'окончание':
        return True, False
    elif status == 'Без клуба':
        return False, True
    else:
        return False, False
        # store['players_info'][id]['end_career'] = False
        # store['players_info'][id]['free_agent'] = False

@logger
def get_rent_from(soup, url, id):
    # store['players_info'][id]['rent_from'] = ''
    rent = soup.find(class_='info-table').find_all('span')
    boll = False
    for i in rent:
        if boll:
            id = i.find('a').get('href')
            new_id = id.split('/')[-1]
            return new_id
            # store['players_info'][id]['rent_from'] = new_id
        if i.text == 'в аренде из:':
            boll = True

@logger
def get_price_and_currency(soup, url, id):
    price = soup.find(class_='right-td').text
    price = convert_price(price)
    return price
    # store['players_info'][id]['price'] = price[0]
    # store['players_info'][id]['currency'] = price[1]


def get_stadium_name(soup):
    dataItems = soup.find_all(class_='dataItem')
    for i in dataItems:
        if i.text == 'Стадион:':
            if i.find_next_sibling().find('a') is not None:
                stadium_name = i.find_next_sibling().find('a').text
                stadium_url = i.find_next_sibling().find('a').get('href')
                return stadium_name, stadium_url
            else:
                return '', ''

def get_stadium_id(stadium_name):
    stadiums_list = []
    file = open('C:\Football_transfer_bot\stadiums_list.txt', 'r', encoding='utf-8')
    while True:
        line = file.readline()
        if line != '':
            stadiums_list.append(line.strip())
        if not line:
            break
    file.close()

    x = False
    for i in stadiums_list:
        if stadium_name == i:
            x = True
            index = stadiums_list.index(stadium_name)
            break
    if x:
        return index + 1
    else:
        stadiums_list.append(stadium_name)
        index = stadiums_list.index(stadium_name)
        file = open('C:\Football_transfer_bot\stadiums_list.txt', 'a', encoding='utf-8')
        file.write(stadium_name)
        file.write('\n')
        file.close()
        return index + 1
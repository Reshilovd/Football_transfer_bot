import re
from constants import *
import datetime



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

def find_or_create(list, name):
    if name not in list:
        list.append(name)

    return list.index(name)+1

def find_or_create_position(position_name):
    return find_or_create(store['positions'], position_name)

def find_or_create_stadium(stadium_name):
    return find_or_create(stadium_list, stadium_name)

def find_or_create_nation(nation):
    return find_or_create(store['nation'], nation)

def find_or_create_national_team(national_team):
    return find_or_create(store['nation'], national_team)

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
            file = open('log.txt', 'a+')
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
                nation_id = find_or_create_nation(j.get('alt'))
                nation_set.add((nation_id, id))
        if i.text == 'Национальность:':
            boll = True
    return nation_set

@logger
def get_position(soup, url, id):
    position_name = soup.find(class_='detail-position__position').text
    position_id = find_or_create_position(position_name)
    # store['positions'][position_id] = position_name
    return position_id, id

@logger
def get_national_team(soup, url, id):
    national_team = soup.find(class_='flaggenrahmen flagge').get('title')
    national_team_id = find_or_create_national_team(national_team)
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


import re
stadium_list = []

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

def club_init(id):
    return {
        'name': '',
        'logo': '',
    }

getFullURL = lambda url: f"https://www.transfermarkt.ru{url}"
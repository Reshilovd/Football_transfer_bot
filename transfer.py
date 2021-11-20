import requests
from bs4 import BeautifulSoup
import datetime as DT
import re


ошибка была, да я поправил

headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Mobile Safari/537.36 Edg/95.0.1020.40"
}
url = 'https://www.transfermarkt.ru/maksim-bordachev/profil/spieler/87262'
players_info = {}

def getMonthByName(s):
    monthes = ['янв', 'фев', 'мар', 'апр', 'мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
    nStr = s.lower().strip()
    for i in range(len(monthes)):
        if re.match(monthes[i], nStr) != None: return ('0' + str(i + 1))[-2:] #Если нашли то возвращаем номер месяца в формате 01, 02

    return None

def parsing_players_info():
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    try:
        name = soup.find(class_='dataName')
        name = name.find('h1').text.split()
        print(name)
        first_name = name[0]
        last_name = name[1]
    except IndexError:
        first_name = name[0]
    except AttributeError:
        print('Имя не найдено')
    try:
        birthday = soup.find(class_='dataValue').text.split()
        print(birthday)
        day = birthday[0]
        month = getMonthByName(birthday[1])
        year = birthday[2]
        date = year + month + day
        date = DT.datetime.strptime(date, '%Y%m%d').date()
        print(date)
    except AttributeError:
        print('Дата рождения не найдена') #тут еще выводи id чтоб потом мог по логам легко найти где была проблема, или вообще ссылку
    except KeyError:
        print('Ошибка ключа')
    try:
        nation = soup.find(class_='flaggenrahmen').get('alt')
        print(nation)
    except AttributeError:
        print('Нация не найдена')
    try:
        position = soup.find(class_='dataDaten').text.split()
        print(position)
    except AttributeError:
        print('Позиция не найдена')

parsing_players_info()

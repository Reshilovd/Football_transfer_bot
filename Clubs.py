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
# def stadium_init(id):
#     return {
#         'name': ''
#     }


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

for key, value in store['clubs_link'].items(): #собираем данные со страниц клубов
    id = key
    url = value
    parsing_from_page_club(url)


json.dump(store, open('clubs.json', 'w', encoding='utf-8'),indent=2,ensure_ascii=False)


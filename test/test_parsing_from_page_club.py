import requests
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar
from random import randrange
import json
from secondary_function import *
from constants import *
import datetime as dt
import time


def get_stadium(url):
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    name = soup.find(class_='dataBild').find('img').get('alt')
    logo = soup.find(class_='dataBild').find('img').get('src')
    dataItems = soup.find_all(class_='dataItem')
    for i in dataItems:
        if i.text == 'Стадион:':
            if i.find_next_sibling().find('a') is not None:
                stadium_name = i.find_next_sibling().find('a').text
                stadium_url = i.find_next_sibling().find('a').get('href')
                return stadium_name, stadium_url
            else:
                return  '', ''


a, b = get_stadium('https://www.transfermarkt.ru/paeek/startseite/verein/21958/saison_id/2021')
print('a:', a, ' b:', b)




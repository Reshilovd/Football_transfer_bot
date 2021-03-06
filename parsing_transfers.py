import requests
from bs4 import BeautifulSoup
import json
from progress.bar import IncrementalBar
import datetime as dt
from constants import *
from secondary_function import getFullURL
from secondary_function import getMonthByName
from secondary_function import get_date
import time

from secondary_function import convert_price
store_transfers = {}

def generate_url(params):
    return f"https://www.transfermarkt.ru/transfers/einnahmenausgaben/statistik/a/ids/a/sa/1/saison_id/{params['saison_id']}/saison_id_bis/{params['saison_id_bis']}/land_id/{params['land_id']}/nat/0/kontinent_id/0/pos//w_s/{params['w_s']}/intern/0/plus/1"

def winter_url(url):
    transfer_url = url.split('/')
    season_id = transfer_url.pop(-1)
    del transfer_url[-1]
    transfer_url = '/'.join(transfer_url)
    winter_transfer_url = transfer_url + f'plus/?saison_id={season_id}&pos=&detailpos=&w_s=w'
    return winter_transfer_url

def summer_url(url):
    transfer_url = url.split('/')
    season_id = transfer_url.pop(-1)
    del transfer_url[-1]
    transfer_url = '/'.join(transfer_url)
    summer_transfer_url = transfer_url + f'plus/?saison_id={season_id}&pos=&detailpos=&w_s=s'
    return summer_transfer_url

def parsing_transfers_url():

    links = []
    lands = ['189']
    seasons = ['2021', '2020']
    # windows = ['w','s']
    for land in lands:
        for season in seasons:
            # for window in windows:
                params = {
                    "saison_id": season,  # 2021
                    "saison_id_bis": season,  # 2021
                    "w_s": "",  # w/s
                    "land_id": land  # 189
                }
                url = generate_url(params)
                req = requests.get(url, headers=headers)
                src = req.text
                soup = BeautifulSoup(src, 'lxml')
                raw_links = soup.find(class_='items').find_all(class_='hauptlink no-border-links')
                for link in raw_links:
                    links.append(winter_url(getFullURL(link.find('a').get('href'))))
                    links.append(summer_url(getFullURL(link.find('a').get('href'))))
    print(f'?? ???????????? {lands} ?????? ????????????(????): {seasons} c???????????? {len(links)} ????????????')
    return links, lands, seasons

def get_info_from_tr(tr):
    td1 = tr.find('td')
    td2 = td1.find_next_sibling()
    td3 = td2.find_next_sibling()
    td4 = td3.find_next_sibling()
    td5 = td4.find_next_sibling()
    td6 = td5.find_next_sibling()
    transfer_id = td6.find('a').get('href').split('/')[-1]
    player_id = td2.find(class_='hauptlink').find('a').get('href').split('/')[-1]
    club_from_id = td5.find('a').get('href').split('/')[-1]
    price_or_rent = td6.find('a').text

    store_transfers[transfer_id] = {}
    store_transfers[transfer_id]['player_id'] = player_id
    store_transfers[transfer_id]['club_from_id'] = club_from_id
    store_transfers[transfer_id]['club_to_id'] = club_to_id

    if price_or_rent[-1] == '???' and price_or_rent[0] != '??':  # '80 ?????? ???'
        store_transfers[transfer_id]['price'] = convert_price(price_or_rent)[0]
        store_transfers[transfer_id]['currency'] = convert_price(price_or_rent)[1]
        store_transfers[transfer_id]['rent'] = False
        store_transfers[transfer_id]['date_end_rent'] = ''

    elif price_or_rent[0] == '??' and price_or_rent[-1] == '???':  # '?????????????????? ????????????:2,00 ?????? ???'
        store_transfers[transfer_id]['price'] = convert_price(price_or_rent.split(':')[1])[0]
        store_transfers[transfer_id]['currency'] = convert_price(price_or_rent.split(':')[1])[1]
        store_transfers[transfer_id]['rent'] = True
        store_transfers[transfer_id]['date_end_rent'] = ''

    elif price_or_rent[0] == '??':
        date_end_rent = price_or_rent.replace('?????????????????? ????????????', '')
        store_transfers[transfer_id]['price'] = ''
        store_transfers[transfer_id]['currency'] = ''
        store_transfers[transfer_id]['rent'] = True
        store_transfers[transfer_id]['date_end_rent'] = get_date(date_end_rent)

    elif price_or_rent == '????????????':
        store_transfers[transfer_id]['price'] = ''
        store_transfers[transfer_id]['currency'] = ''
        store_transfers[transfer_id]['rent'] = True
        store_transfers[transfer_id]['date_end_rent'] = ''

    elif price_or_rent == '?????????????????? ??????????':
        store_transfers[transfer_id]['rent'] = False
        store_transfers[transfer_id]['price'] = ''
        store_transfers[transfer_id]['currency'] = ''
        store_transfers[transfer_id]['date_end_rent'] = ''

    else:
        store_transfers[transfer_id]['price'] = price_or_rent
        store_transfers[transfer_id]['currency'] = ''
        store_transfers[transfer_id]['rent'] = False
        store_transfers[transfer_id]['date_end_rent'] = ''

    store_transfers[transfer_id]['season'] = season
    store_transfers[transfer_id]['window'] = window

def parsing_transfers(url, club_to_id, window, season):

    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    box1 = soup.find(class_='box')
    box2 = box1.find_next_sibling()
    box3 = box2.find_next_sibling()

    if box2.find(class_='responsive-table') is not None:
        tr = box2.find(class_='items').find('tbody').find('tr')
        get_info_from_tr(tr)

        while True:
            tr = tr.find_next_sibling()
            if not tr:
                break
            get_info_from_tr(tr)

file = open('log/log_parsing_transfers.txt', 'a+')
links, lands, seasons = parsing_transfers_url()

bar = IncrementalBar('???????????????? ??????????????????', max=len(links))
for url in links:
    bar.next()
    club_to_id = '' #?????????????????????? ???? ???????????? ???????? ?????????? ?? ?????????????? ?????????? ??????????????????
    raw_club_to_id = url.split('/')[6]
    for i in raw_club_to_id:
        if i.isdigit():
            club_to_id += i

    window = url.split('/')[-1][-1] #?????????????????????? ???? ???????????? ?????????????????????? ????????
    season = int(''.join(i for i in url.split('/')[7] if i.isdigit()))

    try:
        parsing_transfers(url, club_to_id, window, season)

    except Exception as ex:
        message = f'???????????? {ex}, {url}, \n'
        file.write(message)

file.close()

    # print(f'{url} +')
bar.finish()
json.dump(store_transfers, open('json/189_21-20.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
# print(f'?? ???????????? {lands} ?????? ????????????(????): {seasons} c???????????? {len(store_transfers)} ????????????????????')





# 'https://www.transfermarkt.ru/fc-arsenal/transfers/verein/11plus/?saison_id=2021&pos=&detailpos=&w_s=w'
# 'https://www.transfermarkt.ru/fc-arsenal/transfers/verein/11plus/?saison_id=2021&pos=&detailpos=&w_s=s'
# 'https://www.transfermarkt.ru/fc-arsenal/transfers/verein/11plus/?saison_id=2021&pos=&detailpos=&w_s=s'
# 'https://www.transfermarkt.ru/fc-arsenal/transfers/verein/11plus/?saison_id=2021&pos=&detailpos=&w_s=s'
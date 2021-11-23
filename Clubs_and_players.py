import requests
from bs4 import BeautifulSoup
from progress.bar import IncrementalBar
from random import randrange
import json
from secondary_function import *
from constants import *
import datetime as dt
import time

class MyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, set):
            return list(o)
        return o
            

def parsing_clubs_id_and_url(url, league_id):
    time_start = dt.datetime.now()
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
            store['clubs'][id]['league_id'] = league_id
            store['leagues_clubs'].add((league_id, id))
    time_end = dt.datetime.now()
    print(url, ': найдено ', count_clubs, ' клубов за ', str(time_end - time_start))

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
            pass
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
            store['clubs_players'].add((id, id_player))
        except Exception as ex:
            pass

def parsing_player_info(id, url):
    try:
        store['players_info'][id] = {}
        req = requests.get(url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')

        get_photo(soup, url, id)
        get_name(soup, url, id)
        get_birthday(soup, url, id)
        get_death_date(soup, url, id)
        get_height(soup, url, id)
        get_nation(soup, url, id)
        get_position(soup, url, id)
        get_nation_team(soup, url, id)
        get_end_career_and_free_agent(soup, url, id)
        get_rent_from(soup, url, id)
        get_price_and_currency(soup, url, id)

    except Exception as ex:
        print(ex, url)
    time.sleep(randrange(1, 2))

def main():
    time_start = dt.datetime.now()
    leagues = json.load(open('leagues.json', 'r', encoding='utf-8'))

    for elem in leagues[:5]: #собираем id и url клубов со страниц лиг
        url = elem['link']
        league_id = elem['key']
        parsing_clubs_id_and_url(url, league_id)
        break
    time_start_players = dt.datetime.now()
    for id, url in store['clubs_link'].items(): #собираем данные со страниц клубов
        parsing_from_page_club(id, url)
        break
    print('Найдено ', len(store['players_link']), ' игроков за ', str(dt.datetime.now() - time_start_players))

    bar = IncrementalBar('Parsing players', max=len(store['players_link']))

    for id, url in store['players_link'].items():
        parsing_player_info(id, url)
        break
        bar.next()

    bar.finish()
    time_finish = dt.datetime.now()
    print(str(time_finish-time_start))


    json.dump(store, open('clubs_and_players.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False, cls=MyEncoder)

main()
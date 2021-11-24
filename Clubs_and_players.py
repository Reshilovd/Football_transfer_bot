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
            # store['clubs'][id]['league_id'] = league_id
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
    store['stadium_clubs'].add((stadium_id, id))

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
        info['price'], info['currency'] = get_price_and_currency(soup, url, id) or ['', '']
        for nation in get_nation(soup, url, id): store['nations_players'].add(nation)
        store['positions_players'].add(get_position(soup, url, id))
        store['national_team_players'].add(get_national_team(soup, url, id))
        store['players_info'][id] = info

    except Exception as ex:
        print(ex, url)
    # time.sleep(randrange(1, 2))

def main():
    time_start = dt.datetime.now()
    leagues = json.load(open('leagues.json', 'r', encoding='utf-8'))

    for elem in leagues[:1]: #собираем id и url клубов со страниц лиг
        url = elem['link']
        league_id = elem['key']
        league_name = elem['name']
        league_logo = elem['src']
        store['leagues'][league_id] = {}
        store['leagues'][league_id]['league_name'] = league_name
        store['leagues'][league_id]['logo'] = league_logo
        parsing_clubs_id_and_url(url, league_id)

    time_start_players = dt.datetime.now()
    bar = IncrementalBar('Parsing clubs', max=len(store['clubs_link']))
    for id, url in store['clubs_link'].items(): #собираем данные со страниц клубов
        parsing_from_page_club(id, url)
        bar.next()

    bar.finish()
    print('Найдено ', len(store['players_link']), ' игроков за ', str(dt.datetime.now() - time_start_players))

    bar = IncrementalBar('Parsing players', max=len(store['players_link']))

    # c = 0
    for id, url in store['players_link'].items():
        parsing_player_info(id, url)
        # c += 1
        bar.next()

        # if c == 50: break

    bar.finish()
    time_finish = dt.datetime.now()
    print('Собрано ', len(store['players_link']), ' игроков за ', str(time_finish-time_start))


    json.dump(store, open('store.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False, cls=MyEncoder)

main()
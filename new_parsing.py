import requests
from bs4 import BeautifulSoup
from constants import headers
from constants import store
import json
from secondary_function import get_pagination_leagues
from secondary_function import parsing_leagues
from secondary_function import getFullURL
from secondary_function import get_stadium_name
from secondary_function import get_stadium_id
from secondary_function import parsing_from_page_club
from secondary_function import parsing_player_info
from progress.bar import IncrementalBar

leagues_id = parsing_leagues('https://www.transfermarkt.ru/wettbewerbe/europa')
bar = IncrementalBar('Parsing leagues...', max=len(leagues_id))

for league_id in leagues_id:
    url = f'https://www.transfermarkt.ru/home/competition/{league_id}'
    req = requests.get(url, headers=headers)
    src = req.text
    data = json.loads(src)
    if len(data['grids']) == 0:
        print(f'Это не лига, клубов нет - {league_id}')
        continue
    clubs = data['grids'][0]["entries"]
    clubs = data['grids'][0]["entries"]

    bar.next()
    for club in clubs:
        short_name = club['team']['name']
        icon = club['team']['icon']
        club_id = club['team']['id']
        url = club['team']['url']
        url = getFullURL(url)
        position = club['position']
        matches = club['matches']
        diff = club['diff']
        points = club['points']
        is_playing = club['isPlaying']
        marking = club['marking']
        trend = club['trend']

        store['leagues'][club_id] = {}
        store[league_id][club_id]['icon'] = icon
        store[league_id][club_id]['short_name'] = short_name

        parsing_from_page_club(league_id, club_id, url)

    print(f' Лига {league_id} ОК')
    break
bar.finish()
print(store)
json.dump(store, open('store_clubs.json', 'w', encoding='utf-8'), indent=4)
for id, url in store['players_link'].items():
    parsing_player_info(id, url)











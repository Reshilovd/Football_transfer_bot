import json
import requests
from bs4 import BeautifulSoup
from constants import headers
from parsing_transfers import get_info_from_tr


url = 'https://www.transfermarkt.ru/neftekhimik-nizhnekamsk/transfers/verein/3733plus/?saison_id=2018&pos=&detailpos=&w_s=s'
# https://www.transfermarkt.ru/quickselect/players/131
# https://www.transfermarkt.ru/quickselect/countries
req = requests.get(url, headers=headers)
src = req.text
soup = BeautifulSoup(src, 'lxml')
print(soup)
box1 = soup.find(class_='box')
box2 = box1.find_next_sibling()
box3 = box2.find_next_sibling()
#
# if box2.find(class_='responsive-table') is not None:
#     tr = box2.find(class_='items').find('tbody').find('tr')
#     get_info_from_tr(tr)
#     print(tr)
#
#
#     while True:
#         tr = tr.find_next_sibling()
#         if not tr:
#             break
#         get_info_from_tr(tr)

# with open('countries.json', 'w') as file:
#     json.dump(req.json(), file, indent=4, ensure_ascii=False)


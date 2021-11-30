import requests
from bs4 import BeautifulSoup
from constants import *
from secondary_function import getFullURL

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
            links = []
            for link in raw_links:
                links.append(winter_url(getFullURL(link.find('a').get('href'))))
                links.append(summer_url((getFullURL(link.find('a').get('href')))))

print(links)
for url in links:
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    transfers = soup.find(class_='items').find_all(class_='inline-table')
    for transfer in transfers:

        print(transfer.find('img'))


import requests
from bs4 import BeautifulSoup
import datetime as DT
import re
import time
from random import randrange
import pymysql


headers = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Mobile Safari/537.36 Edg/95.0.1020.40"
}

# url = 'https://www.transfermarkt.ru/aleksandr-maksimenko/profil/spieler/351419'

list_url = ['https://www.transfermarkt.ru/%D0%A3%D0%9F%D0%9B/startseite/wettbewerb/UKR1']
            # 'https://www.transfermarkt.ru/%D0%A3%D0%9F%D0%9B/startseite/wettbewerb/UKR1',
            # 'https://www.transfermarkt.ru/1-division/startseite/wettbewerb/RU2',
            # 'https://www.transfermarkt.ru/premier-league/startseite/wettbewerb/GB1',
            # 'https://www.transfermarkt.ru/la-liga/startseite/wettbewerb/ES1',
            # 'https://www.transfermarkt.ru/serie-a/startseite/wettbewerb/IT1',
            # 'https://www.transfermarkt.ru/1-bundesliga/startseite/wettbewerb/L1',
            # 'https://www.transfermarkt.ru/ligue-1/startseite/wettbewerb/FR1'

clubs_link = {} #Ссылки на клубы
players_link = {} #Ссылки на игроков id: {'url': link}
players_info = {} #Инфо игроков

def parsing_club():
    count_clubs = 0
    for i in range(len(list_url)):
        req = requests.get(list_url[i], headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        clubs = soup.find(class_='items').find_all(class_='hauptlink no-border-links show-for-small show-for-pad')
        print(clubs)
        print(len(clubs))
        for j in clubs:

            print(j)

            if id != None and id not in clubs_link.keys():
                count_clubs += 1
                clubs_link[id] = {'url': getFullURL(j.get('href')), 'name': j.text}
        print(f"Собрано {count_clubs} клубов")
        time.sleep(randrange(1,3))


def parsing_players():
    for i in clubs_link.keys():
        req = requests.get(clubs_link[i]['url'], headers=headers)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')

        players = soup.find(class_='items')
        if players == None: continue
        players = players.find_all(class_='spielprofil_tooltip')
        count_players = 0

        for j in players:
            id = j.get('id')
            if id != None and id not in players_link.keys():
                count_players += 1
                players_link[id] = {'url': getFullURL(j.get('href')), 'club_id': i}
        print(f"Для {clubs_link[i]['name']} собрано {count_players} игроков.")
        time.sleep(randrange(1, 3))
        break

def parsing_players_info(list):
    # id: {'url': link}
    # вот тут я файл подключал и это получалась локальная переменная и дальше на это ругалось
    for id in list.keys():
        players_info[id] = parsing_player_info(list[id])
        break

    file.close()

def parsing_player_info(data):
    info = {'club_id': data['club_id']}
    url = data['url']
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, 'lxml')
    try:
        try:
            photo = soup.find(rel="preload").get('href')
            info['photo'] = photo
        except AttributeError:
            err = f'Фото не найдено: {url}'
            info['photo'] = ''
            print(err)
            file.write(err + '\n')

        try:
            name = soup.find(class_='dataName')
            last_name = name.find('b').text
            # first_name = ' '.join(name.find('h1').text.split()[:-1 * len(last_name.split())])
            first_name = ' '.join(filter(lambda x: not x in last_name.split(), name.find('h1').text.split()))
            info['first_name'] = first_name
            info['last_name'] = last_name
        except IndexError:
            #Если только имя
            info['first_name'] = name[0]
            info['last_name'] = ''
        except AttributeError:
            #Если имя вообще нет
            info['first_name'] = ''
            info['last_name'] = ''

            err = f'Имя не найдено: {url}'
            print(err)
            file.write(err + '\n')

        try:
            birthday = soup.find(class_='dataValue').text.split()
            day = birthday[0]
            month = getMonthByName(birthday[1])
            year = birthday[2]
            date = year + month + day
            date = DT.datetime.strptime(date, '%Y%m%d').date()
            info['birthday'] = str(date)
        except AttributeError:
            info['birthday'] = '1000-01-01'

            err = f'Дата рождения не найдена: {url}'
            print(err)
            file.write(err + '\n')
        except KeyError:
            info['birthday'] = '1000-01-01'

            err = f'Ошибка ключа: {url}'
            print(err)
            file.write(err + '\n')
        except TypeError:
            info['birthday'] = '1000-01-01'

            err = f'Ошибка типа: {url}'
            print(err)
            file.write(err + '\n')

        try:
            death_date = soup.find(itemprop="deathDate").text.split()
            del death_date[-1]
            death_date = death_date[0]
            death_date = death_date.split('.')
            day = death_date[0]
            month = death_date[1]
            year = death_date[2]
            date = year + month + day
            date = DT.datetime.strptime(date, '%Y%m%d').date()
            info['death_date'] = str(date)

        except AttributeError:
            err = f' {url}'
            print(err)
            info['death_date'] = ''
            file.write(err + '\n')

        try:
            height = soup.find(itemprop="height").text
            height = height.replace(',','.').replace('м','')
            height = float(height)*100
            info['height'] = height

        except AttributeError:
            err = f' {url}'
            info['height'] = ''
            print(err)
            file.write(err + '\n')

        try:
            nation = soup.find(class_='info-table').find_all(class_='flaggenrahmen')
            list_nation = []
            for i in nation:
                if not i.get('alt') in list_nation:
                    list_nation.append(i.get('alt'))
            info['nation'] = list_nation
            if len(list_nation) > 2:
                err = f'Подозрительное количество наций {url}'
                print(err)

        except AttributeError:
            info['nation'] = ''
            err = f'Нация не найдена {url}'
            print(err)
            file.write(err + '\n')

        try:
            position = soup.find(class_='detail-position__position').text
            info['position'] = position
        except AttributeError:
            info['position'] = ''

            err = f'Позиция не найдена {url}'
            print(err)
            file.write(err + '\n')

        try:
            national_team = soup.find(class_='flaggenrahmen flagge').get('title')
            info['national_team'] = national_team

        except AttributeError:
            err = f'Сборная не найдена: {url}'
            print(err)
            file.write(err + '\n')

        try:
            status = soup.find(class_='hauptpunkt').text.strip()
            if status == 'окончание':
                info['end_career'] = True
                info['free_agent'] = False
            elif status == 'Без клуба':
                info['end_career'] = False
                info['free_agent'] = True
            else:
                info['end_career'] = False
                info['free_agent'] = False

        except AttributeError:
            err = f'Не удалось определить статус игрока {url}'
            print(err)
            info['end_career'] = ''
            info['free_agent'] = ''
            file.write(err + '\n')

        try:
            rent = soup.find(class_='info-table').find_all('span')
            boll = False
            for i in rent:
                if boll:
                    id = i.find('a').get('href')
                    new_id = id.split('/')[-1]
                    info['rent_from'] = new_id
                    boll = False
                if i.text == 'в аренде из:':
                    boll = True

        except AttributeError:
            err = f'Не удалось найти из какого клуба пришел {url}'
            print(err)
            info['rent_from'] = ''
            file.write(err + '\n')

        try:
            price = soup.find(class_='right-td').text
            price = convert_price(price)

            info['price'] = price[0]
            info['currency'] = price[1]
        except AttributeError:
            info['price'] = ''
            info['currency'] = ''

            err = f'Стоимость не найдена {url}'
            print(err)
            file.write(err + '\n')
        except ValueError:
            info['price'] = ''
            info['currency'] = ''

            err = f'Стоимость не найдена {url}'
            print(err)
            file.write(err + '\n')
    except Exception as ex:
        print(ex, url)
        file.write(ex +":" + url + '\n')
    time.sleep(randrange(1, 2))

    return info

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

getFullURL = lambda url: f"https://www.transfermarkt.ru{url}"

file = open('text.txt', 'w')
parsing_club()
parsing_players()
parsing_players_info(players_link)
print(players_info)

try:
    connection = pymysql.connect(host='141.8.192.193',
                                user='a0595563',
                                password='kaifamumig',
                                db='a0595563_Transfer',
                                cursorclass=pymysql.cursors.DictCursor)
    print('Success!')
    try:
        for key in players_info:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `players` (`id`, `first_name`, `last_name`, `birthday`, `position`, `nation`, `club_id`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (key, players_info[key]['first_name'],players_info[key]['last_name'],players_info[key]['birthday'],players_info[key]['position'],players_info[key]['nation'],players_info[key]['club_id']))
                print('Запись добавлена')
                connection.commit()

    finally:
        connection.close()

except Exception as ex:
    print(ex)
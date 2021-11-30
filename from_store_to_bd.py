import pymysql
import json
import datetime as dt

store = json.load(open('store.json', 'r', encoding='utf-8'))
print(type(store))
leagues = json.load(open('leagues.json', 'r', encoding='utf-8'))


def from_store_to_table_players():
    try:
        connection = pymysql.connect(host='141.8.192.193',
                                     user='a0595563',
                                     password='kaifamumig',
                                     db='a0595563_Transfer',
                                     cursorclass=pymysql.cursors.DictCursor)
        print('Success!')


        try:
            for id in store['players_info']:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `players` (`id`, `photo`, `first_name`, `last_name`, `birthday`, `death_date`, `height`, `end_career`, `free_agent`, `price`, `currency`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (id, store['players_info'][id]['photo'], store['players_info'][id]['first_name'], store['players_info'][id]['last_name'], store['players_info'][id]['birthday'], store['players_info'][id]['death_date'], store['players_info'][id]['height'], store['players_info'][id]['end_career'], store['players_info'][id]['free_agent'], store['players_info'][id]['price'], store['players_info'][id]['currency']))
                    print(f'Игрок с ID: {id} добавлен')
                    connection.commit()

        finally:
            connection.close()

    except Exception as ex:
        print(ex)

def from_store_to_table_clubs():
    try:
        connection = pymysql.connect(host='141.8.192.193',
                                     user='a0595563',
                                     password='kaifamumig',
                                     db='a0595563_Transfer',
                                     cursorclass=pymysql.cursors.DictCursor)
        print('Success!')


        try:
            for id in store['clubs']:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `clubs` (`id`, `name`, `logo`) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (int(id), store['clubs'][id]['name'], store['clubs'][id]['logo']))
                    print(f'Клуб с ID: {id} добавлен')
                    connection.commit()
        finally:
            connection.close()

    except Exception as ex:
        print(ex)

def from_store_to_table_clubs_players():
    try:
        connection = pymysql.connect(host='141.8.192.193',
                                     user='a0595563',
                                     password='kaifamumig',
                                     db='a0595563_Transfer',
                                     cursorclass=pymysql.cursors.DictCursor)
        print('Success!')


        try:
            for i in store['clubs_players']:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `clubs_players` (`club_id`, `player_id`, `current`) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (i[0], i[1], i[2]))
                    print(f'Связь клуба ID: {i[0]} c игроком ID: {i[1]}  добавлена')
                    connection.commit()
        finally:
            connection.close()

    except Exception as ex:
        print(ex)

def from_store_to_table_leagues_clubs():
    try:
        connection = pymysql.connect(host='141.8.192.193',
                                     user='a0595563',
                                     password='kaifamumig',
                                     db='a0595563_Transfer',
                                     cursorclass=pymysql.cursors.DictCursor)
        print('Success!')


        try:
            for league_id in store['leagues_clubs']:
                print(league_id)
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `leagues_clubs` (`league_id`, `club_id`) VALUES (%s, %s)"
                    cursor.execute(sql, (league_id[0], league_id[1]))
                    print(f'Связь лиги ID: {league_id[0]} c клубом ID: {league_id[1]}  добавлена')
                    connection.commit()
        finally:
            connection.close()

    except Exception as ex:
        print(ex)

def from_store_to_table_leagues():
    try:
        connection = pymysql.connect(host='141.8.192.193',
                                     user='a0595563',
                                     password='kaifamumig',
                                     db='a0595563_Transfer',
                                     cursorclass=pymysql.cursors.DictCursor)
        print('Success!')


        try:
            for league_id in store['leagues']:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `leagues` (`id`, `name`, `logo`) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (league_id, store['leagues'][league_id]['name'], store['leagues'][league_id]['logo']))
                    print(f'Лига ID: {league_id}  добавлена')
                    connection.commit()
        finally:
            connection.close()

    except Exception as ex:
        print(ex)

def from_store_to_table_stadiums():
    try:
        connection = pymysql.connect(host='141.8.192.193',
                                     user='a0595563',
                                     password='kaifamumig',
                                     db='a0595563_Transfer',
                                     cursorclass=pymysql.cursors.DictCursor)
        print('Success!')


        try:
            for stadium_id in store['stadiums']:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `stadiums` (`id`, `name`) VALUES (%s, %s)"
                    cursor.execute(sql, (stadium_id, store['stadiums'][stadium_id]['name']))
                    print(f'Стадион ID: {stadium_id}  добавлен')
                    connection.commit()
        finally:
            connection.close()

    except Exception as ex:
        print(ex)

def from_store_to_table_stadiums_clubs():
    try:
        connection = pymysql.connect(host='141.8.192.193',
                                     user='a0595563',
                                     password='kaifamumig',
                                     db='a0595563_Transfer',
                                     cursorclass=pymysql.cursors.DictCursor)
        print('Success!')


        try:
            for i in store['stadium_clubs']:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `stadiums_clubs` (`stadium_id`, `club_id`) VALUES (%s, %s)"
                    cursor.execute(sql, (i[0], i[1]))
                    print(f'Связь стадиона ID: {i[0]} c клубом ID: {i[1]}  добавлена')
                    connection.commit()
        finally:
            connection.close()

    except Exception as ex:
        print(ex)

def from_store_to_table_positions():
    try:
        connection = pymysql.connect(host='141.8.192.193',
                                     user='a0595563',
                                     password='kaifamumig',
                                     db='a0595563_Transfer',
                                     cursorclass=pymysql.cursors.DictCursor)
        print('Success!')

        try:
            for i in store['positions']:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `positions` (`id`, `name`) VALUES (%s, %s)"
                    cursor.execute(sql, (store['positions'].index(i)+1, i))
                    print(f"Позиция ID: {store['positions'].index(i)+1}  добавлена")
                    connection.commit()
        finally:
            connection.close()

    except Exception as ex:
        print(ex)

def from_store_to_table_positions_players():
    try:
        connection = pymysql.connect(host='141.8.192.193',
                                     user='a0595563',
                                     password='kaifamumig',
                                     db='a0595563_Transfer',
                                     cursorclass=pymysql.cursors.DictCursor)
        print('Success!')


        try:
            for i in store['positions_players']:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `positions_players` (`position_id`, `player_id`) VALUES (%s, %s)"
                    cursor.execute(sql, (i[0], i[1]))
                    print(f'Связь позиции ID: {i[0]} c игроком ID: {i[1]}  добавлена')
                    connection.commit()
        finally:
            connection.close()

    except Exception as ex:
        print(ex)

def from_store_to_table_nations():
    try:
        connection = pymysql.connect(host='141.8.192.193',
                                     user='a0595563',
                                     password='kaifamumig',
                                     db='a0595563_Transfer',
                                     cursorclass=pymysql.cursors.DictCursor)
        print('Success!')

        try:
            for i in store['nation']:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `nations` (`id`, `name`) VALUES (%s, %s)"
                    cursor.execute(sql, (store['nation'].index(i)+1, i))
                    print(f"Нация ID: {store['nation'].index(i)+1}  добавлена")
                    connection.commit()
        finally:
            connection.close()

    except Exception as ex:
        print(ex)

def from_store_to_table_national_team_players():
    try:
        connection = pymysql.connect(host='141.8.192.193',
                                     user='a0595563',
                                     password='kaifamumig',
                                     db='a0595563_Transfer',
                                     cursorclass=pymysql.cursors.DictCursor)
        print('Success!')


        try:
            for i in store['national_team_players']:
                if i != '':
                    with connection.cursor() as cursor:
                        sql = "INSERT INTO `national_team_players` (`national_team_id`, `player_id`) VALUES (%s, %s)"
                        cursor.execute(sql, (i[0], i[1]))
                        print(f'Связь национальной команды ID: {i[0]} c игроком ID: {i[1]}  добавлена')
                        connection.commit()
        finally:
            connection.close()

    except Exception as ex:
        print(ex)

def from_store_to_table_nations_players():
    try:
        connection = pymysql.connect(host='141.8.192.193',
                                     user='a0595563',
                                     password='kaifamumig',
                                     db='a0595563_Transfer',
                                     cursorclass=pymysql.cursors.DictCursor)
        print('Success!')


        try:
            for i in store['nations_players']:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `nations_players` (`nation_id`, `player_id`) VALUES (%s, %s)"
                    cursor.execute(sql, (i[0], i[1]))
                    print(f'Связь нации ID: {i[0]} c игроком ID: {i[1]}  добавлена')
                    connection.commit()
        finally:
            connection.close()

    except Exception as ex:
        print(ex)

def main():
    time_start = dt.datetime.now()
    from_store_to_table_players()
    from_store_to_table_clubs()
    from_store_to_table_clubs_players()
    from_store_to_table_leagues_clubs()
    from_store_to_table_leagues()
    from_store_to_table_stadiums()
    from_store_to_table_stadiums_clubs()
    from_store_to_table_positions()
    from_store_to_table_positions_players()
    from_store_to_table_nations()
    from_store_to_table_national_team_players()
    from_store_to_table_nations_players()
    time_finish = dt.datetime.now()
    print('Загружено в базу данных ', len(store['players_link']), ' игроков за ', str(time_finish - time_start))

main()

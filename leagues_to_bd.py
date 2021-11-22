import pymysql
import json
store = json.load(open('clubs_and_players.json', 'r', encoding='utf-8'))
print(type(store))
leagues = json.load(open('leagues.json', 'r', encoding='utf-8'))


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
                print(f'{id} ОК')
                connection.commit()
        for id in store['clubs']:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `clubs` (`id`, `club_name`,`league_id`) VALUES (%s, %s, %s )"
                cursor.execute(sql, (id, ))
                print(f'{id} ОК')
                connection.commit()

    finally:
        connection.close()

except Exception as ex:
    print(ex)

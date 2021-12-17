import pymysql
import json
import datetime as dt

store = json.load(open('json/189_21-20.json', 'r', encoding='utf-8'))


def from_store_to_table_transfers():
    try:
        connection = pymysql.connect(host='141.8.192.193',
                                     user='a0595563',
                                     password='kaifamumig',
                                     db='a0595563_Transfer',
                                     cursorclass=pymysql.cursors.DictCursor)
        print('Success!')


        try:
            for id in store.keys():
                with connection.cursor() as cursor:
                    sql = "INSERT INTO `transfers` (`id`, `player_id`, `from_club_id`, `to_club_id`, `rent`, `date_end_rent`, `season`, `window`, `price`, `currency`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(sql, (id, store[id]['player_id'], store[id]['club_from_id'], store[id]['club_to_id'], store[id]['rent'], store[id]['date_end_rent'], store[id]['season'], store[id]['window'], store[id]['price'], store[id]['currency']))
                    print(f'Трансфер с ID: {id} добавлен')
                    connection.commit()

        finally:
            connection.close()

    except Exception as ex:
        print(ex)

from_store_to_table_transfers()

import pymysql

dict = {
    '86269': {
        'first_name': 'Aleksandr',
        'last_name': 'Gutor',
        'birthday': '1989-04-18',
        'nation': 'СССР',
        'position': 'Вратарь',
        'club_id' : '1'
    },
    '129561': {
        'first_name': 'Sergey',
        'last_name': 'Chernik',
        'birthday': '1988-07-20',
        'nation': 'СССР',
        'position': 'Вратарь',
        'club_id' : '1'

    },
    '176142': {
        'first_name': 'Konstantin',
        'last_name': 'Rudenok',
        'birthday': '1990-12-15',
        'nation': 'СССР',
        'position': 'Вратарь',
        'club_id' : '1'}
}



try:
    connection = pymysql.connect(host='141.8.192.193',
                                user='a0595563',
                                password='kaifamumig',
                                db='a0595563_Transfer',
                                cursorclass=pymysql.cursors.DictCursor)
    print('Success!')


    try:
        for key in dict:
            with connection.cursor() as cursor:
                sql = "INSERT INTO `players` (`id`, `first_name`, `last_name`, `birthday`, `position`, `nation`, `club_id`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (key, dict[key]['first_name'],dict[key]['last_name'],dict[key]['birthday'],dict[key]['position'],dict[key]['nation'],dict[key]['club_id']))
                connection.commit()


    finally:
        connection.close()

except Exception as ex:
    print(ex)

for key in dict:
    print(key, dict[key]['first_name'])

import pymysql
import json
import datetime as dt



def select_leagues_url():
    data = []
    try:
        connection = pymysql.connect(host='141.8.192.193',
                                     user='a0595563',
                                     password='kaifamumig',
                                     db='a0595563_Transfer',
                                     cursorclass=pymysql.cursors.DictCursor)
        print('Success!')

        try:
            with connection.cursor() as cursor:
                sql = "SELECT url FROM leagues_url"
                cursor.execute(sql, data)
                data = cursor.fetchall()

        finally:
            connection.close()
        return data

    except Exception as ex:
        print(ex)

urls = select_leagues_url()
print(urls)
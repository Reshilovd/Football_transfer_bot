import json

#data  = json.dumps(name,ensure_ascii=True по умолчанию, если нужна кириллица то False
#                   indent = 2 - отступы
#                   sort_keys = True


# data = [{
#     'src': 'https://tmssl.akamaized.net/images/logo/small/gb1.png?lm=1521104656',
#     'name': 'Премьер-Лига',
#     'link': 'https://www.transfermarkt.ru/%D0%9F%D1%80%D0%B5%D0%BC%D1%8C%D0%B5%D1%80-%D0%9B%D0%B8%D0%B3%D0%B0/startseite/wettbewerb/GB1'
# }, {
#     'src': 'https://tmssl.akamaized.net/images/logo/small/es1.png?lm=1557051003',
#     'name': 'ЛаЛига',
#     'link': 'https://www.transfermarkt.ru/%D0%9B%D0%B0%D0%9B%D0%B8%D0%B3%D0%B0/startseite/wettbewerb/ES1'
# }, {
#     'src': 'https://tmssl.akamaized.net/images/logo/small/it1.png?lm=1632134907',
#     'name': 'Серия А',
#     'link': 'https://www.transfermarkt.ru/%D0%A1%D0%B5%D1%80%D0%B8%D1%8F-%D0%90/startseite/wettbewerb/IT1'}]
#
# json_str = json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)  #из py_obj в json_str
#
# py_obj = json.loads(json_str)  #из json_str в py_obj
#
# json.dump(json_str, open('../test_json', 'w', encoding='utf-8')) #запись в файл
#
# data2 = json.load(open('../test_json', 'r', encoding='utf-8')) #загрузка из файла
# data2 = json.loads(data2)
# print(type(data2))
# data2 = json.loads(data2)
# for i in data2:
#     print(i['link'])


def get_stadium_id(stadium_name):
    stadiums_list = []
    file = open('C:\Football_transfer_bot\stadiums_list.txt', 'r', encoding='utf-8')
    while True:
        line = file.readline()
        if line != '':
            stadiums_list.append(line.strip())
        if not line:
            break
    file.close()

    x = False
    for i in stadiums_list:
        if stadium_name == i:
            x = True
            index = stadiums_list.index(stadium_name)

    if x:
        return index
    else:
        stadiums_list.append(stadium_name)
        index = stadiums_list.index(stadium_name)
        file = open('C:\Football_transfer_bot\stadiums_list.txt', 'a', encoding='utf-8')
        file.write(stadium_name)
        file.write('\n')
        file.close()
        return index

print(get_stadium_id("Tor Stadtgrtgbgbggrgrium"))


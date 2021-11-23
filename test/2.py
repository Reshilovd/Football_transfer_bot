def logger(url):
    def decorate(func):
        def wrapper(*args):
            print(args[1])
            try:
                func(args)
            except Exception as ex:
                template = "##########################"
                template += "\nURL: " + url
                template += "\nФункция: " + func.__name__
                template += "\nОшибка типа: {0}.\nАргументы: {1}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
        return wrapper
    return decorate


@logger('http')
def find(obj, a, s):
    return obj['name']

find('afeagew', 'asd', 'as')


def logger(id):
    def decorate(func):
        def wrapper(soup):

            func(soup)
            print('Декоратор работает')

            print('take photo  not OK')
            err = f'Фото не найдено: {url}'
            store['players_info'][id]['photo'] = ''
            print(err)
        return wrapper
    return decorate



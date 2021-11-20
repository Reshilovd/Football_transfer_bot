def logger(url):
    def decorate(func):
        def wrapper(obj):
            try:
                func(obj)

            except Exception as ex:
                print(ex)
                print('ВСЕ ОК')
                print(url)

        return wrapper
    return decorate


@logger('http')
def find(obj):
    return obj['name']

find('afeagew')



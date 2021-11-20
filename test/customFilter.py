def myFilter( callback, arr):
    newArr = []
    for el in arr:
        b = callback(el)

        if b: newArr.append(el)

    return newArr


a = [1,2,3,4]

def forFilt(x):
    return x > 2

res = myFilter(forFilt, a)

print(list(res))

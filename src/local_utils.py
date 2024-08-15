import datetime

"""
Split string by space
"""
def splitdata(data):
    array = data.split(" ")
    return array

"""
Count arguments
"""
def countarray(array):
    return len(array)


"""
Logg command
"""
def logger(function):
    def wrapper(*args, **kwargs):
        data = function()
        print(str(datetime.datetime.now()), " ", data)
        return data
    return wrapper

"""
Get input
"""
@logger
def get_input():
    data = input()
    return data



import datetime
import random


def time_to_str(timestamp, time_format="%Y-%m-%d %H:%M:%S.%f"):
    """get datetime string from timestamp
    """
    d = datetime.datetime.fromtimestamp(timestamp)
    time_str = d.strftime(time_format)
    return time_str


def random_number_str(length=20):
    """generate a random number string
    """
    return ''.join([str(random.randint(0, 9)) for i in range(length)])


def timestamp_str():
    """get timestamp
    """
    return str(int(datetime.datetime.now().timestamp()*1000))

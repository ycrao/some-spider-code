import datetime
import random
import os
import csv


def write_csv(path, row=None, head=None):
    """
    创建或更新一个 csv 文件，创建时可附带表头或行数据信息，更新时可附带行数据
    """
    if not os.path.exists(path):
        with open(path, "w") as f:
            writer = csv.writer(f)
            if head is not None:
                writer.writerow(head)
            if row is not None:
                writer.writerow(row)
    else:
        with open(path, "a+") as f:
            writer = csv.writer(f)
            if row is not None:
                writer.writerow(row)


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
    return str(int(datetime.datetime.now().timestamp() * 1000))


def get_query(query_str):
    """get url query params
    """
    query = query_str.replace('?', '')
    query = query.split('&')
    query_dict = {}
    for item in query:
        item = item.split('=')
        if len(item) >= 2:
            query_dict[item[0]] = item[1]
    return query_dict
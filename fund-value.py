# -- coding: utf-8 --**
import requests
from helper import timestamp_str, write_csv
import demjson
import web


def fetchFund(code):
    # https://fundgz.1234567.com.cn/js/001186.js?rt=1606225216006
    url = 'https://fundgz.1234567.com.cn/js/' + code + '.js?rt=' + timestamp_str()
    resp = requests.get(url)
    text = resp.text
    text = text.replace('jsonpgz(', '')
    text = text.replace(');', '')
    json_data = demjson.decode(text)
    return json_data


def formatFund():
    """
    get all fund info
    """
    resp = requests.get('https://fund.eastmoney.com/js/fundcode_search.js')
    text = resp.text
    text = text.replace('var r = ', '')
    text = text.replace(';', '')
    json_data = demjson.decode(text)
    for item in json_data:
        result = {
            "code": item[0],
            "name": item[2],
            "type": item[3],
            "abbr": item[1],
            "full": item[4],
        }
        write_csv("./data/fund.csv", list(result.values()), list(result.keys()))
    return json_data


class index:
    def GET(self, code):
        query = web.ctx.query
        print(query)
        web.header('content-type', 'application/json;charset=utf-8')
        return demjson.encode(fetchFund(code))


if __name__ == "__main__":
    urls = (
        '/([0-9]{6})', 'index'
    )
    app = web.application(urls, globals())
    app.run()
    # formatFund()
    # fetchFund('001592')

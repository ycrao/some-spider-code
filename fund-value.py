# -- coding: utf-8 --**
import requests
from helper import timestamp_str, write_csv
import demjson
import web
from decimal import Decimal


def fetchFund(code):
    # https://fundgz.1234567.com.cn/js/001186.js?rt=1606225216006
    url = 'https://fundgz.1234567.com.cn/js/' + code + '.js?rt=' + timestamp_str()
    resp = requests.get(url)
    text = resp.text
    text = text.replace('jsonpgz(', '')
    text = text.replace(');', '')
    try:
        json_data = demjson.decode(text)
    except demjson.JSONDecodeError:
        json_data = None
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


class FundValue:
    def GET(self, code):
        web.header('content-type', 'application/json;charset=utf-8')
        fund_data = fetchFund(code)
        resp_code = 500
        resp_message = 'not a valid fund code or got something wrong'
        resp_data = None
        if fund_data is not None:
            resp_code = 200
            resp_message = 'ok'
            resp_data = {
                # 基金代码
                'fund_code': fund_data['fundcode'],
                # 基金名称
                'fund_name': fund_data['name'],
                # 基金单位净值（非预估，最新已确定的）
                'net_value': fund_data['dwjz'],
                # 基金单位净值日期
                'net_value_date': fund_data['jzrq'],
                # 预估净值
                'estimated_net_value': fund_data['gsz'],
                # 预估净值增长值
                'estimated_growth_value': str(Decimal(fund_data['gsz']) - Decimal(fund_data['dwjz'])),
                # 预估净值增长率
                'estimated_growth_rate': fund_data['gszzl'] + '%',
                # 预估净值时间
                'estimated_at': fund_data['gztime'] + ':00',
            }
        resp = {
            "code": resp_code,
            "message": resp_message,
            "data": resp_data,
        }
        return demjson.encode(resp, sort_keys=False)


if __name__ == "__main__":
    urls = (
        '/([0-9]{6})', 'FundValue'
    )
    app = web.application(urls, globals())
    app.run()
    # formatFund()
    # fetchFund('001592')

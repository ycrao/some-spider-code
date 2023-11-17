# -- coding: utf-8 --**
import datetime

import requests
from helper import timestamp_str, time_to_str
import demjson
import web
from decimal import Decimal
from fake_useragent import UserAgent


# see: https://blog.csdn.net/qq1130169218/article/details/122087853

def format_sina_stock_data(data):
    return {
        'source': 'sina',
        'name': data[0],
        'open': Decimal(data[1]),
        'close': Decimal(data[2]),
        'current': Decimal(data[3]),
        'high': Decimal(data[4]),
        'low': Decimal(data[5]),
        'buy': Decimal(data[6]),
        'sell': Decimal(data[7]),
        'volume': int(Decimal(data[8]) / 100),
        'amount': int(Decimal(data[9]) / 10000),
        'buy1_volume': round(Decimal(data[10]) / 100),
        'buy1': Decimal(data[11]),
        'buy2_volume': round(Decimal(data[12]) / 100),
        'buy2': Decimal(data[13]),
        'buy3_volume': round(Decimal(data[14]) / 100),
        'buy3': Decimal(data[15]),
        'buy4_volume': round(Decimal(data[16]) / 100),
        'buy4': Decimal(data[17]),
        'buy5_volume': round(Decimal(data[18]) / 100),
        'buy5': Decimal(data[19]),
        'sell1_volume': round(Decimal(data[20]) / 100),
        'sell1': Decimal(data[21]),
        'sell2_volume': round(Decimal(data[22]) / 100),
        'sell2': Decimal(data[23]),
        'sell3_volume': round(Decimal(data[24]) / 100),
        'sell3': Decimal(data[25]),
        'sell4_volume': round(Decimal(data[26]) / 100),
        'sell4': Decimal(data[27]),
        'sell5_volume': round(Decimal(data[28]) / 100),
        'sell5': Decimal(data[29]),
        'date_time': data[30] + ' ' + data[31],
    }


def _format_datetime_str(origin_datetime_str, origin_datetime_format='%Y%m%d%H%M%S',
                         to_date_format='%Y-%m-%d %H:%M:%S'):
    date_obj = datetime.datetime.strptime(origin_datetime_str, origin_datetime_format)
    return date_obj.strftime(to_date_format)


def format_tencent_stock_data(data):
    return {
        'source': 'tencent',
        'name': data[1],
        'open': Decimal(data[5]),
        'close': Decimal(data[4]),
        'current': Decimal(data[3]),
        'high': Decimal(data[33]),
        'low': Decimal(data[34]),
        'sell': Decimal(data[19]),
        'buy': Decimal(data[9]),
        'volume': Decimal(data[6]),
        'amount': Decimal(data[37]),
        'buy1_volume': Decimal(data[10]),
        'buy1': Decimal(data[9]),
        'buy2_volume': Decimal(data[12]),
        'buy2': Decimal(data[11]),
        'buy3_volume': Decimal(data[14]),
        'buy3': Decimal(data[13]),
        'buy4_volume': Decimal(data[16]),
        'buy4': Decimal(data[15]),
        'buy5_volume': Decimal(data[18]),
        'buy5': Decimal(data[17]),
        'sell1_volume': Decimal(data[20]),
        'sell1': Decimal(data[19]),
        'sell2_volume': Decimal(data[22]),
        'sell2': Decimal(data[21]),
        'sell3_volume': Decimal(data[24]),
        'sell3': Decimal(data[23]),
        'sell4_volume': Decimal(data[26]),
        'sell4': Decimal(data[25]),
        'sell5_volume': Decimal(data[28]),
        'sell5': Decimal(data[27]),
        'date_time': _format_datetime_str(data[30])
    }


def format_xueqiu_stock_data(data, buy_sell_data):
    return {
        'source': 'xueqiu',
        'name': data['data'][0]['symbol'],
        'open': data['data'][0]['open'],
        'close': data['data'][0]['last_close'],
        'current': data['data'][0]['current'],
        'high': data['data'][0]['high'],
        'low': data['data'][0]['low'],
        'sell': buy_sell_data['data']['sp1'],
        'buy': buy_sell_data['data']['bp1'],
        'volume': int(data['data'][0]['volume'] / 100),
        'amount': int(Decimal(data['data'][0]['amount']) / 10000),
        'buy1_volume': round(buy_sell_data['data']['bc1'] / 100),
        'buy1': buy_sell_data['data']['bp1'],
        'buy2_volume': round(buy_sell_data['data']['bc2'] / 100),
        'buy2': buy_sell_data['data']['bp2'],
        'buy3_volume': round(buy_sell_data['data']['bc3'] / 100),
        'buy3': buy_sell_data['data']['bp3'],
        'buy4_volume': round(buy_sell_data['data']['bc4'] / 100),
        'buy4': buy_sell_data['data']['bp4'],
        'buy5_volume': round(buy_sell_data['data']['bc5'] / 100),
        'buy5': buy_sell_data['data']['bp5'],
        'sell1_volume': round(buy_sell_data['data']['sc1'] / 100),
        'sell1': buy_sell_data['data']['sp1'],
        'sell2_volume': round(buy_sell_data['data']['sc2'] / 100),
        'sell2': buy_sell_data['data']['sp2'],
        'sell3_volume': round(buy_sell_data['data']['sc3'] / 100),
        'sell3': buy_sell_data['data']['sp3'],
        'sell4_volume': round(buy_sell_data['data']['sc4'] / 100),
        'sell4': buy_sell_data['data']['sp4'],
        'sell5_volume': round(buy_sell_data['data']['sc5'] / 100),
        'sell5': buy_sell_data['data']['sp5'],
        'date_time': time_to_str(int(buy_sell_data['data']['timestamp'] / 1000), '%Y-%m-%d %H:%M:%S'),
    }


def fetch_sina_stock(symbol):
    """
    symbol: 股票代码，例如：sz300750、sh600519
    这里我们以宁德时代 sz300750 作为示例
    返回数据格式：
    ```text
    var hq_str_sz300750 = "宁德时代,185.480,184.480,181.150,185.490,180.100,181.140,181.150,17466200,3180032494.610,600,181.140,1500,181.130,36700,181.120,7800,181.110,23860,181.100,988,181.150,200,181.160,1000,181.170,3500,181.180,1300,181.190,2023-11-16,15:35:00,00,D|1200|217380.000";
    ```
    """
    ua = UserAgent(browsers=['chrome', 'edge'])
    headers = {
        'Referer': 'https://finace.sina.com.cn/',
        'User-Agent': ua.random,
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;',
        'X-Requested-With': 'XMLHttpRequest',
    }
    symbol = symbol.lower()
    url = f'https://hq.sinajs.cn/list={symbol}'
    resp = requests.get(url, headers=headers)
    text = resp.text
    text = text.replace('var hq_str_' + symbol + '="', '')
    text = text.replace('";', '')
    data_array = text.split(',')
    '''
    0：股票名字；
    1: 今日开盘价；（开）
    2: 昨日收盘价；（收）
    3: 当前价格；
    4: 今日最高价；（高）
    5: 今日最低价；（低）
    6: 竞买价，即“买一”报价；
    7: 竞卖价，即“卖一”报价；
    8: 成交的股票数（单位为“个”）；
    9: 成交金额（单位为“元”）；
    10: “买一”申请 600 股，即 6 手；
    11: “买一”报价；
    (12, 13), (14, 15), (16, 17), (18, 19) 依次类推
    20: “卖一”申报 988 股，进位即 10 手；
    21: “卖一”报价
    (22, 23), (24, 25), (26, 27), (28, 29) 依次类推
    30: 日期；
    31: 时间；
    # 特别注意： 32序号之后可能不存在
    32: 未知；
    33: D|1200|217380.000 `217380.000` 为成交量，`1200` 为成交笔数
    '''
    return format_sina_stock_data(data_array)


def fetch_tencent_stock(symbol):
    """
    symbol: 股票代码，例如：sz300750、sh600519
    这里我们以宁德时代 sz300750 作为示例
    see:
    - https://gu.qq.com/sz300750/gp
    - https://web.sqt.gtimg.cn/utf8/q=sz300750
    - https://web.sqt.gtimg.cn/q=sz300750
    - https://qt.gtimg.cn/q=sz300750
    返回数据格式：
    ```text
    v_sz300750="51~宁德时代~300750~181.15~184.48~185.48~174662~75994~98668~181.14~6~181.13~15~181.12~367~181.11~78~181.10~239~181.15~10~181.16~2~181.17~10~181.18~35~181.19~13~~20231116161403~-3.33~-1.81~185.49~180.10~181.15/174662/3180032495~174662~318003~0.45~17.99~~185.49~180.10~2.92~7054.11~7967.44~4.42~221.38~147.58~1.06~635~182.07~19.19~25.93~~~0.88~318003.2495~21.7380~12~ A~GP-A-CYB~-16.58~-5.38~0.77~24.59~6.90~271.13~168.81~-2.38~-0.85~-22.12~3894069163~4398257697~81.94~-20.95~3894069163~~~-14.54~0.00~~CNY~0~~181.20~-135";
    ```
    """
    ua = UserAgent(browsers=['chrome', 'edge'])
    headers = {
        'Referer': 'https://gu.qq.com/' + symbol + '/gp',
        'User-Agent': ua.random,
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;',
        'X-Requested-With': 'XMLHttpRequest',
    }
    symbol = symbol.lower()
    url = f'https://web.sqt.gtimg.cn/utf8/q={symbol}'
    resp = requests.get(url, headers=headers)
    text = resp.text
    text = text.replace('v_' + symbol + '="', '')
    text = text.replace('";', '')
    data_array = text.split('~')
    '''
    0: 未知
    1: 股票名字
    2: 股票代码
    3: 当前价格
    4: 昨收
    5: 今开
    6: 成交量（手）
    7: 外盘 75994（手）
    8: 内盘 98668（手）
    (7+8 合计 174662）
    9: 买一价 
    10: 买一量（手）
    (11, 12), (13, 14), (15, 16), (17, 18) 依次类推
    19: 卖一价
    20: 卖一量（手）
    (21, 22), (23, 24), (25, 26), (27, 28) 依次类推
    29: 未知
    30: 日期 格式为YmdHis 示例: 20231116161403
    31: 跌幅值
    32: 跌幅百分比 %
    33: 今日最高价
    34: 今日最低价
    35: 当前价/成交量（手）/成交额（元）
    36: 不明，应该是成交量（手）
    37: 不明，应该是成交额（万元）
    38: 不明，应该是换手率（%）
    39: 市盈率（动态）
    40: 未知
    41: high
    42: low
    43: 振幅 % 
    44: 流动市值（亿元）
    45: 总市值（亿元）
    46: 市净率
    47: 未知
    48: 未知
    49: 未知
    50+: 均未知
    '''
    return format_tencent_stock_data(data_array)


def fetch_xueqiu_stock(symbol):
    """
    symbol: 股票代码，例如：SZ300750、SH000519
    这里我们以宁德时代 SZ300750 作为示例
    see: https://xueqiu.com/S/SZ300750
    雪球的接口较为繁琐，特别是五档盘口行情，需要额外请求（甚至可能限制爬虫）
    - https://stock.xueqiu.com/v5/stock/quote.json?symbol=SZ300750&extend=detail&_=1700185320809
    - https://stock.xueqiu.com/v5/stock/realtime/quotec.json?symbol=SZ300750&_=1700185320808
    - https://stock.xueqiu.com/v5/stock/realtime/pankou.json?symbol=SZ300750&_=1700185320810
    """
    ua = UserAgent(browsers=['chrome', 'edge'])
    headers = {
        'Referer': 'https://xueqiu.com/S/' + symbol,
        'User-Agent': ua.random,
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;',
        'X-Requested-With': 'XMLHttpRequest',
    }
    symbol = symbol.upper()
    ts = timestamp_str()
    url1 = f'https://stock.xueqiu.com/v5/stock/realtime/quotec.json?symbol={symbol}&_={ts}'
    url2 = f'https://stock.xueqiu.com/v5/stock/realtime/pankou.json?symbol={symbol}&_={ts}'
    resp1 = requests.get(url1, headers=headers)
    data = resp1.json()
    resp2 = requests.get(url2, headers=headers)
    bs_data = resp2.json()
    return format_xueqiu_stock_data(data, bs_data)


def get_query(query_str):
    query = query_str.replace('?', '')
    query = query.split('&')
    query_dict = {}
    for item in query:
        item = item.split('=')
        if len(item) >= 2:
            query_dict[item[0]] = item[1]
    return query_dict


class StockPrice:
    def GET(self, code):
        web.header('content-type', 'application/json;charset=utf-8')
        query_param = get_query(web.ctx.query)
        if 'source' in query_param:
            source = query_param['source']
        else:
            source = 'sina'
        if source == 'tencent':
            resp_data = fetch_tencent_stock(code)
        elif source == 'xueqiu':
            resp_data = fetch_xueqiu_stock(code)
        else:
            resp_data = fetch_sina_stock(code)
        resp = {
            'code': 200,
            'message': 'ok',
            'data': resp_data
        }
        return demjson.encode(resp, sort_keys=False)


if __name__ == "__main__":
    urls = (
        '/(sh[0-9]{6}|sz[0-9]{6})', 'StockPrice'
    )
    app = web.application(urls, globals())
    app.run()

# -- coding: utf-8 --**
import datetime
import demjson
import requests
import web
from helper import time_to_str, get_query
from decimal import Decimal
from fake_useragent import UserAgent


def fetch_cmb_forex(symbol):
    symbol = symbol.lower()
    symbol = symbol.replace('2cny', '')
    ref_map = {
        'cny': '人民币',
        'hkd': '港币',
        'nzd': '新西兰元',
        'aud': '澳大利亚元',
        'usd': '美元',
        'eur': '欧元',
        'cad': '加拿大元',
        'gbp': '英镑',
        'jpy': '日元',
        'sgd': '新加坡元',
        'chf': '瑞士法郎',
    }

    if symbol not in ref_map:
        return None
    url = 'https://fx.cmbchina.com/api/v1/fx/rate'
    ua = UserAgent(browsers=['chrome', 'edge'])
    headers = {
        'Referer': 'https://fx.cmbchina.com/Hq/',
        'User-Agent': ua.random,
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7,en-GB;',
        'X-Requested-With': 'XMLHttpRequest',
    }
    resp = requests.get(url, headers=headers)
    json_data = resp.json()
    price_items = {
        'cny': {
            'source': 'cmb',
            'name': '1人民币兑人民币',
            'symbol': 'cny2cny',
            'middle_price': 1,
            'price': 1,
            'datetime': time_to_str(int(datetime.datetime.now().timestamp()), '%Y-%m-%d %H:%M:%S')
        }
    }
    reversed_ref_map = dict(map(reversed, ref_map.items()))
    if json_data['returnCode'] == 'SUC0000':
        fx_items = json_data['body']
        for fx in fx_items:
            tmp_symbol = reversed_ref_map.get(fx['ccyNbr'])
            if tmp_symbol in ref_map:
                date_str = fx['ratDat']
                date_str = date_str.replace('年', '-')
                date_str = date_str.replace('月', '-')
                date_str = date_str.replace('日', ' ')
                price_items[tmp_symbol] = {
                    'source': 'cmb',
                    'name': '1' + fx['ccyNbr'] + '兑人民币',
                    'symbol': tmp_symbol + '2cny',
                    'middle_price': None,
                    # 现汇卖出价
                    'price': Decimal(Decimal(fx['rthOfr']) / 100),
                    # 现钞卖出价 fx['rtcOfr'] 现汇买入价 fx['rthBid'] 现钞买入价 fx['rtcBid']
                    'datetime': date_str + fx['ratTim'],
                }
    return price_items.get(symbol)


def trans_cn_silver_price(price, fx_rate=None):
    """
    trans `AG(T+D)` price -> `XAGUSD` price
    :param price: original AG(T+D) price (in cny/kg unit)
    :param fx_rate: forex rate, 1usd = ?cny
    :return:
    """
    if fx_rate is None:
        fx_data = fetch_cmb_forex('usd2cny')
        fx_rate = fx_data.get('price')
        fx_from = '招商银行(CMB)'
    else:
        fx_data = None
        fx_from = '用户输入(UserInput)'
    oz_to_g = Decimal('31.1035')
    price_to_usd_per_oz = float(price * oz_to_g / 1000 / fx_rate)
    cast = {
        'symbol': 'agtd',
        'original_price': int(price),
        'original_unit': 'cny/kg',
        'fx_rate': fx_rate,
        'fx_from': fx_from,
        'fx_detail': fx_data,
        'target_price': Decimal(format(price_to_usd_per_oz, '.3f')),
        'target_unit': 'usd/oz',
    }
    return cast


def trans_cn_gold_price(price, fx_rate=None):
    """
    trans `AU(T+D)` price -> `XAUUSD` price
    :param price: original AU(T+D) price (in cny/g unit)
    :param fx_rate: forex rate, 1usd = ?cny
    :return:
    """
    if fx_rate is None:
        fx_data = fetch_cmb_forex('usd2cny')
        fx_rate = fx_data.get('price')
        fx_from = '招商银行(CMB)'
    else:
        fx_data = None
        fx_from = '用户输入(UserInput)'
    oz_to_g = Decimal('31.1035')
    price_to_usd_per_oz = float(price * oz_to_g / fx_rate)
    cast = {
        'symbol': 'autd',
        'original_price': price,
        'original_unit': 'cny/g',
        'fx_rate': fx_rate,
        'fx_from': fx_from,
        'fx_detail': fx_data,
        'target_price': Decimal(format(price_to_usd_per_oz, '.2f')),
        'target_unit': 'usd/oz',
    }
    return cast


def trans_us_price(price, symbol, fx_rate=None):
    """
    trans `XAGUSD` price -> `AG(T+D)` price or `XAUUSD` price -> `AU(T+D)` price
    :param price: original `XAUUSD` or `XAGUSD` price (in usd/oz unit)
    :param symbol: xau or xag
    :param fx_rate: forex rate, 1usd = ?cny
    :return:
    """
    if symbol in ['xau', 'xag']:
        if fx_rate is None:
            fx_data = fetch_cmb_forex('usd2cny')
            fx_rate = fx_data.get('price')
            fx_from = '招商银行(CMB)'
        else:
            fx_data = None
            fx_from = '用户输入(UserInput)'
        oz_to_g = Decimal('31.1035')
        price_to_cny_per_g = price * fx_rate / oz_to_g
        price_to_cny_per_kg = price_to_cny_per_g * 1000
        if symbol == 'xau':
            target_price = '{:.2f}'.format(price_to_cny_per_g)
            target_unit = 'cny/g'
        else:
            target_price = '{:.0f}'.format(price_to_cny_per_kg)
            target_unit = 'cny/kg'
        cast = {
            'symbol': symbol,
            'original_price': float(price),
            'original_unit': 'usd/oz',
            'fx_rate': fx_rate,
            'fx_from': fx_from,
            'fx_detail': fx_data,
            'target_price': Decimal(target_price),
            'target_unit': target_unit,
        }
        return cast
    else:
        return None


class TransPrice:
    def GET(self, code):
        web.header('content-type', 'application/json;charset=utf-8')
        query_param = get_query(web.ctx.query)

        if 'fx_rate' in query_param:
            fx_rate = Decimal(query_param.get('fx_rate'))
        else:
            fx_rate = None
        if 'price' in query_param:
            metal_price = Decimal(query_param.get('price'))
            if code == 'autd':
                data = trans_cn_gold_price(metal_price, fx_rate)
            elif code == 'agtd':
                data = trans_cn_silver_price(metal_price, fx_rate)
            elif code == 'xau':
                data = trans_us_price(metal_price, 'xau', fx_rate)
            elif code == 'xag':
                data = trans_us_price(metal_price, 'xag', fx_rate)
            else:
                data = None
            resp_code = 500
            resp_message = 'not a valid fund code or got something wrong'
            resp_data = None
            if data is not None:
                resp_code = 200
                resp_message = 'ok'
                resp_data = data
            resp = {
                "code": resp_code,
                "message": resp_message,
                "data": resp_data,
            }
            return demjson.encode(resp, sort_keys=False)
        return demjson.encode({
            'code': 400,
            'message': 'not supported!',
            'data': None
        }, sort_keys=False)


if __name__ == "__main__":
    urls = (
        '/trans-price/(autd|agtd|xau|xag)', 'TransPrice'
    )
    app = web.application(urls, globals())
    app.run()

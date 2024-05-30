some-spider-code
----------------

### usage

```bash
# runtime: python >= 3.8
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# then run code
python fin-eco-news-spider-by-sina.py
# ...
```

### fin-eco-news-spider-by-sina

>   [fin-eco-news-spider-by-sina.py](./fin-eco-news-spider-by-sina.py)：新浪全球实时财经新闻爬虫。

![sina-spider](./assets/sina.png)

### fin-eco-news-spider-by-eastmoney

>   [fin-eco-news-spider-by-eastmoney.py](./fin-eco-news-spider-by-eastmoney.py)：东方财富全球财经快讯爬虫。

![eastmoney-spider](./assets/eastmoney.png)

### fin-eco-news-spider-by-jrwei

>   [fin-eco-news-spider-by-jrwei.py](./fin-eco-news-spider-by-jrwei.py)：金融圈财经快讯爬虫。

![jrwei-spider](./assets/jrwei.png)

### fund-value

>   [fund-value.py](./fund-value.py)：基金净值爬虫。

```bash
# 9501 as port
python fund-value.py 9501
```

Open `http://127.0.0.1:9501/012414` in browser. You can change `012414` (fund code) to another. See all codes in [data/fund.csv](./data/fund.csv) file.

Response example:

```json
{
    "code": 200,
    "message": "ok",
    "data": {
        "fund_code": "002939",
        "fund_name": "广发创新升级混合",
        "net_value": "1.9049",
        "net_value_date": "2023-11-15",
        "estimated_net_value": "1.8643",
        "estimated_growth_value": "-0.0406",
        "estimated_growth_rate": "-2.13%",
        "estimated_at": "2023-11-16 15:00:00"
    }
}
```

### stock-price

>   [stock-price.py](./stock-price.py)：股票行情爬虫。

Symbol rule: `sh600519` （沪市） or `sz300750` （深市） .

```bash
# 9502 as port
python stock-price.py 9502
```

Open `http://127.0.0.1:9502/sz300750?source=sina` in browser. You can change `sz300750` (Chinese stock code) to another, and the value of source `sina` (新浪) to `tencent` (腾讯) or `xueqiu` (雪球) . 

Response example:

```json
{
    "code": 200,
    "message": "ok",
    "data": {
        "source": "sina",
        "name": "宁德时代",
        "open": 179.85,
        "close": 181.15,
        "current": 180.91,
        "high": 181.25,
        "low": 179.49,
        "buy": 180.89,
        "sell": 180.9,
        "volume": 56526,
        "amount": 101923,
        "buy1_volume": 14,
        "buy1": 180.89,
        "buy2_volume": 5,
        "buy2": 180.83,
        "buy3_volume": 1,
        "buy3": 180.82,
        "buy4_volume": 2,
        "buy4": 180.8,
        "buy5_volume": 2,
        "buy5": 180.78,
        "sell1_volume": 6,
        "sell1": 180.9,
        "sell2_volume": 6,
        "sell2": 180.91,
        "sell3_volume": 5,
        "sell3": 180.92,
        "sell4_volume": 5,
        "sell4": 180.94,
        "sell5_volume": 1,
        "sell5": 180.95,
        "date_time": "2023-11-17 10:57:12"
    }
}
```

>   *Notice*: `data.volume`,`data.buyX_volume` and `data.sellY_volume` are the number of hands （`手`, 1手=100股）; `data.amount` is the amount of money but in ten thousand yuan unit（`万元`）; others are in yuan unit（`元`）.


### trans-price

>   [trans-price.py](./trans-price.py)：内外盘金银价格互转。当前上海金银 `Au(T+D)/Ag(T+D)` 相对于国际金银 `XAU/XAG` 均溢价不少，这个工具可以很方便快捷地进行转换。

| 时间                 | 国内金银                                     | 国际金银                                    | 汇率       | 溢价                             |
|--------------------|------------------------------------------|-----------------------------------------|----------|--------------------------------|
| `2024-05-30 21:00` | `Au(T+D) 552.39 cny/g => 2367.84 usd/oz` | `XAUUSD 2341.22 usd/oz => 546.18 cny/g` | `7.2561` | `6.21 cny/g` or `25.78 usd/oz` |
| `2024-05-30 21:15` | `Ag(T+D) 8267 cny/kg => 35.450 usd/oz`   | `XAGUSD 31.467 usd/oz => 7338 cny/kg`   | `7.2534` | `929 cny/kg` or `3.983 usd/oz` |

>   从上表可看到，国内白银相对于国际白银人民币计价溢超 900元每公斤，美元计价溢近 4美元每盎司。一些公开资料说中国央行最近2，3年一直在买入贵金属，且白银具有工业用途，国内新能源车、光伏等行业有大量需求，再加税，这些举措一起进一步推高国内外金银价差。

>   Translate China silver price (in cny/kg unit) to USA `XAGUSD` price  (in usd/oz unit). Translate China gold price (in cny/g unit) to USA `XAUUSD` price (in usd/oz unit).

```bash
# 9503 as port
python trans-price.py 9503
```

Open these api urls to see response.

```
http://127.0.0.1:9503/trans-price/autd?price=551.64
http://127.0.0.1:9503/trans-price/agtd?price=8508&fx_rate=7.2648
http://127.0.0.1:9503/trans-price/xau?price=2332.68&fx_rate=7.2530
http://127.0.0.1:9503/trans-price/xag?price=31.390
```

Response example:

Gold price: `Au(T+D) 551.64 cny/g` ≈ `XAUUSD 2364.46 usd/oz` by forex rate `7.2566`.

```json
{
    "code": 200,
    "message": "ok",
    "data": {
        "symbol": "autd",
        "original_price": 551.64,
        "original_unit": "cny/g",
        "fx_rate": 7.2566,
        "fx_from": "招商银行(CMB)",
        "fx_detail": {
            "source": "cmb",
            "name": "1美元兑人民币",
            "symbol": "usd2cny",
            "middle_price": null,
            "price": 7.2566,
            "datetime": "2024-05-30 18:01:14"
        },
        "target_price": 2364.46,
        "target_unit": "usd/oz"
    }
}
```

Silver price: `Ag(T+D) 8508 cny/kg` ≈ `XAGUSD 36.426 usd/oz` by forex rate `7.2648`.

```json
{
    "code": 200,
    "message": "ok",
    "data": {
        "symbol": "agtd",
        "original_price": 8508,
        "original_unit": "cny/kg",
        "fx_rate": 7.2648,
        "fx_from": "用户输入(UserInput)",
        "fx_detail": null,
        "target_price": 36.426,
        "target_unit": "usd/oz"
    }
}
```
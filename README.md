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

>   [stock-price.py](./fund-value.py)：股票行情爬虫。

Symbol rule: `sh600519` （沪市） or `sz300750` （深市） .

```bash
# 9502 as port
python stock-price.py 9502
```

Open `http://127.0.0.1:9502/sz300750?source=sina` in browser. You can change `sz300750` (Chinese stock code) to another, and the value of source `sina` (`新浪`) to `tencent` (腾讯) or `xueqiu` (雪球) . 

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



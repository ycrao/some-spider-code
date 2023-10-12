import requests
from helper import random_number_str, timestamp_str
import demjson
from termcolor import colored, cprint
import textwrap


def fetchNewestData():
    """
    from https://www.jrwei.com/datacenter/kuaixun
    :return:
    """
    headers = {
        'authority': 'kuaixun.jrjr.com:4338',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5,zh-HK;q=0.4',
        'origin': 'https://www.jrwei.com',
        'referer': 'https://www.jrwei.com/',
        'sec-ch-ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.55',
    }

    params = {
        'page': '1',
        'pageSize': '20',
        'token': '0f5cdad1-fe74-d523-437f-c9760d5265fb',
        'tokenCode': 'e7ca328c73d173f1a691c239a80f495e',
    }

    response = requests.get('https://kuaixun.jrjr.com:4338/get.php', params=params, headers=headers)
    return response.json()


if __name__ == "__main__":
    data = fetchNewestData()
    result_items = data['data']
    colored_header = colored(" 金融圈财经快讯 ", 'red', attrs=['blink', 'bold', 'reverse'])
    print(colored_header)
    print("")
    for item in result_items:
        news_id = item['NEWSID']
        publish_time = item['PUBLISHTIME']
        news_title = item['NEWS_TITLE']
        # cprint(f"{news_id}@{publish_time}:", 'light_grey', attrs=['underline'])
        contents_arr = textwrap.wrap(news_title, width=25)
        for con in contents_arr:
            cprint(f"{con}", 'light_grey')
        cprint(f"--------------------------------------------------", "white")
        # TODO: write data to file or database

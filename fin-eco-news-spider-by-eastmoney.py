import requests
from helper import random_number_str, timestamp_str
import demjson
from termcolor import colored, cprint
import textwrap


def fetchNewestData():
    """
    from https://kuaixun.eastmoney.com/
    :return:
    """
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-TW;q=0.5,zh-HK;q=0.4',
        'Connection': 'keep-alive',
        'Referer': 'https://kuaixun.eastmoney.com/',
        'Sec-Fetch-Dest': 'script',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.55',
        'sec-ch-ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    params = {
        'r': '0.2' + random_number_str(16),
        '_': timestamp_str(),
    }

    response = requests.get(
        'https://newsapi.eastmoney.com/kuaixun/v1/getlist_102_ajaxResult_50_1_.html',
        params=params,
        headers=headers,
    )
    text = response.text
    json_str = text.replace('var ajaxResult=', '')
    json_data = demjson.decode(json_str)
    return json_data


if __name__ == "__main__":
    data = fetchNewestData()
    result_items = data['LivesList']
    header = colored("东方财富全球财经快讯", 'red', attrs=['blink', 'bold', 'reverse'])
    print(header)
    print("")
    for item in result_items:
        news_id = item['id']
        show_time = item['showtime']
        title = item['title']
        url = item['url_w']
        # cprint(f"{news_id}@{show_time}:", 'light_grey', attrs=['underline'])
        contents_arr = textwrap.wrap(title, width=25)
        for con in contents_arr:
            cprint(f"{con}", 'light_grey')
        cprint(f"link: {url}", 'white')
        cprint(f"--------------------------------------------------", "white")
        # TODO: write data to file or database

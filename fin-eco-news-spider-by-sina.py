import requests
from helper import random_number_str, timestamp_str
import demjson
from termcolor import colored, cprint
import textwrap


def fetchNewestJsonpData(tag='0'):
    """
    from https://finance.sina.com.cn/7x24/?tag=0
    :return: json_data dict
    """
    ts_str = timestamp_str()
    cb_str = 'jQuery11120' + random_number_str(15) + '_' + ts_str
    headers = {
        'authority': 'zhibo.sina.com.cn',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://finance.sina.com.cn/',
        'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/117.0.0.0 Safari/537.36',
    }

    params = {
        'callback': cb_str,
        'page': '1',
        'page_size': '20',
        'zhibo_id': '152',
        # tag_id 0 为 全部，如果只关心特定标签，如`国际`，可以设置为 `102`
        'tag_id': tag,
        'dire': 'f',
        'dpc': '1',
        'pagesize': '20',
        '_': ts_str,
    }

    response = requests.get('https://zhibo.sina.com.cn/api/zhibo/feed', params=params, headers=headers)
    text = response.text
    text = text.replace('try{' + cb_str + '(', '')
    json_str = text.replace(');}catch(e){};', '')
    json_data = demjson.decode(json_str)
    # print(json_data)
    return json_data


if __name__ == "__main__":
    data = fetchNewestJsonpData()
    result_items = data['result']['data']['feed']['list']
    title = colored("新浪全球实时财经新闻(Sina Global Finance News)", 'red', attrs=['blink', 'bold', 'reverse'])
    print(title)
    print("")
    for item in result_items:
        sina_id = item['id']
        update_time = item['update_time']
        content = item['rich_text']
        # cprint(f"{sina_id}@{update_time}:", 'light_grey', attrs=['underline'])
        contents_arr = textwrap.wrap(content, width=25)
        for con in contents_arr:
            cprint(f"{con}", 'light_grey')

        cprint(f"--------------------------------------------------", "white")
        # TODO: write data to file or database


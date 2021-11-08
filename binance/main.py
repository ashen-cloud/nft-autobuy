#!/usr/bin/python3

import requests
import json
from datetime import datetime
import pytz
from time import sleep
import json

config_f = open('./config.json', 'r')
config = json.load(config_f)

csrftoken = '' + config['CSRFTOKEN']
cookie = u'''''' + config['COOKIE']
product_id = '' + config['PRODUCT_ID']
cookie = cookie.encode('utf8')
buy_amount = config['BUY_AMOUNT']

mbox_info_api = f"https://www.binance.com/bapi/nft/v1/friendly/nft/mystery-box/detail?productId={product_id}"
mbox_buy_api = "https://www.binance.com/bapi/nft/v1/private/nft/mystery-box/purchase"
user_data_api = "https://www.binance.com/bapi/accounts/v1/private/account/user/base-detail"

default_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'clienttype': 'web',
}

def is_ready(s_hours):
    time_now = datetime.today().strftime("%H:%M:%S.%f")
    time_now_arr = list(map(int, time_now[:8].split(':')))

    now_hours = time_now_arr[0] - 3

    return now_hours == s_hours

def main():
    session = requests.Session()
    session.headers.update({
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        'clienttype': 'web',
        'Content-Type': 'application/json',
        'cookie': cookie,
        'csrftoken': csrftoken,
    })

    user_data = session.post(user_data_api).json()
    print('Email', user_data['data']['email'])

    data = {
        'number': buy_amount,
        'productId': product_id
    }

    info = requests.get(mbox_info_api, headers=default_headers).json()
    
    tz = pytz.timezone('Europe/Zaporozhye')
    
    ts = int(info['data']['startTime'] / 1000)
    
    ts_tz = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    
    time_sale = ts_tz.split(' ')
    
    time_sale_arr = list(map(int, time_sale[1].split(':')))

    print(is_ready(time_sale_arr[0]))

    while not is_ready(time_sale_arr[0]):
      sleep(0.01)

    i = 0
    while i != 1000000:
      buy_res = session.post(mbox_buy_api, json=data).json()
      print(buy_res)
      i += 1


if __name__ == '__main__':
    main()



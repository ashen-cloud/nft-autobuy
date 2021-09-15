#!/usr/bin/python3

import requests
import json
from datetime import datetime
import pytz
from time import sleep

csrftoken = ''
cookie = u''''''
product_id = '133913760132809728'
cookie = cookie.encode('utf8')
buy_amount = 20

mbox_info_api = f"https://www.binance.com/bapi/nft/v1/friendly/nft/mystery-box/detail?productId={product_id}"
mbox_buy_api = "https://www.binance.com/bapi/nft/v1/private/nft/mystery-box/purchase"

default_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'clienttype': 'web',
}

def get_info():
    res = requests.get(mbox_info_api, headers=default_headers)
    return res.json()

def buy_box(sess):
    data = {
        'number': 1,
        'productId': product_id
    }

    return sess.post(mbox_buy_api, data=data).json()

def is_ready(s_hours):
    time_now = datetime.today().strftime("%H:%M:%S.%f")
    time_now_arr = list(map(int, time_now[:8].split(':')))

    now_hours = time_now_arr[0] - 3

    return now_hours == s_hours

def main():
    session = requests.Session()
    session.headers.update({
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'clienttype': 'web',
        'Content-Type': 'application/json',
        'cookie': cookie,
        'csrftoken': csrftoken
    })

    info = get_info()

    tz = pytz.timezone('Europe/Zaporozhye')

    ts = int(info['data']['startTime'] / 1000)

    ts_tz = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    time_sale = ts_tz.split(' ')

    time_sale_arr = list(map(int, time_sale[1].split(':')))

    while not is_ready(time_sale_arr[0]):
        sleep(0.01)

    session.post('https://www.binance.com/bapi/accounts/v1/private/account/user/base-detail').json()

    for i in range(buy_amount):
        buy_res = buy_box(session)
        print(buy_res)


if __name__ == '__main__':
    main()

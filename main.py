#!/usr/bin/python3

import requests
import json
from datetime import datetime
import pytz
from time import sleep

csrftoken = '8069d430920443187cd3693334cd37a8'
cookie = u'''cid=AF94XGao; nft-init-compliance=true; bnc-uuid=39cd3923-d796-4912-a3f6-9507f518e770; campaign=accounts.binance.com; source=referral; userPreferredCurrency=UAH_USD; _ga=GA1.2.1762933967.1631295596; home-ui-ab=A; fiat-prefer-currency=RUB; sensorsdata2015jssdkcross={"distinct_id":"158443705","first_id":"17bd09819a62c1-0c1ca4e6fc9ab6-525b340e-2073600-17bd09819a7ae9","props":{"$latest_traffic_source_type":"直接流量","$latest_search_keyword":"未取到值_直接打开","$latest_referrer":""},"$device_id":"17bd09819a62c1-0c1ca4e6fc9ab6-525b340e-2073600-17bd09819a7ae9"}; BNC_FV_KEY=3144c906acf9a8c7bbb97640fa9eb32db9ba0b6e; BNC_FV_KEY_EXPIRE=1631701310842; _gid=GA1.2.408621267.1631616643; defaultMarketTab=spot; monitor-uuid=c4d3fb14-846e-4be3-bc54-f55fdfc31d72; gtId=e304d9a6-cfe2-414b-a7a5-207a5e8310b0; s9r1=D872C9A37E1679CBC76A78AB5211D893; lang=ru; _gat=1; cr00=AE13794FF44B841AACD8FE5AA6504586; d1og=web.158443705.F8A72387601C39ABEEC694CEAEC2F735; r2o1=web.158443705.3BBF81F70D27688D460D509ADA31B112; f30l=web.158443705.0EF1C041C1C8664DE3415CE5037BDEBD; logined=y; isAccountsLoggedIn=y; BINANCE_USER_DEVICE_ID={"2737792d6ec0db1528c540bd33c54494":{"date":1621715873601,"value":"1621715874279wL7LdsGoqBZX1w02qb3"},"dd5ed2b4b00c472a9f54b8dd25f3345b":{"date":1631441634882,"value":"1631441634555MtjdOilI9G1II0IGF8U"},"69aa6726cf605e08ae28c685f928c315":{"date":1631616940835,"value":"1631616941779lKE5LRluiuekEqI6Oqc"}}; p20t=web.158443705.FACA31A8BEAE0162FB18CECD3FF50C51'''
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

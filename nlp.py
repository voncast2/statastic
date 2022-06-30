import json
import random
import time
from hashlib import md5

import requests

appid = '20220606001240056'
appKey = 'vGjI8OPdUzBy6XeTzDD7'

from_lang = 'zh'
to_lang = 'en'

endpoint = 'https://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path

def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


# Send request
def Nlp(query):
    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appKey)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {
        'appid': appid,
        'q': query,
        'from': from_lang,
        'to': to_lang,
        'salt': salt,
        'sign': sign
    }
    middle = 'apple'
    for i in range(2):
        if i == 0:
            r = requests.post(url, params=payload, headers=headers)
            result_middle = r.json()
            middle = result_middle['trans_result'][0]['dst']
            print("英文：" + middle)
            time.sleep(1)
        if i == 1:
            salt2 = random.randint(32768, 65536)
            sign2 = make_md5(appid + middle + str(salt2) + appKey)
            payload2 = {
                'appid': appid,
                'q': middle,
                'from': to_lang,
                'to': from_lang,
                'salt': salt2,
                'sign': sign2
            }
            r2 = requests.post(url, params=payload2, headers=headers)
            result_middle2 = r2.json()
            result = result_middle2['trans_result'][0]['dst']
            print("增强：" + result)
            return result
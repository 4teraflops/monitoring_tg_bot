import requests
from requests.exceptions import HTTPError
from requests.auth import HTTPBasicAuth
import json
from src import config
import time
import random
from loguru import logger

logger.add(f'extentions/demo_checker/src/log/{__name__}.log', format='{time} {level} {message}', level='DEBUG', rotation='10 MB', compression='zip')
s = requests.Session()
# Приватный ключ через тектсовик я вытащил из серта pem, затем командой
# "openssl rsa -in my.key_encrypted -out my.key_decrypted" (со вводом пароля) расшифровал закрытый ключ
# s.cert = (config.sert_path, config.key_path)
auth = HTTPBasicAuth(config.shopToken, config.sec_key)
user = {}  # Для записи локальных переменных в глобальную
output = []


#@logger.catch()
def create_anonimus_pay():
    #logger.info('Check method /do/payment/anonymous...')
    output.append('\nCheck anonimus payment methods:\n\n')
    output.append('/do/payment/anonymous...')
    url = config.anonimus_pay_url
    payload = {
        "serviceCode": f"{config.service_code}",
        "amount": "2500",
        "comission": "0",
        "properties": [
            {
                "name": "ПОЗЫВНОЙ",
                "value": f"{random.randint(10, 20)}"
            }
        ]
    }
    # Рассчет подписи
    #sign_str = payload['serviceCode'] + '&' + payload['amount'] + '&' + payload['comission'] + '&' + payload['properties'][0]['name'] + '&' + payload['properties'][0]['value'] + '&' + payload['shopToken'] + '&' + config.sec_key
    #pre_sign = (hashlib.md5(f"{sign_str}".encode('utf-8')).hexdigest()).upper()
    #sign = (hashlib.md5(f"{pre_sign}".encode('utf-8')).hexdigest()).upper()
    #payload['sign'] = sign
    headers = {
        'Content-Type': 'application/json',
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0",
    }
    r = s.post(url, data=json.dumps(payload), headers=headers, auth=auth)
    #logger.info(f'responce: {r.text}')
    if r.status_code == 200:
        request = r.json()
    else:
        output.append(f'\ncreate_anonimus_pay: http error. request status code: {r.status_code}')
        logger.error(f'\ncreate_anonimus_pay: http error. request status code: {r.status_code}')
        raise HTTPError

    try:
        user['regPayNum'] = request['regPayNum']
        user['payUrl'] = request['payUrl']
        user['methodType'] = request['methodType']
    except KeyError:
        #print(f'Something wrong! Key Error. Url: {url}, request: {request}')
        output.append(f'Something wrong! Except Key Error. Url: {url}, request: {request}\n')

    if user['methodType'] == 'GET' and 'https://demo-acq.bisys.ru/cardpay/card?order=' in user['payUrl'] and user['regPayNum']:
        output.append('OK\n')
    else:
        output.append(f'Something wrong!\nrequest_status_code: {r.status_code}\nrequest: {request}\n')
    # Открываем полученную ссылку, чтоб перехватить Cookies
    s.get(user['payUrl'], headers=headers)
    user['cookies'] = s.cookies.get_dict()


def payment_created_pay():
    #logger.info('Trying to payment created pay')
    output.append('Trying to payment created pay...\nSent a POST request...\n')
    order = user['payUrl'].replace('https://demo-acq.bisys.ru/cardpay/card?order=', '')
    payload = {
        "form": "default",
        "operation": "pay",
        "order": f"{order}",
        "type": "visa",
        "pan": "4000000000000002",
        "exp": "01 21",
        "holder": "hard support",
        "secret": "123"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": f"{user['payUrl']}",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0",
        "Cookies": f"{user['cookies']}"
    }

    url = config.acq_pay_url
    r = s.post(url, data=payload, headers=headers, auth=auth)
    if r.status_code == 200:
        output.append('Response code == 200 OK\n')
    else:
        output.append(f'Something wrong!\nrequest_status_code: {r.status_code}\nrequest_text: {r.text}\n')


def check_pay_status():
    url = config.payment_state_url
    #logger.info('Check payment state...')
    output.append('Check payment state...')
    payload = {
        "regPayNum": f"{user['regPayNum']}"
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = s.post(url, data=json.dumps(payload), headers=headers, auth=auth)
    #logger.info(f'response: {r.text}')
    request = r.json()
    payment_state = request['state']
    if payment_state == 'payed':
        output.append('OK\n')
    elif payment_state == 'created':
        output.append(f'Payment state: {payment_state}. Retry...\n')
        time.sleep(10)
        check_pay_status()
    else:
        output.append(f'Something wrong! payment state: {payment_state}\n')


if __name__ == '__main__':
    create_anonimus_pay()
    payment_created_pay()
    check_pay_status()
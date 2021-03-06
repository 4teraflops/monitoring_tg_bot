import requests
from requests.exceptions import HTTPError
import json
import os
from .src import config
import time
import hashlib
import random
from datetime import datetime
from loguru import logger

logger.add(f'log/{__name__}.log', format='{time} {level} {message}', level='DEBUG', rotation='10 MB', compression='zip')


s = requests.Session()
sert_path = 'extentions/demo_checker/src/cert.pem'
key_path = 'extentions/demo_checker/src/dec.key'
# Приватный ключ через тектсовик я вытащил из серта pem, затем командой
# "openssl rsa -in my.key_encrypted -out my.key_decrypted" (со вводом пароля) расшифровал закрытый ключ
s.cert = (sert_path, key_path)
user = {}  # Для записи локальных переменных в глобальную
json_headers = {'Content-Type': 'application/json'}
output = []


@logger.catch()
def user_registration():
    #print('Check method /user/registration...', end='')
    output.append('\nCheck rekurrent payment methods:\n\n')
    output.append('/user/registration...')
    url = config.user_registration_rek_url
    login = '7902' + f'{random.randint(1000000, 9999999)}'
    payload = {
        "sign": "C5A5386EBADC3D0574CCB7A81820698A",
        "login": f"{login}",
        "shopToken": f"{config.shopToken}"
    }

    # Рассчет подписи
    sign_str = payload['login'] + '&' + payload['shopToken'] + '&' + config.sec_key
    pre_sign = (hashlib.md5(f"{sign_str}".encode('utf-8')).hexdigest()).upper()
    sign = (hashlib.md5(f"{pre_sign}".encode('utf-8')).hexdigest()).upper()
    payload['sign'] = sign

    r = s.post(url, data=json.dumps(payload), headers=json_headers)  # тут есть login, userToken

    if r.status_code == 200:  # !!! этот кусок не пашет. Если демо ляжет, то в предыдущей строке бот крашнется
        request = r.json()
        try:
            # print('OK')
            output.append('OK\n')
            user['login'] = request['login']
        except KeyError:
            # print(f'Something wrong! url: {url}, request: {request}')
            output.append(f'Something wrong! url: {url}, request: {request}\n')
    else:
        output.append(f'\nuser_registration: http error. request status code: {r.status_code}')
        logger.error(f'\nuser_registration: http error. request status code: {r.status_code}')
        raise HTTPError


def get_user_status():
    #print('Check method /user/status...', end='')
    output.append('/user/status...')
    url = config.user_status_rek_url
    payload = {
        "sign": "C5A5386EBADC3D0574CCB7A81820698A",
        "login": f"{user['login']}",
        "shopToken": f"{config.shopToken}"
    }
    # Рассчет подписи
    sign_str = payload['login'] + '&' + payload['shopToken'] + '&' + config.sec_key
    pre_sign = (hashlib.md5(f"{sign_str}".encode('utf-8')).hexdigest()).upper()
    sign = (hashlib.md5(f"{pre_sign}".encode('utf-8')).hexdigest()).upper()
    payload['sign'] = sign

    request = s.post(url, data=json.dumps(payload), headers=json_headers).json()

    if request['state'] == 'active':
        #print('OK')
        output.append('OK\n')
    else:
        #print(f'Something wrong! url: {url}, request: {request}')
        output.append(f'Something wrong! url: {url}, request: {request}\n')
    userToken = request['userToken']
    user['userToken'] = userToken  # Записываем в глобальную переменную


def get_cards_rek():
    url = config.get_cards_rek_url
    output.append('/get/cards...')
    payload = {
        "sign": "C5A5386EBADC3D0574CCB7A81820698A",
        "userToken": f"{user['userToken']}",
        "shopToken": f"{config.shopToken}"
    }

    # Рассчет подписи
    sign_str = payload['userToken'] + '&' + payload['shopToken'] + '&' + config.sec_key
    pre_sign = (hashlib.md5(f"{sign_str}".encode('utf-8')).hexdigest()).upper()
    sign = (hashlib.md5(f"{pre_sign}".encode('utf-8')).hexdigest()).upper()
    payload['sign'] = sign

    request = s.post(url, data=json.dumps(payload), headers=json_headers).json()
    #print('Check method /get/cards...', end='')
    cards = request['cards']
    user['cards'] = cards  # Записал в глобальную переменную
    if cards:
        #print('OK')
        output.append('OK\n')
    else:
        #print(f'Something wrong! url: {url} request: {request}')
        output.append(f'No cards.\n')


def card_registration():
    #print('Check method /card/registration...', end='')
    output.append('/card/registration...')
    url = config.card_registration_url_rek
    payload = {
        "sign": "C5A5386EBADC3D0574CCB7A81820698A",
        "userToken": f"{user['userToken']}",
        "shopToken": f"{config.shopToken}"
    }
    # Рассчет подписи
    sign_str = payload['userToken'] + '&' + payload['shopToken'] + '&' + config.sec_key
    pre_sign = (hashlib.md5(f"{sign_str}".encode('utf-8')).hexdigest()).upper()
    sign = (hashlib.md5(f"{pre_sign}".encode('utf-8')).hexdigest()).upper()
    payload['sign'] = sign

    request = s.post(url, data=json.dumps(payload), headers=json_headers).json()

    registration_url = request['payUrl']
    order = registration_url.replace('https://demo-acq.bisys.ru/cardpay/card?order=', '')

    # Открываем payUrl чтоб перехватить Cookies
    s.get(registration_url, headers=json_headers)
    cookies = s.cookies.get_dict()

    reg_payload = {
        "form": "default",
        "operation": "checkpay",
        "order": f"{order}",
        "type": "visa",
        "pan": "4000000000000002",
        "exp": "01 21",
        "holder": "hard support",
        "secret": "123"
    }

    reg_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": f"{registration_url}",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0",
        "Cookies": f"{cookies}"
    }
    reg_url = 'https://demo-acq.bisys.ru/cardpay/api/C/rpcheck'
    reg_request = s.post(reg_url, data=reg_payload, headers=reg_headers)

    if reg_request.status_code == 200:
        #print('OK')
        output.append('OK\n')
        #print(f'request: {reg_request.text}')
    else:
        #print(f'Something wrong! url: {url} request: {reg_request}')
        output.append(f'Something wrong! url: {url} request: {reg_request}\n')


def do_payment():

    url = config.do_payment_rek_url
    output.append('/do/payment...')
    try:
        cardToken = user['cards'][0]['cardToken']  # Берем первую привязанную карту
    except IndexError:
        #print('IndexError... No cards. Start method /card/registration...')
        output.append('IndexError... No cards. Start method /card/registration...\n')
        card_registration()  # пробуем повторно зарегать карту
        try:
            cardToken = user['cards'][0]['cardToken']
        except IndexError:
            output.append('IndexError... No cards. Stop method.\n')
            return
    payload = {
        "sign": "C5A5386EBADC3D0574CCB7A81820698A",
        "serviceCode": f"{config.service_code}",
        "userToken": f"{user['userToken']}",
        "amount": "2500",
        "comission": "0",
        "cardToken": f"{cardToken}",  # берем первую привязанную карту
        "holdTtl": "345600",
        "properties": [
            {
                "name": "ПОЗЫВНОЙ",
                "value": f"{random.randint(10, 20)}"
            }
        ],
        "shopToken": f"{config.shopToken}"
    }
    # Рассчет подписи
    sign_str = payload['serviceCode'] + '&' + payload['userToken'] + '&' + payload['amount'] + '&' + \
               payload['comission'] + '&' + payload['cardToken'] + '&' + payload['holdTtl'] + '&' + \
               payload['properties'][0]['name'] + '&' + payload['properties'][0]['value'] + '&' + \
               payload['shopToken'] + '&' + config.sec_key
    pre_sign = (hashlib.md5(f"{sign_str}".encode('utf-8')).hexdigest()).upper()
    sign = (hashlib.md5(f"{pre_sign}".encode('utf-8')).hexdigest()).upper()
    payload['sign'] = sign
    #print('Check method /do/payment...', end='')
    request = (s.post(url, data=json.dumps(payload), headers=json_headers)).json()
    regPayNum = request['regPayNum']

    user['regPayNum'] = regPayNum  # Записал в глобальную переменную
    if regPayNum:
        #print('OK')
        output.append('OK\n')
    else:
        #print(f'Something wrong! url: {url} request: {request}')
        output.append(f'Something wrong! url: {url} request: {request}\n')


def confirm_pay():
    url = config.confirm_pay_rek_url
    output.append('/provision-services/confirm...')
    try:
        regPayNum = user['regPayNum']
    except KeyError:
        output.append('No regPayNum. Stop Method\n')
        return
    payload = {
        "sign": "C5A5386EBADC3D0574CCB7A81820698A",
        "regPayNum": f"{regPayNum}",
        "orderId": f"{random.randint(1000000, 2000000)}",
        "shopToken": f"{config.shopToken}"
    }
    # Рассчет подписи
    sign_str = payload['regPayNum'] + '&' + payload['orderId'] + '&' + payload['shopToken'] + '&' + config.sec_key
    pre_sign = (hashlib.md5(f"{sign_str}".encode('utf-8')).hexdigest()).upper()
    sign = (hashlib.md5(f"{pre_sign}".encode('utf-8')).hexdigest()).upper()
    payload['sign'] = sign

    #print('Check method /provision-services/confirm...', end='')
    request = (s.post(url, data=json.dumps(payload), headers=json_headers)).json()
    result = request['resultState']
    if result == 'success':
        user['payment_state'] = result
        #print('OK')
        output.append('OK\n')
    else:
        #print(f'Something wrong! url: {url} request: {request}')
        output.append(f'Something wrong! url: {url} request: {request}\n')


def get_pay_state():
    url = config.get_pay_state_url
    output.append('/payment/state...')
    try:
        regPayNum = user['regPayNum']
    except KeyError:
        output.append('No regPayNum. Stop Method\n')
        return
    payload = {
        "sign": "C5A5386EBADC3D0574CCB7A81820698A",
        "regPayNum": f"{regPayNum}",
        "shopToken": f"{config.shopToken}"
    }
    # Рассчет подписи
    sign_str = payload['regPayNum'] + '&' + payload['shopToken'] + '&' + config.sec_key
    pre_sign = (hashlib.md5(f"{sign_str}".encode('utf-8')).hexdigest()).upper()
    sign = (hashlib.md5(f"{pre_sign}".encode('utf-8')).hexdigest()).upper()
    payload['sign'] = sign

    #print("Check method /payment/state...", end='')
    request = s.post(url, data=json.dumps(payload), headers=json_headers).json()
    payment_state = request['state']
    if payment_state:
        #print('OK')
        output.append('OK\n')
        user['payment_state'] = payment_state
    else:
        #print(f'Something wrong! url: {url} request: {request}')
        output.append(f'Something wrong! url: {url} request: {request}\n')


def refund_payment():
    url = config.refund_rek_url
    # Сначала выполняем функцию создания платежа с указанием holdttl
    # будет новый regPayNum, он перезапишется в глобальный словарь user
    do_payment()
    # таймаут 3 секунды, иначе возвращается статус created
    time.sleep(3)
    output.append('/provision-services/refund...')
    try:
        regPayNum = user['regPayNum']
    except KeyError:
        output.append('No regPayNum. Stop Method\n')
        return
    payload = {
        "sign": "C5A5386EBADC3D0574CCB7A81820698A",
        "regPayNum": f"{regPayNum}",
        "orderId": f"{random.randint(10, 20)}",
        "shopToken": f"{config.shopToken}"
    }
    # Рассчет подписи
    sign_str = payload['regPayNum'] + '&' + payload['orderId'] + '&' + payload['shopToken'] + '&' + config.sec_key
    #print(f'userToken: {payload["userToken"]}\ncardToken: {payload["cardToken"]}\nshopToken: {payload["shopToken"]}')
    pre_sign = (hashlib.md5(f"{sign_str}".encode('utf-8')).hexdigest()).upper()
    sign = (hashlib.md5(f"{pre_sign}".encode('utf-8')).hexdigest()).upper()
    payload['sign'] = sign
    #print('Check method /provision-services/refund...', end='')
    request = (s.post(url, data=json.dumps(payload), headers=json_headers)).json()
    result = request['resultState']
    if result == 'success':
        #print('OK')
        output.append('OK\n')
    else:
        #print(f'Something wrong! url: {url} request: {request}')
        output.append(f'Something wrong! url: {url} request: {request}\n')


def card_deactivation():
    url = config.card_deactivation_url
    output.append('/card/deatcivation...')
    try:
        cardToken = user['cards'][0]['cardToken']  # Берем первую карту
    except IndexError:
        output.append('No cards. Stop method\n')
        return
    payload = {
        "sign": "C5A5386EBADC3D0574CCB7A81820698A",
        "userToken": f"{user['userToken']}",
        "shopToken": f"{config.shopToken}",
        "cardToken": f"{cardToken}"
    }

    # Рассчет подписи
    sign_str = payload['userToken'] + '&' + payload['cardToken'] + '&' + payload['shopToken'] + '&' + config.sec_key
    #print(f'userToken: {payload["userToken"]}\ncardToken: {payload["cardToken"]}\nshopToken: {payload["shopToken"]}')
    pre_sign = (hashlib.md5(f"{sign_str}".encode('utf-8')).hexdigest()).upper()
    sign = (hashlib.md5(f"{pre_sign}".encode('utf-8')).hexdigest()).upper()
    payload['sign'] = sign
    #print('Check method /card/deatcivation...', end='')
    request = (s.post(url, data=json.dumps(payload), headers=json_headers)).json()
    result = request['resultState']
    if result == 'success':
        #print('OK')
        output.append('OK\n')
    else:
        #print(f'Something wrong! url: {url} request: {request}')
        output.append(f'Something wrong! url: {url} request: {request}\n')



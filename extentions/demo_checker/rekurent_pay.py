import requests
from requests.exceptions import HTTPError
from requests.auth import HTTPBasicAuth
import json
from .src import config
import time
import random
from loguru import logger

logger.add(f'extentions/demo_checker/src/log/{__name__}.log', format='{time} {level} {message}', level='DEBUG', rotation='10 MB', compression='zip')
auth = HTTPBasicAuth(config.shopToken, config.sec_key)
s = requests.Session()
user = {}  # Для записи локальных переменных в глобальную
json_headers = {'Content-Type': 'application/json'}
output = []


def user_registration():
    output.append('\nCheck rekurrent payment methods:\n\n')
    output.append('/user/registration...')
    url = config.user_registration_rek_url
    login = '7902' + f'{random.randint(1000000, 9999999)}'
    payload = {
        "login": f"{login}"
    }

    r = s.post(url, data=json.dumps(payload), headers=json_headers, auth=auth)  # тут есть login, userToken
    #logger.info(f'response: {r.json()}')
    if r.status_code == 200:  # !!! этот кусок не пашет. Если демо ляжет, то в предыдущей строке бот крашнется
        request = r.json()
        try:
            output.append('OK\n')
            user['login'] = request['login']
        except KeyError:
            output.append(f'Something wrong! url: {url}, request: {request}\n')
    else:
        output.append(f'\nuser_registration: http error. request status code: {r.status_code}')
        #logger.error(f'\nuser_registration: http error. request status code: {r.status_code}')
        raise HTTPError


def get_user_status():
    output.append('/user/status...')
    url = config.user_status_rek_url
    payload = {
        "login": f"{user['login']}"
    }
    r = s.post(url, data=json.dumps(payload), headers=json_headers, auth=auth)
    response = r.json()
    #logger.info(f'response: {r.text}')
    if response['state'] == 'active':
        output.append('OK\n')
    else:
        output.append(f'Something wrong! url: {url}, response: {response}\n')
    userToken = response['userToken']
    user['userToken'] = userToken  # Записываем в глобальную переменную


def get_cards_rek():
    url = config.get_cards_rek_url
    output.append('/get/cards...')
    payload = {
        "userToken": f"{user['userToken']}",
    }
    r = s.post(url, data=json.dumps(payload), headers=json_headers, auth=auth)
    response = r.json()
    #logger.info(f'response: {response}')
    cards = response['cards']
    user['cards'] = cards  # Записал в глобальную переменную
    if cards:
        output.append('OK\n')
    else:
        output.append(f'No cards.\n')


def card_registration():
    output.append('/card/registration...')
    url = config.card_registration_url_rek
    payload = {
        "userToken": f"{user['userToken']}"
    }
    r = s.post(url, data=json.dumps(payload), headers=json_headers, auth=auth)
    response = r.json()
    #logger.info(f'response: {response}')
    registration_url = response['payUrl']
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
    reg_request = s.post(reg_url, data=reg_payload, headers=reg_headers, auth=auth)
    #logger.info(f'reg_response: {reg_request.text}')
    if reg_request.status_code == 200:
        output.append('OK\n')
    else:
        output.append(f'Something wrong! url: {url} request: {reg_request}\n')


def do_payment():

    url = config.do_payment_rek_url
    output.append('/do/payment...')
    # Сначала запишем действующие карты по клиенту
    get_cards_rek()
    try:
        cardToken = user['cards'][0]['cardToken']  # Берем первую привязанную карту
    except IndexError:
        output.append('IndexError... No cards. Start method /card/registration...\n')
        card_registration()  # пробуем повторно зарегать карту
        try:
            cardToken = user['cards'][0]['cardToken']
        except IndexError:
            output.append('IndexError... No cards. Stop method.\n')
            return
    payload = {
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
        ]
    }
    r = s.post(url, data=json.dumps(payload), headers=json_headers, auth=auth)
    response = r.json()
    logger.info(f'response: {response}')
    regPayNum = response['regPayNum']
    user['regPayNum'] = regPayNum  # Записал в глобальную переменную
    if regPayNum:
        output.append('OK\n')
    else:
        output.append(f'Something wrong! url: {url} response: {response}\n')


def confirm_pay():
    url = config.confirm_pay_rek_url
    output.append('/provision-services/confirm...')
    try:
        regPayNum = user['regPayNum']
    except KeyError:
        output.append('No regPayNum. Stop Method\n')
        return
    payload = {
        "regPayNum": f"{regPayNum}",
        "orderId": f"{random.randint(1000000, 2000000)}"  # Рандом потому что тут номер заказа в системе клиента
    }
    r = s.post(url, data=json.dumps(payload), headers=json_headers, auth=auth)
    response = r.json()
    logger.info(f'response: {response}')
    try:
        result = response['resultState']
        if result == 'success':
            user['payment_state'] = result
            output.append('OK\n')
        else:
            output.append(f'Something wrong! url: {url} response: {response}\n')
    except KeyError:
        output.append(f'Response key error. url: {url} response: {response}\n')
        logger.error(f'Response key error. url: {url} response: {response}\n')


def get_pay_state():
    url = config.get_pay_state_url
    output.append('/payment/state...')
    try:
        regPayNum = user['regPayNum']
    except KeyError:
        output.append('No regPayNum. Stop Method\n')
        return
    payload = {
        "regPayNum": f"{regPayNum}"
    }
    r = s.post(url, data=json.dumps(payload), headers=json_headers, auth=auth)
    response = r.json()
    logger.info(f'response: {response}')
    try:
        payment_state = response['state']
        if payment_state:
            output.append('OK\n')
            user['payment_state'] = payment_state
        else:
            output.append(f'Something wrong! url: {url} response: {response}\n')
    except KeyError:
        output.append(f'Response key error. url: {url} response: {response}\n')
        logger.error(f'Response key error. url: {url} response: {response}\n')


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
        "regPayNum": f"{regPayNum}",
        "orderId": f"{random.randint(10, 20)}",
    }
    r = s.post(url, data=json.dumps(payload), headers=json_headers, auth=auth)
    response = r.json()
    logger.info(f'response: {response}')
    try:
        result = response['resultState']
        if result == 'success':
            output.append('OK\n')
        else:
            output.append(f'Something wrong! url: {url} response: {response}\n')
    except KeyError:
        output.append(f'Response key error. url: {url} response: {response}\n')
        logger.error(f'Response key error. url: {url} response: {response}\n')


def card_deactivation():
    url = config.card_deactivation_url
    output.append('/card/deatcivation...')
    try:
        cardToken = user['cards'][0]['cardToken']  # Берем первую карту
    except IndexError:
        output.append('No cards. Stop method\n')
        return
    payload = {
        "userToken": f"{user['userToken']}",
        "cardToken": f"{cardToken}"
    }
    r = s.post(url, data=json.dumps(payload), headers=json_headers, auth=auth)
    response = r.json()
    logger.info(f'response: {response}')
    result = response['resultState']
    if result == 'success':
        output.append('OK\n')
    else:
        output.append(f'Something wrong! url: {url} response: {response}\n')


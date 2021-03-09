import sqlite3
import datetime

db_path = '/home/support/soft/acqpc_mon/src/db.sqlite'


def _acqpc_mon_digest():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    last_id = get_cursor_id('all_data')
    acqpc_status = cursor.execute(f'SELECT acqpc_status FROM all_data WHERE id = {last_id}').fetchall()[0][0]
    acqpc_datasource_status = cursor.execute(f'SELECT acqpc_datasource_status FROM all_data WHERE id = {last_id}').fetchall()[0][0]
    autopays_datasource_status = cursor.execute(f'SELECT autopays_datasource_status FROM all_data WHERE id = {last_id}').fetchall()[0][0]
    free_disk_space_procent = cursor.execute(f'SELECT free_disk_space_procent FROM all_data WHERE id = {last_id}').fetchall()[0][0]
    acqpc_ping_status = cursor.execute(f'SELECT ping_status FROM all_data WHERE id = {last_id}').fetchall()[0][0]
    rabbit_status = cursor.execute(f'SELECT rabbit_status FROM all_data WHERE id = {last_id}').fetchall()[0][0]
    rabbit_version = cursor.execute(f'SELECT rabbit_version FROM all_data WHERE id = {last_id}').fetchall()[0][0]
    redis_status = cursor.execute(f'SELECT redis_status FROM all_data WHERE id = {last_id}').fetchall()[0][0]
    redis_version = cursor.execute(f'SELECT redis_version FROM all_data WHERE id = {last_id}').fetchall()[0][0]
    request_time = cursor.execute(f'SELECT request_time FROM all_data WHERE id = {last_id}').fetchall()[0][0]
    conn.commit()

    message_text = f'{acqpc_status=}\n{acqpc_datasource_status=}\n{autopays_datasource_status=}\n{free_disk_space_procent=}\n{acqpc_ping_status=}\n{rabbit_status=}\n{rabbit_version=}\n{redis_status=}\n{redis_version=}\nВремя последней проверки: {request_time}'
    return message_text


def get_cursor_id(table_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    line_id = cursor.execute(f"select seq from sqlite_sequence where name='{table_name}'").fetchall()[0][0]
    conn.commit()
    return line_id


def get_last_time():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    last_id = get_cursor_id('all_data')
    last_time = cursor.execute(f'SELECT request_time from all_data WHERE id = "{last_id}"').fetchall()[0][0]
    conn.commit()
    return last_time


def _get_state_acqpc_mon():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Првоерим когда в последний раз была запись в БД
    last = datetime.datetime.strptime(get_last_time(), '%d-%m-%Y %H:%M:%S')  # Приводим время к одному формату, чтоб посчитать разницу
    now = datetime.datetime.now()
    time_delay = (now - last).seconds  # Разница между временнем последней записи и текущим временем (в секундах)
    normal_delay = 120  # Нормальной задержкой считаем 70 минут
    if time_delay < normal_delay:
        state_db = 'OK'
    else:
        state_db = f'ERROR. Задержка во времени = {round(time_delay/60, 2)} минут.'
    conn.commit()

    last_id = get_cursor_id('all_data')
    actual_data = cursor.execute(f'SELECT * FROM all_data WHERE id = {last_id}').fetchall()[0]
    if actual_data[1] == '1' and actual_data[2] == '1' and actual_data[3] == '1' and actual_data[5] == '1' and actual_data[6] == '1' and actual_data[8] == '1':
        state_acqpc = 'OK'
    else:
        state_acqpc = 'ERROR. Какой-то компонет потерял статус UP! Проверь алармы.'

    message_text = f'Проверка состояния.\nАктуальность данных: {state_db}\nРелевантность данных: {state_acqpc}'
    return message_text
import sqlite3
import datetime


db_path = '/home/support/soft/postmon_3.1/src/db.sqlite'


def mon_digest():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    id_errors = cursor.execute("SELECT id FROM res_h WHERE status = 'error'").fetchall()
    id_oks = cursor.execute("SELECT id FROM res_h WHERE status = 'ok'").fetchall()
    id_with_format = cursor.execute("SELECT id FROM res_h WHERE status = 'format'").fetchall()
    id_shadow = cursor.execute("SELECT id FROM res_h WHERE status = 'услуга не выведена'").fetchall()
    # Смотрим неопознанные ошибки (которым не присвоилась категория)
    manual_check = cursor.execute(f"SELECT id FROM res_h WHERE status is NULL").fetchall()
    # Подсчитаем общее кол-во проанализированных ПУ
    len_all_table = cursor.execute(f"SELECT id from res_h").fetchall()
    # Посмотрим есть ли ошибки у клиентов категории А
    errors_a = cursor.execute(
        f"SELECT code, status, operation_time FROM res_h  WHERE category = 'A' AND (status = 'Error' OR status = 'услуга не выведена')").fetchall()
    errors_b = cursor.execute(
        f"SELECT code, status, operation_time FROM res_h  WHERE category = 'B' AND (status = 'Error' OR status = 'услуга не выведена')").fetchall()
    conn.commit()

    message_text = f"Всего проанализировано: {len(len_all_table)} ПУ. \nИз них: \n\n{len(id_errors)} - С техническими " \
                   f"ошибками \n{len(id_oks)} - В состоянии OK \n{len(id_with_format)} - Не совпали по формату " \
                   f"запроса проверки\n{len(manual_check)} - Неопознанные ошибки\n{len(id_shadow)} - Услуга не " \
                   f"выведена\n\nКлиентов категории А с ошибками: {len(errors_a)}\nКлиентов категории B  ошибками: {len(errors_b)} "
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

    last_id = get_cursor_id('global_answers_data')
    last_time = cursor.execute(f'SELECT operation_time from global_answers_data WHERE id = "{last_id}"').fetchall()
    conn.commit()
    return last_time[0][0]


def _get_state_postmon():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Првоерим когда в последний раз была запись в БД
    last = datetime.datetime.strptime(get_last_time(), '%d-%m-%Y %H:%M:%S')  # Приводим время к одному формату, чтоб посчитать разницу
    now = datetime.datetime.now()
    time_delay = (now - last).seconds  # Разница между временнем последней записи и текущим временем (в секундах)
    normal_delay = 4200  # Нормальной задержкой считаем 70 минут
    if time_delay < normal_delay:
        state_db = 'OK'
    else:
        state_db = f'ERROR. Задержка во времени = {round(time_delay/60, 2)} минут.'

    last_status = cursor.execute(f'SELECT status FROM global_answers_data WHERE id = {get_cursor_id("global_answers_data")}').fetchall()
    conn.commit()
    if last_status == 'Null':
        state_data = 'ERROR'
    else:
        state_data = 'OK'

    message_text = f'Проверка состояния.\nАктуальность данных: {state_db}\nРелевантность данных: {state_data}'
    return message_text
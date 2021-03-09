import sqlite3
from datetime import datetime
from src.services_manager import do_alarm
from loguru import logger

logger.add(f'src/log/{__name__}.log', format='{time} {level} {message}', level='DEBUG', rotation='10 MB', compression='zip')


db_path = 'src/db.sqlite'
#  Команда для записи данных для анализа:
#         insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
#                                call.from_user.username, call.data.split(':')[1])


def validate_analysis_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    tables = cursor.execute('SELECT name from sqlite_master WHERE type = "table"').fetchall()  # Смотрим какие есть таблицы
    valid_tables = []

    for t in tables:
        valid_tables.append(t[0])

    if 'analysis_data' not in valid_tables:
        cursor.execute('CREATE TABLE "analysis_data" (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, datetime TEXT NOT '
                       'NULL, user_id TEXT NOT NULL, first_name TEXT, last_name TEXT, user_name TEXT NOT NULL, '
                       'button TEXT)')
    else:
        pass
    conn.commit()


def insert_in_analysis_table(user_id, first_name, last_name, user_name, button):
    try:
        validate_analysis_db()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        actualtime = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
        cursor.execute(
            f'INSERT INTO analysis_data VALUES (Null, "{actualtime}", "{user_id}", "{first_name}", "{last_name}", "{user_name}", "{button}")')
        conn.commit()
    except Exception as e:
        t_alarmtext = f'tg_mon_bot (analyzer.py): {str(e)}'
        do_alarm(t_alarmtext)
        logger.error(f'Other except error Exception', exc_info=True)

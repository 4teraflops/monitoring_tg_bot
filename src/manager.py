import subprocess
import config
import requests
import json
from loguru import logger

logger.add(f'log/{__name__}.log', format='{time} {level} {message}', level='DEBUG', rotation='10 MB', compression='zip')


def _system_command(command):
    try:
        command = subprocess.check_output(f'{command}; exit 0', shell=True)
        return command.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return 'Команда \n> {}\nзавершилась с кодом {}'.format(e.cmd, e.returncode)


def do_alarm(t_alarmtext):
    headers = {"Content-type": "application/json"}
    payload = {"text": f"{t_alarmtext}", "chat_id": f"{config.admin_id}"}
    requests.post(url=config.webhook_url, data=json.dumps(payload), headers=headers)

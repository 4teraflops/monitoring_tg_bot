from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import menu_callbacks


start_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Службы мониторинга', callback_data=menu_callbacks.new('menu', click1='mons_menu'))
    ],
    [
        InlineKeyboardButton(text='Автотест demo.ckassa.ru', callback_data=menu_callbacks.new('menu', click1='demo_checker'))
    ],
    [
        InlineKeyboardButton(text='Стукач', callback_data=menu_callbacks.new('menu', click1='news_poster'))
    ]
])

mons_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='acqpc_mon', callback_data='menu:mons_menu:acqpc_mon'),
        InlineKeyboardButton(text='postmon', callback_data='menu:mons_menu:postmon')
    ],
    [
        InlineKeyboardButton(text='webserver', callback_data='menu:mons_menu:webserver'),
        InlineKeyboardButton(text='redis_telnet_mon', callback_data='menu:mons_menu:redis_telnet_mon')
    ],
    [InlineKeyboardButton(text='redis_telnet_mon_db_exporter', callback_data='menu:mons_menu:redis_telnet_mon_db_exporter')],
    [InlineKeyboardButton(text='prometheus-custom-collector', callback_data='menu:mons_menu:prometheus-custom-collector')],
    [InlineKeyboardButton(text="Назад", callback_data='menu:mons_menu:Back')]
])

mon_acqpc_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Дайджест", callback_data='mons_menu:acqpc-mon:digest'),
        InlineKeyboardButton(text="Проверка данных", callback_data='mons_menu:acqpc-mon:state')
    ],
    [
        InlineKeyboardButton(text="Управление", callback_data='mons_menu:acqpc-mon:manage'),
        InlineKeyboardButton(text="Назад", callback_data='mons_menu:acqpc-mon:Back')

    ],
])

postmon_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Дайджест", callback_data='mons_menu:postmon:digest'),
        InlineKeyboardButton(text="Состояние данных", callback_data='mons_menu:postmon:state')
    ],
    [
        InlineKeyboardButton(text="Управление", callback_data='mons_menu:postmon:manage'),
        InlineKeyboardButton(text="Назад", callback_data='mons_menu:postmon:Back')

    ],
])

manage_acqpc_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Старт", callback_data="mons_menu:acqpc-mon:manage:start"),
        InlineKeyboardButton(text="Стоп", callback_data="mons_menu:acqpc-mon:manage:stop"),
    ],
    [
        InlineKeyboardButton(text="Статус", callback_data="mons_menu:acqpc-mon:manage:status"),
        InlineKeyboardButton(text="Рестарт", callback_data="mons_menu:acqpc-mon:manage:restart"),
    ],
    [
        InlineKeyboardButton(text="Назад", callback_data='mons_menu:acqpc-mon:manage:Back')
    ]
])

manage_postmon_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Старт", callback_data="mons_menu:postmon:manage:start"),
        InlineKeyboardButton(text="Стоп", callback_data="mons_menu:postmon:manage:stop"),
    ],
    [
        InlineKeyboardButton(text="Статус", callback_data="mons_menu:postmon:manage:status"),
        InlineKeyboardButton(text="Рестарт", callback_data="mons_menu:postmon:manage:restart"),
    ],
    [
        InlineKeyboardButton(text="Назад", callback_data='mons_menu:postmon:manage:Back')
    ]
])

poster_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Кошелек', callback_data='newsposter:wallet'),
        InlineKeyboardButton(text='Все', callback_data='newsposter:all')
    ],
    [
        InlineKeyboardButton(text='Восстановлено', callback_data='newsposter:fixed')
    ],
    [
        InlineKeyboardButton(text='Назад', callback_data='newsposter:Back')
    ]
])

demo_checker_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Анонимный платеж', callback_data='demo_checker:anon_pay'),
        InlineKeyboardButton(text='Рекуррентный платеж', callback_data='demo_checker:rek_pay')
    ],
    [
        InlineKeyboardButton(text='Фискализация наличных', callback_data='demo_checker:fiscal_pay'),
        InlineKeyboardButton(text='Все', callback_data='demo_checker:all')
    ],
    [InlineKeyboardButton(text='Назад', callback_data='demo_checker:Back')]
])

#S = Sticker(file_id='CAACAgIAAxkBAAEBXjdfba_DDpBbFf2eYSVq6wjkHLhbLQACJQMAArrAlQW6VSV8AAHUde8bBA')
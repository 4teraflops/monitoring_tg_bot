from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Sticker

# from config import URL_APPLES, URL_PEAR
from keyboards.inline.callback_datas import menu_callbacks

# Вариант 1, как в прошлом уроке
# choice = InlineKeyboardMarkup(inline_keyboard=[
#     [
#         InlineKeyboardButton(text="Купить грушу", callback_data=buy_callback.new(item_name="pear")),
#         InlineKeyboardButton(text="Купить яблоки", callback_data="buy:apple")
#     ],
#     [
#         InlineKeyboardButton(text="Отмена", callback_data="next")
#     ]
# ])
#
## А теперь клавиатуры со ссылками на товары
# pear_keyboard = InlineKeyboardMarkup(inline_keyboard=[
#    [
#        InlineKeyboardButton(text="Купи тут", url=URL_APPLES)
#    ]
# ])
# apples_keyboard = InlineKeyboardMarkup(inline_keyboard=[
#    [
#        InlineKeyboardButton(text="Купи тут", url=URL_PEAR)
#    ]
# ])

start_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="ПУ", callback_data=menu_callbacks.new(click1="postmon")),
        InlineKeyboardButton(text="ACQ-PC", callback_data=menu_callbacks.new(click1="acqpc")),
        InlineKeyboardButton(text="Стукач", callback_data=menu_callbacks.new(click1="newsposter"))
    ],
    [
        InlineKeyboardButton(text="Demo checker", callback_data=menu_callbacks.new(click1="demo_checker"))
    ]
])

mon_pu_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Дайджест", callback_data='postmon:digest'),
        InlineKeyboardButton(text="Состояние", callback_data='postmon:state')
    ],
    [
        InlineKeyboardButton(text="Управление", callback_data='postmon:manage'),
        InlineKeyboardButton(text="Назад", callback_data='postmon:Back')

    ],
])

manage_pu_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Старт", callback_data="postmon:manage:start"),
        InlineKeyboardButton(text="Стоп", callback_data="postmon:manage:stop"),
    ],
    [
        InlineKeyboardButton(text="Статус", callback_data="postmon:manage:status"),
        InlineKeyboardButton(text="Рестарт", callback_data="postmon:manage:restart"),
    ],
    [
        InlineKeyboardButton(text="Назад", callback_data='postmon:manage:Back')
    ]
])

mon_acqpc_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Дайджест", callback_data='acqpc:digest'),
        InlineKeyboardButton(text="Состояние", callback_data='acqpc:state')
    ],
    [
        InlineKeyboardButton(text="Управление", callback_data='acqpc:manage'),
        InlineKeyboardButton(text="Назад", callback_data='acqpc:Back')

    ],
])

manage_acqpc_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Старт", callback_data="acqpc:manage:start"),
        InlineKeyboardButton(text="Стоп", callback_data="acqpc:manage:stop"),
    ],
    [
        InlineKeyboardButton(text="Статус", callback_data="acqpc:manage:status"),
        InlineKeyboardButton(text="Рестарт", callback_data="acqpc:manage:restart"),
    ],
    [
        InlineKeyboardButton(text="Назад", callback_data='acqpc:manage:Back')
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
        InlineKeyboardButton(text='Start', callback_data='demo_checker:start'),
        InlineKeyboardButton(text="Назад", callback_data='demo_checker:Back')
    ]
])

#S = Sticker(file_id='CAACAgIAAxkBAAEBXjdfba_DDpBbFf2eYSVq6wjkHLhbLQACJQMAArrAlQW6VSV8AAHUde8bBA')
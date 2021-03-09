import logging
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboards.inline.callback_datas import menu_callbacks
from keyboards.inline.choice_buttons import start_menu, demo_checker_menu
from loader import dp, bot
from states.states import Start, DemoChecker
from extentions.demo_checker import demo_checker as demo_checker_app
from loguru import logger
from src.analyzer import insert_in_analysis_table

logger.add(f'log/{__name__}.log', format='{time} {level} {message}', level='DEBUG', rotation='10 MB', compression='zip')


@dp.callback_query_handler(menu_callbacks.filter(click1='demo_checker'), state=Start.Start_menu)
async def demo_checker(call: CallbackQuery, state: FSMContext):
    await state.get_state()
    text = 'Demo Checker:'
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text)
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=demo_checker_menu)

    insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                             call.from_user.username, call.data.split(':')[1])  # В анализ

    await DemoChecker.Start.set()


@dp.callback_query_handler(state=DemoChecker.Start)
async def start_demo_checker(call: CallbackQuery, state: FSMContext):
    await state.get_state()
    button_callback = call.data.split(":")[1]
    if button_callback == 'Back':
        text = 'Привет! Выбирай кнопку'
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text)
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            reply_markup=start_menu)
        await state.get_state()
        await Start.Start_menu.set()

        insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                                 call.from_user.username, call.data.split(':')[1])  # В анализ
    elif button_callback == 'start':
        # Убираем клавиатуру
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup='')
        # Сообщаем, чтоб ждал (сообщением и алертом)
        await bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
                                        text='Автотест запущен.\nОжидайте около минуты.', cache_time=10)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Start testing...\n')
        # Когда функции автотеста отработали возвращаем их вывод и клавиатуру
        await call.message.answer(text=demo_checker_app.autotest_anonimus_pay())
        await call.message.answer(text=demo_checker_app.autotest_rekurrent_pay())
        await call.message.answer(text=demo_checker_app.autotest_fiscal_cash_pay())
        await call.message.answer(text='End testing', reply_markup=demo_checker_menu)

        insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                                 call.from_user.username, call.data.split(':')[1])  # В анализ

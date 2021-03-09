from config import admin_id
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from keyboards.inline.callback_datas import menu_callbacks
from keyboards.inline.choice_buttons import start_menu, mon_pu_menu, manage_pu_menu, mon_acqpc_menu, manage_acqpc_menu
from loader import dp, bot
from src.selector_postmon import mon_digest, _get_state_postmon
from src.selector_acqpc_mon import _get_state_acqpc_mon, _acqpc_mon_digest
from src.services_manager import _system_command
from states.states import Pu, ACQPC, Start
from src.analyzer import insert_in_analysis_table
from loguru import logger

logger.add(f'src/log/{__name__}.log', format='{time} {level} {message}', level='DEBUG', rotation='10 MB', compression='zip')


@dp.callback_query_handler(menu_callbacks.filter(click1='postmon'), state=Start.Start_menu)  # Ловим State и callback
async def postmon_menu(call: CallbackQuery, state: FSMContext):
    await state.get_state()

    # Отобразим что у нас лежит в callback_data
    # logger.info(f'callback_data_type={call.data.split(":")[1]}')  # Задаю разделитель ":" и вывел второй элемент массива

    text = 'Доступные инструменты:'
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text=text)  # Меняем текст в сообщении
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        reply_markup=mon_pu_menu)  # Меняем клавиатуру в сообщении
    await Pu.Tools.set()  # Присваиваем состояние

    # В анализ
    insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                             call.from_user.username, call.data.split(':')[1])


@dp.callback_query_handler(menu_callbacks.filter(click1='acqpc'), state=Start.Start_menu)  # Ловим State и callback
async def acqpc_mon_menu(call: CallbackQuery, state: FSMContext):
    await state.get_state()
    # Укажем cache_time, чтобы бот не получал какое-то время апдейты, тогда нижний код не будет выполняться.
    # await call.answer(cache_time=60)
    # Отобразим что у нас лежит в callback_data
    # logger.info(f'callback_data_type={call.data.split(":")[1]}')  # Задаю разделитель ":" и вывел второй элемент массива

    text = 'Доступные инструменты:'
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text=text)  # Меняем текст в сообщении
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        reply_markup=mon_acqpc_menu)  # Меняем клавиатуру в сообщении
    await ACQPC.Tools.set()  # Присваиваем состояние

    # В анализ
    insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                             call.from_user.username, call.data.split(':')[1])


@dp.callback_query_handler(state=Pu.Tools)
async def pu_tools(call: CallbackQuery, state: FSMContext):
    button_callback = call.data.split(":")[1]
    await state.get_state()

    if button_callback == 'Back':
        text = 'Привет! Выбирай кнопку'
        # Меняем текст в сообщении
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text)
        # Меняем клавиатуру в сообщении
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            reply_markup=start_menu)
        await state.get_state()
        await Start.Start_menu.set()

        # В анализ
        insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                                 call.from_user.username, call.data.split(':')[1])

    elif button_callback == 'digest':
        text = mon_digest()
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text)
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            reply_markup=mon_pu_menu)

        # В анализ
        insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                                 call.from_user.username, call.data.split(':')[1])
    elif button_callback == 'state':
        text = _get_state_postmon()
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text)
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            reply_markup=mon_pu_menu)

        # В анализ
        insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                                 call.from_user.username, call.data.split(':')[1])
    elif button_callback == 'manage':
        text = 'Доступные команды:'
        # Меняем текст в сообщении
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text)
        # Меняем клавиатуру в сообщении
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            reply_markup=manage_pu_menu)
        await state.get_state()
        await Pu.Manage.set()
        # В анализ
        insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                                 call.from_user.username, call.data.split(':')[1])


@dp.callback_query_handler(state=ACQPC.Tools)
async def acqpc_tools(call: CallbackQuery, state: FSMContext):
    button_callback = call.data.split(":")[1]
    await state.get_state()

    if button_callback == 'Back':
        text = 'Привет! Выбирай кнопку'
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text=text)  # Меняем текст в сообщении
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            reply_markup=start_menu)  # Меняем клавиатуру в сообщении
        await state.get_state()
        await Start.Start_menu.set()  # Меняем состояние на первое

        # В анализ
        insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                                 call.from_user.username, call.data.split(':')[1])

    elif button_callback == 'digest':
        text = _acqpc_mon_digest()
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text)
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            reply_markup=mon_acqpc_menu)

        # В анализ
        insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                                 call.from_user.username, call.data.split(':')[1])
    elif button_callback == 'state':
        text = _get_state_acqpc_mon()
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text)
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            reply_markup=mon_acqpc_menu)

        # В анализ
        insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                                 call.from_user.username, call.data.split(':')[1])
    elif button_callback == 'manage':
        text = 'Доступные команды:'
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text)
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            reply_markup=manage_acqpc_menu)
        await state.get_state()
        await ACQPC.Manage.set()
        # В анализ
        insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                                 call.from_user.username, call.data.split(':')[1])


@dp.callback_query_handler(state=Pu.Manage)
async def postmon_manage(call: CallbackQuery, state: FSMContext):
    await state.get_state()
    user_id = call.from_user.id
    button_callback = call.data.split(":")[2]
    if button_callback == 'Back':
        text = 'Доступные инструменты:'
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text=text)  # Меняем текст в сообщении
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            reply_markup=mon_pu_menu)  # Меняем клавиатуру в сообщении
        await state.get_state()
        await Pu.Tools.set()  # Присваиваем нужное состояние

        # В анализ
        insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                                 call.from_user.username, call.data.split(':')[2])

    elif button_callback == 'status':
        if user_id == admin_id:
            text = _system_command('service postmon status')
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text)
            await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                                reply_markup=manage_pu_menu)

            # В анализ
            insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                                     call.from_user.username, call.data.split(':')[2])
        else:
            await call.message.answer(f'Ты не админ. Иди отсюда.')
    elif button_callback == 'start':

        # В анализ
        insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                                 call.from_user.username, call.data.split(':')[2])

        if user_id == admin_id:
            _system_command('service postmon start')
        else:
            await call.message.answer('Ты не админ. Иди отсюда.')
    elif button_callback == 'stop':

        # В анализ
        insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                                 call.from_user.username, call.data.split(':')[2])

        if user_id == admin_id:
            _system_command('service postmon stop')
        else:
            await call.message.answer('Ты не админ. Иди отсюда.')
    elif button_callback == 'restart':

        # В анализ
        insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                                 call.from_user.username, call.data.split(':')[2])

        if user_id == admin_id:
            _system_command('service postmon restart')
        else:
            await call.message.answer('Ты не админ. Иди отсюда.')


@dp.callback_query_handler(state=ACQPC.Manage)
async def acqpc_manage(call: CallbackQuery, state: FSMContext):
    await state.get_state()
    user_id = call.from_user.id
    button_callback = call.data.split(":")[2]
    if button_callback == 'Back':
        text = 'Доступные инструменты:'
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text=text)  # Меняем текст в сообщении
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                            reply_markup=mon_acqpc_menu)  # Меняем клавиатуру в сообщении
        await state.get_state()
        await ACQPC.Tools.set()  # Присваиваем нужное состояние

        # В анализ
        insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                                 call.from_user.username, call.data.split(':')[2])

    elif button_callback == 'status':

        # В анализ
        insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                                 call.from_user.username, call.data.split(':')[2])

        if user_id == admin_id:
            text = _system_command('service acqpc_mon status')
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text=text)
            await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                                reply_markup=manage_acqpc_menu)
        else:
            await call.message.answer('Ты не админ. Иди отсюда.')
    elif button_callback == 'start':

        # В анализ
        insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                                 call.from_user.username, call.data.split(':')[2])

        if user_id == admin_id:
            _system_command('service acqpc_mon start')
        else:
            await call.message.answer('Ты не админ. Иди отсюда.')
    elif button_callback == 'stop':

        # В анализ
        insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                                 call.from_user.username, call.data.split(':')[2])

        if user_id == admin_id:
            _system_command('service acqpc_mon stop')
        else:
            await call.message.answer('Ты не админ. Иди отсюда.')
    elif button_callback == 'restart':

        # В анализ
        insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                                 call.from_user.username, call.data.split(':')[2])

        if user_id == admin_id:
            _system_command('service acqpc_mon restart')
        else:
            await call.message.answer('Ты не админ. Иди отсюда.')


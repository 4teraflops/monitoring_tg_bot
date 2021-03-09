from config import news_channel_id
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from keyboards.inline.callback_datas import menu_callbacks
from keyboards.inline.choice_buttons import poster_menu, start_menu
from loader import dp, bot
from states.states import Start, NewsPoster
from src.analyzer import insert_in_analysis_table
from loguru import logger

logger.add(f'src/log/{__name__}.log', format='{time} {level} {message}', level='DEBUG', rotation='10 MB', compression='zip')


@dp.callback_query_handler(menu_callbacks.filter(click1='newsposter'), state=Start.Start_menu)  # Ловим State и callback
async def news_poster_menu(call: CallbackQuery, state: FSMContext):
    await state.get_state()
    text = 'С чем проблемы?'
    # Меняем текст в сообщении
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text)
    # Меняем клавиатуру в сообщении
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=poster_menu)
    await NewsPoster.Choise_command.set()

    # В анализ
    insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name, call.from_user.username, call.data.split(':')[1])


@dp.callback_query_handler(state=NewsPoster.Choise_command)
async def news_poster(call: CallbackQuery, state: FSMContext):
    button_callback = call.data.split(':')[1]

    if button_callback == 'Back':
        text = 'Привет! Выбирай кнопку'
        # Меняем текст в сообщении
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text)
        # Меняем клавиатуру в сообщении
        await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=start_menu)
        await state.get_state()
        await Start.Start_menu.set()
        # В анализ
        insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                                 call.from_user.username, call.data.split(':')[1])

    elif button_callback == 'wallet':
        text = 'Наблюдаем технические сложности в работе электронного кошелька. Могут быть задержки в зачислении/списании, некорректный баланс.\nМы уже локализовали проблему и работаем над ее решением. О восстановлении напишем отдельно.'
        await bot.send_message(chat_id=news_channel_id, text=text)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Сообщение отправлено')
        await call.message.answer(text='Выбери что отправить:', reply_markup=poster_menu)
        # В анализ
        insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                                 call.from_user.username, call.data.split(':')[1])
        await state.get_state()
        await NewsPoster.Choise_command.set()

    elif button_callback == 'all':
        text = 'Фиксируем технические трудности в проведении онлайн-платежей.\nМогут быть двойные списания (при создании платежей с заморозкой), задержки в проведении онлайн-платежей, либо отказы при попытке создать платеж.\nНе проведенные платежи складываются в очередь, мы уже работаем над устранением причин и последствий.\nО восстановлении сообщим дополнительно.'
        await bot.send_message(chat_id=news_channel_id, text=text)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Сообщение отправлено')
        await call.message.answer(text='Выбери что отправить:', reply_markup=poster_menu)
        # В анализ
        insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                                 call.from_user.username, call.data.split(':')[1])
        await state.get_state()
        await NewsPoster.Choise_command.set()

    elif button_callback == 'fixed':
        text = 'Вернулись в штатный режим работы.'
        await bot.send_message(chat_id=news_channel_id, text=text)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Сообщение отправлено')
        await call.message.answer(text='Выбери что отправить:', reply_markup=poster_menu)
        # В анализ
        insert_in_analysis_table(call.from_user.id, call.from_user.first_name, call.from_user.last_name,
                                 call.from_user.username, call.data.split(':')[1])
        await state.get_state()
        await NewsPoster.Choise_command.set()


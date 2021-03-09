from config import access_list
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ContentTypes
from keyboards.inline.choice_buttons import start_menu
from loader import dp
from states.states import Start
from src.analyzer import insert_in_analysis_table
from loguru import logger

logger.add(f'src/log/{__name__}.log', format='{time} {level} {message}', level='DEBUG', rotation='10 MB', compression='zip')


@dp.message_handler(Command('start'))
async def show_start_menu(message: Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton(text="Подтвердить свой номер", request_contact=True))
    await message.answer("Подтверди свой номер", reply_markup=keyboard)
    await Start.Auth.set()


@dp.message_handler(Command('reset'), state="*")
async def reset_states(message: Message):
    await message.answer(text="Состояния сброшены. Возврат к авторизации...")
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton(text="Подтвердить свой номер", request_contact=True))
    await message.answer("Подтверди свой номер", reply_markup=keyboard)
    await Start.Auth.set()


@dp.callback_query_handler(state=None)
async def lost_state(call: CallbackQuery, state: FSMContext):
    await state.get_state()
    await call.message.answer(text='Сервер перезапускался, состояния сброшены.\nСейчас вы будете перенаправлены на сценарий авторизации.\nНажми на "подтвердить свой номер".')
    #logger.info(f'state пойман" {state}')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton(text="Подтвердить свой номер", request_contact=True))
    #await call.message.answer(text='Подтверди свой номер')
    #await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id, reply_markup=keyboard)
    await call.message.answer("Подтверди свой номер", reply_markup=keyboard)
    await Start.Auth.set()


@dp.message_handler(content_types=ContentTypes.CONTACT, state=Start.Auth)
async def auth(message: Message, state: FSMContext):
    await state.get_state()
    user_phone = message.contact.phone_number
    #logger.info(f'user_phone:{user_phone}')
    if user_phone in access_list:
        text = 'Привет! Выбирай кнопку'
        await message.answer(text=text, reply_markup=start_menu)
        await Start.Start_menu.set()
        # В анализ
        insert_in_analysis_table(message.from_user.id, message.from_user.first_name, message.from_user.last_name,
                                 message.from_user.username, 'login_Success')
    else:
        await message.answer_video(video='BAACAgIAAxkBAAIFmGA_ghnJJb0Owq5Ph2EHHp4ErZ79AAIzDAACOQEBSjctoPs_xUjSHgQ')
        # В анализ
        insert_in_analysis_table(message.from_user.id, message.from_user.first_name, message.from_user.last_name,
                                 message.from_user.username, 'login_Error')

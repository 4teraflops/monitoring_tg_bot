from aiogram.dispatcher.filters.state import StatesGroup, State


class Start(StatesGroup):
    Auth = State()
    Phone = State()
    Start_menu = State()


class Mons(Start):
    Mons_menu = State()


class ACQPC(Mons):
    Tools = State()
    Manage = State()


class Postmon(Mons):
    Tools = State()
    Manage = State()


class NewsPoster(Start):
    Choise_command = State()


class DemoChecker(Start):
    Methods = State()
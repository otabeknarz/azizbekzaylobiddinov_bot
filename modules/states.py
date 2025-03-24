from aiogram.fsm.state import State, StatesGroup


class RegistrationState(StatesGroup):
    name = State()
    phone_number = State()

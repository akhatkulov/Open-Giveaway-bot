from aiogram.filters.state import StatesGroup, State


class AdminState(StatesGroup):
    are_you_sure = State()
    ask_ad_content = State()
    Add_Channel = State()
    Delete_Channel = State()


class UserState(StatesGroup):
    send_number = State()


class PanelState(StatesGroup):
    add_channel = State()
    delete_channel = State()
    ask_giweaway_period = State()

from aiogram.dispatcher.filters.state import State, StatesGroup

class States(StatesGroup):
    start = State()
    public = State()
    source = State()
    private = State()
    phone = State()
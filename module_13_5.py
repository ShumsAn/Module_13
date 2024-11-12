from aiogram import Bot,Dispatcher,executor,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.types import ReplyKeyboardMarkup,KeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Информация')

button2 = KeyboardButton(text='Рассчитать')
kb.row(button,button2)


@dp.message_handler(commands=['start'])
async def start_message(message):
     await message.answer("Привет, я бот помогающий твоему здоровью.",reply_markup= kb)


@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer(f'Информация:\n'
                         f'Бот умеет рассчитывать вашу дневную норму калорий по формуле Миффлина - Сан Жеора\n'
                         f'Для использования этой функции воспользуйтесь командой "Рассчитать"')

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(text="Рассчитать")
async def set_age(message):
    await message.answer("Введите свой возраст:")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def  set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def  send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    await state.finish()
    calorie_allowance_men = float(data['weight']) * 10 + float(data['growth']) * 6.25 - float(data['age']) * 4.92 + 5
    calorie_allowance_women = float(data['weight']) * 10 + float(data['growth']) * 6.25 - float(data['age']) * 4.92-161
    await message.answer(f'Мужская норма калорий: {calorie_allowance_men}')
    await message.answer(f'Женская норма калорий: {calorie_allowance_women}')



@dp.message_handler()
async def all_message(message):
       await message.answer(f'Введите команду /start, чтобы начать общение.')

if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True)



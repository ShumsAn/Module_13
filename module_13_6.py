from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Информация')
button2 = KeyboardButton(text='Рассчитать')
kb.row(button, button2)

button3 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb2 = InlineKeyboardMarkup(row_width=2).add(button3)
kb2.add(InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'))

kb3 = InlineKeyboardMarkup(resize_keyboard=True)
button5 = InlineKeyboardButton(text='М', callback_data='men')
button6 = InlineKeyboardButton(text='Ж', callback_data='women')
kb3.add(button5, button6)

start = False

@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer("Привет, я бот помогающий твоему здоровью.", reply_markup=kb)
    global start
    start = True

@dp.callback_query_handler(text='formulas')
async def get_formulas(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(
        callback_query.id,
        text='для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5; \n'
             'для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161 😉', show_alert=True)

@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer(f'Информация:\n'
                         f'Бот умеет рассчитывать вашу дневную норму калорий по формуле Миффлина - Сан Жеора\n'
                         f'Для использования этой функции воспользуйтесь командой "Рассчитать"')

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выбрать опцию:', reply_markup=kb2)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()

@dp.callback_query_handler(text='calories')
async def set_gender(call):
    await call.message.answer('Выбрать пол:', reply_markup=kb3)
    await call.answer()
    await UserState.gender.set()

@dp.callback_query_handler(text=('men', 'women'), state=UserState.gender)
async def set_age(call, state):
    await state.update_data(gender=call.data)
    await call.answer()
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await state.finish()
    try:
        if data['gender'] == 'men':
            calorie_allowance_men = float(data['weight']) * 10 + float(data['growth']) * 6.25 - float(
                data['age']) * 4.92 + 5
            await message.answer(f'Мужская норма калорий: {calorie_allowance_men}')
        elif data['gender'] == 'women':
            calorie_allowance_women = float(data['weight']) * 10 + float(data['growth']) * 6.25 - float(
                data['age']) * 4.92 - 161
            await message.answer(f'Женская норма калорий: {calorie_allowance_women}')
    except:
        print('Пользователь передал не верные данные')
        await message.answer(f'Что-то пошло не так.\n Попробуйте заново нажать кнопку рассчитать норму')

@dp.message_handler()
async def all_message(message):
    if start == False:
        await message.answer(f'Введите команду /start, чтобы начать общение.')
    else:
        await message.answer(message.text + ' - Не знаю такой команды')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

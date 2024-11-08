from aiogram import Bot,Dispatcher,executor,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

#Немного ушли от тз, но не сильно
start = False
name_user = ''

@dp.message_handler(commands=['start'])
async def start_message(message):
        await message.answer(f"Привет , я бот помогающий твоему здоровью.")
        await message.answer(f" Как к тебе можно обращаться?")
        global start
        start = True

@dp.message_handler()
async def all_message(message):
    global name_user
    if start == False:
        await message.answer(f'Введите команду /start, чтобы начать общение.')
    elif start == True and name_user == '':
        name_user = message.text
        await message.answer(f'{name_user} Какие способы повышения здоровья тебе известны?')
    elif start == True and name_user != '':
        await message.answer(message.text + ', дело хорошее, я также тебе рекомендую заниматься спортом')


if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True)
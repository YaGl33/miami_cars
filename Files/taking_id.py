from aiogram import Dispatcher, executor, types
from aiogram.bot import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import logging

logging.basicConfig(level=logging.INFO)
API = "5658004976:AAE94u4W9N9PK4f-rYhxvGfa83t7cjAAptA"
bot = Bot(API)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def foo(message: types.Message):
    await message.answer(message.from_user.id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

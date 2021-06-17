import logging
import os

from aiogram import Bot, Dispatcher, types, executor
from messages import START_MESSAGE


TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
logging.basicConfig(level=logging.INFO)

bot = Bot(TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_walcome(message: types.Message):
    '''Отправляет приветственное сообщение пользователю'''

    await message.answer(START_MESSAGE)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
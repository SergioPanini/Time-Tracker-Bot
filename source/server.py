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
    m = types.InlineKeyboardMarkup()
    m.add(types.InlineKeyboardButton(text='Activity1', callback_data='1' ), types.InlineKeyboardButton(text='start', callback_data='1' ))
    
    m.add(types.InlineKeyboardButton(text='<', callback_data='<' ), types.InlineKeyboardButton(text='>', callback_data='>' ))

    await message.answer(START_MESSAGE, reply_markup=m)

@dp.callback_query_handler()
async def set_activety(callback_query: types.CallbackQuery):

    print('get callback: ', callback_query)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
import logging
import os
import typing

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import reply_keyboard
from aiogram.types.message import Message
from messages import START_MESSAGE

from db import add_user, add_activity, get_user_activities
from services import get_activities_keyboard, get_main_keyboard


TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
logging.basicConfig(level=logging.INFO)

bot = Bot(TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

set_activety_user_dict = {}


@dp.message_handler(commands=['start', 'help'])
async def send_walcome(message: types.Message):
    '''Отправляет приветственное сообщение пользователю'''

    add_user(message.chat.id)

    user_activities = get_user_activities(message.chat.id)
    print('Активность пользователя: ', user_activities)
    start_keyboard = get_activities_keyboard(message.chat.id)
    static_keyboard = get_main_keyboard()

    await message.answer('🖐🏻', reply_markup=static_keyboard)
    await message.answer(START_MESSAGE, reply_markup=start_keyboard)


@dp.message_handler(commands=['console'])
async def show_main_console(message: types.Message):
    '''Отправляет основную консоль'''
    await message.answer(text='Панель управления временем', reply_markup=get_activities_keyboard(message.chat.id))

@dp.callback_query_handler()
async def activety_select(callback_query: types.CallbackQuery):
    '''Callback на кнопки добавления активности'''

    if callback_query.data == "Add_new_activities":
        await bot.send_message(chat_id=callback_query.message.chat.id, text='Введите название активности')

        # Сохраняем флаг, что следующее сообщени пользователя будет активность
        set_activety_user_dict[callback_query.message.chat.id] = True


@dp.message_handler()
async def set_activety(message: types.Message):
    '''Запись новой активности от пользователя в бд'''

    if set_activety_user_dict.get(message.chat.id) == True:
        set_activety_user_dict[message.chat.id] = False
        await message.answer(text='Запомнил %s' % message.text)

        add_activity(chat_id=message.chat.id, activity=message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

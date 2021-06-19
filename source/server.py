import logging
import os

from aiogram import Bot, Dispatcher, types, executor
from messages import START_MESSAGE

from db import add_user, add_activity, get_user_activities

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
logging.basicConfig(level=logging.INFO)

bot = Bot(TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

set_activety_user_dict = {}

@dp.message_handler(commands=['start', 'help'])
async def send_walcome(message: types.Message):
    '''Отправляет приветственное сообщение пользователю и главный экран'''
    m = types.InlineKeyboardMarkup()
    
    m.add(types.InlineKeyboardButton(text='Добавить активность', callback_data='add' ))
    #m.add(types.InlineKeyboardButton(text='<', callback_data='<' ), types.InlineKeyboardButton(text='>', callback_data='>' ))
    
    #m.add(types.InlineKeyboardButton(text='Activity1', callback_data='1' ), types.InlineKeyboardButton(text='start', callback_data='1' ))
    #m.add(types.InlineKeyboardButton(text='Activity2', callback_data='2' ), types.InlineKeyboardButton(text='start', callback_data='2' ))
    #m.add(types.InlineKeyboardButton(text='Activity3', callback_data='3' ), types.InlineKeyboardButton(text='start', callback_data='3' ))
    
    add_user(message.chat.id)

    user_activities = get_user_activities(message.chat.id)
    print(user_activities)

    await message.answer(START_MESSAGE, reply_markup=m)

@dp.callback_query_handler()
async def activety_select(callback_query: types.CallbackQuery):
    '''Callback на кнопки главного экрана'''

    await callback_query.answer(text='good')
    print('get callback: ', callback_query.message.reply_markup)
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Введите название активности')
    set_activety_user_dict[callback_query.message.chat.id] = True

@dp.message_handler()
async def set_activety(message: types.Message):
    '''Получает название новой активности от пользователя''' 
    
    if set_activety_user_dict.get(message.chat.id) == True: 
        set_activety_user_dict[message.chat.id] = False
        await message.answer(text='Запомнил %s' % message.text)

        add_activity(chat_id=message.chat.id, activity=message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
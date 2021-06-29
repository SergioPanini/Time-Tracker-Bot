import logging
import os
import typing

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import reply_keyboard
from aiogram.types.message import Message
from messages import START_MESSAGE

from db import add_user, add_activity, get_user_activities, start_activity, show_all
from services import get_activities_console, get_main_keyboard, DontShowPage


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
    start_keyboard = get_activities_console(message.chat.id)
    static_keyboard = get_main_keyboard()

    await message.answer('🖐🏻', reply_markup=static_keyboard)
    await message.answer(START_MESSAGE, reply_markup=start_keyboard)


@dp.message_handler(commands=['console'])
async def show_main_console(message: types.Message):
    '''Отправляет основную консоль'''
    await message.answer(text='Панель управления временем', reply_markup=get_activities_console(message.chat.id))

#@dp.callback_query_handler(lambda callback_query: callback_query.data.split(':')[0] in ['START', 'STOP'])
#async await

@dp.callback_query_handler(lambda callback_query: callback_query.data.split(':')[0] in ['<', '>'] )
async def main_comsole_move(callback_query: types.CallbackQuery):
    '''Показывает новые активности на консоли'''

    #Получаем  номер страницы, которую нужно показать 
    page = callback_query.data.split(':')[1]
    
    try:
        #Создаем новую клавиатуру
        new_keyboard = get_activities_console(callback_query.message.chat.id, int(page))
        await callback_query.message.edit_reply_markup(new_keyboard)
        await callback_query.answer('Готово')

    except DontShowPage:
        await callback_query.answer('Больше нет активностей')

@dp.callback_query_handler(lambda callback_query: callback_query.data == "Add_new_activities")
async def activety_select(callback_query: types.CallbackQuery):
    '''Callback на кнопки добавления активности'''

    await bot.send_message(chat_id=callback_query.message.chat.id, text='Введите название активности')
    await callback_query.answer('Введите активность')
        
    # Сохраняем флаг, что следующее сообщени пользователя будет активность
    set_activety_user_dict[callback_query.message.chat.id] = True

@dp.callback_query_handler(lambda callback_query: callback_query.data.split(':')[0] in ['START', 'STOP'])
async def start_stop_activities(callback_query: types.CallbackQuery):
    '''Включает и выключает отслеживание активностей'''

    #Получаем активность и задачу для отслеживания(начать или прекратить)
    command, activity = callback_query.data.split(':')

    print('I get calback acti', command, activity)
    
    if command == "START":
        start_activity(callback_query.message.chat.id, activity)
        show_all()
    else:
 #       stop_activity(callback_query.message.chat.id, activity)
        pass
@dp.message_handler()
async def set_activety(message: types.Message):
    '''Запись новой активности от пользователя в бд'''

    if set_activety_user_dict.get(message.chat.id) == True:
        set_activety_user_dict[message.chat.id] = False
        await message.answer(text='Запомнил %s' % message.text)

        add_activity(chat_id=message.chat.id, activity=message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

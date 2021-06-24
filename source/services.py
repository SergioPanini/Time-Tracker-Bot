import os
from db import get_user_activities
from aiogram import types

SHOW_ACTIVITIES_SIZE = os.getenv('SHOW_ACTIVITIES_SIZE')


def get_activities_keyboard(chat_id: int):
    '''Создает главную клавитатуру'''

    START_KEYBOARD = types.InlineKeyboardMarkup()

    START_KEYBOARD.add(types.InlineKeyboardButton(
        text='Добавить активность', callback_data='Add_new_activities'))

    user_activities = get_user_activities(chat_id)

    for i in user_activities:
        print(i)
        START_KEYBOARD.add(types.InlineKeyboardButton(text=str(i), callback_data=str(
            i)), types.InlineKeyboardButton(text='Start', callback_data='START-' + str(i)))

        # START_KEYBOARD.add(types.InlineKeyboardButton(text=i, callback_data=i),
        #                   types.InlineKeyboardButton(text='Start', callback_data='START'))

    START_KEYBOARD.add(types.InlineKeyboardButton(text='<', callback_data='<'),
                       types.InlineKeyboardButton(text='>', callback_data='>'))

    return START_KEYBOARD


def get_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add(types.KeyboardButton(text='/console'))

    return keyboard
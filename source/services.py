import os
from db import get_user_activities
from aiogram import types

SHOW_ACTIVITIES_SIZE = int(os.getenv('SHOW_ACTIVITIES_SIZE'))
print('show....', SHOW_ACTIVITIES_SIZE)

def get_activities_keyboard(chat_id: int, _list=0):
    '''Создает главную клавитатуру'''

    START_KEYBOARD = types.InlineKeyboardMarkup()

    START_KEYBOARD.add(types.InlineKeyboardButton(
        text='Добавить активность', callback_data='Add_new_activities'))

    user_activities = get_user_activities(chat_id)

    print(user_activities[_list * SHOW_ACTIVITIES_SIZE : (_list + 1) * SHOW_ACTIVITIES_SIZE])
    for i in user_activities[_list * SHOW_ACTIVITIES_SIZE : (_list + 1) * SHOW_ACTIVITIES_SIZE ]:
        print(i)
        START_KEYBOARD.add(types.InlineKeyboardButton(text=str(i), callback_data=str(
            i)), types.InlineKeyboardButton(text='Start', callback_data='START-' + str(i)))

    #Создание кнопок управления

    #Проверяем, есть ли что то на след странице
    if user_activities[(_list + 1) * SHOW_ACTIVITIES_SIZE : (_list + 2) * SHOW_ACTIVITIES_SIZE]:
        right_wall = _list + 1
    else:
        right_wall = _list
    
    #Проверяем, есть ли что то на предыдущ странице
    if user_activities[(_list - 1) * SHOW_ACTIVITIES_SIZE : _list * SHOW_ACTIVITIES_SIZE]:
        left_wall = _list - 1
    else:
        left_wall = _list


    START_KEYBOARD.add(types.InlineKeyboardButton(text='<', callback_data='<:' + str(left_wall)),
                       types.InlineKeyboardButton(text='>', callback_data='>:' + str(right_wall)))

    return START_KEYBOARD


def get_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add(types.KeyboardButton(text='/console'))

    return keyboard
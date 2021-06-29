import os
from db import get_user_activities
from aiogram import types

SHOW_ACTIVITIES_SIZE = int(os.getenv('SHOW_ACTIVITIES_SIZE'))

class DontShowPage(Exception):
    pass

def get_activities_console(chat_id: int, page=0):
    '''Создает консоль управления'''

    #Проверяем список активностей пользовтеля
    user_activities = get_user_activities(chat_id)

    if _check_show_page_activities(user_activities, page):
        return _build_new_page_activities(user_activities, page)
    else:
        raise DontShowPage()
    

def _check_show_page_activities(user_activities: list, page: int):
    '''Проверяем есть ли активности на странице что бы их показать '''

    return True if user_activities[page * SHOW_ACTIVITIES_SIZE: (page + 1) * SHOW_ACTIVITIES_SIZE] else False

def _build_new_page_activities(user_activities, page):
    '''Собираем клавиатуру'''

    #Инициализируем клавиатуру
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(
        text='Добавить активность', callback_data='Add_new_activities'))

    #Собираем клавиатуру активностей
    for i in user_activities[page * SHOW_ACTIVITIES_SIZE : (page + 1) * SHOW_ACTIVITIES_SIZE ]:
        keyboard.add(types.InlineKeyboardButton(text=str(i), callback_data=str(
            i)), types.InlineKeyboardButton(text='Start', callback_data='START-' + str(i)))
    
    #Создаем кнопки управления
    keyboard.add(types.InlineKeyboardButton(text='<', callback_data='<:' + str(page - 1)),
                       types.InlineKeyboardButton(text='>', callback_data='>:' + str(page + 1)))
    
    return keyboard




def get_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add(types.KeyboardButton(text='/console'))

    return keyboard
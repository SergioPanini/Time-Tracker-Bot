import os
from db import get_user_activities, check_start_activity
from aiogram import types

SHOW_ACTIVITIES_SIZE = int(os.getenv('SHOW_ACTIVITIES_SIZE'))


class DontShowPage(Exception):
    pass


def get_activities_console(chat_id: int, page=0):
    '''Создает консоль управления'''

    # Проверяем список активностей пользовтеля
    user_activities = get_user_activities(chat_id)

    if _check_show_page_activities(user_activities, page):
        return _build_new_page_activities(user_activities, page, chat_id)
    else:
        raise DontShowPage()


def _check_show_page_activities(user_activities: list, page: int):
    '''Проверяем есть ли активности на странице что бы их показать '''

    return True if user_activities[page * SHOW_ACTIVITIES_SIZE: (page + 1) * SHOW_ACTIVITIES_SIZE] else False


def _build_new_page_activities(user_activities: list, page: int, chat_id: int):
    '''Собираем клавиатуру'''

    # Инициализируем клавиатуру
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(
        text='Добавить активность', callback_data='Add_new_activities'))

    # Собираем клавиатуру активностей
    for i in user_activities[page * SHOW_ACTIVITIES_SIZE: (page + 1) * SHOW_ACTIVITIES_SIZE]:
        #Проверяем отслеживание активности
        status_activity = 'STOP' if check_start_activity(
            chat_id, i) else 'START'

        #Создаем клавиатуру
        keyboard.add(types.InlineKeyboardButton(text=i,
            callback_data=status_activity + ":" + i),\
             types.InlineKeyboardButton(text=status_activity, callback_data=status_activity + ":" + i))

    # Создаем кнопки управления
    keyboard.add(types.InlineKeyboardButton(text='<', callback_data='<:' + str(page - 1)),
                       types.InlineKeyboardButton(text='>', callback_data='>:' + str(page + 1)))

    return keyboard

def get_console():
    '''Возвращяет кнопку с командой вывода консоли'''
    
    keyboard=types.ReplyKeyboardMarkup()
    keyboard.add(types.KeyboardButton(text='/console'))

    return keyboard

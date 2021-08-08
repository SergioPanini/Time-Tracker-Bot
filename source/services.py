import os
from db import get_user_activities, check_start_activity, delete_activities_db
from aiogram import types

SHOW_ACTIVITIES_SIZE = int(os.getenv('SHOW_ACTIVITIES_SIZE'))


class DontGetPage(Exception):
    pass


users_selected_delete_button = {}


def get_activities_console(chat_id: int, page=0):
    '''Создает консоль управления'''

    # Проверяем список активностей пользовтеля
    user_activities = get_user_activities(chat_id)

    if _check_show_page_activities(user_activities, page):
        return _build_page_activities(page, chat_id)
    else:
        raise DontGetPage()


def get_delete_activities_console(chat_id: int, page=0):
    '''Создает консоль удаления активностей'''

    # Проверяем список активностей пользовтеля
    user_activities = get_user_activities(chat_id)

    if _check_show_page_activities(user_activities, page):
        return _build_page_activities(page, chat_id,
                                      get_callback_data_and_status_activity_function=_get_delete_activity_function,
                                      first_button_callback='Selected_activities_delete', first_button_text='Удалить выбраные активности')
    else:
        raise DontGetPage()


def _check_show_page_activities(user_activities: list, page: int):
    '''Проверяем есть ли активности на странице что бы их показать '''
    
    #Если у нас нет активностей, мы собираем консоль, но активности будут пустые
    if len(user_activities) == 0:
        return True
    
    #Если у нас есть активности, мы проверяем сможем ли собрать новую страницу
    return True if user_activities[page * SHOW_ACTIVITIES_SIZE: (page + 1) * SHOW_ACTIVITIES_SIZE] else False


def _get_start_stop_activity_function(chat_id: int, activity: str) -> tuple:
    '''Функция возвращяет данные для колбэк-датa кнопок-стрелочек и состояние кнопки консоли начала активностей'''

    return (('<:', '>:'), '⛔️ STOP' if check_start_activity(chat_id, activity) else '✅ START')


def _get_delete_activity_function(chat_id: int, activity: str) -> tuple:
    '''Функция возвращяет данные для колбэк-датa кнопок-стрелочек и состояние кнопки консоли удаления активностей'''

    return (('<del:', '>del:'), '☠️ Select' if _check_selected_button(chat_id, activity) else '💙 Unselect')


def _check_selected_button(chat_id: int, activity: str):
    '''Функция проверяет нажата ля кнопка выбора для удаления активности'''

    try:
        return activity in users_selected_delete_button[chat_id]
    except KeyError:
        return False


def _build_page_activities(page_number: int,
                           chat_id: int, get_callback_data_and_status_activity_function=_get_start_stop_activity_function,
                           first_button_callback: str = 'Add_new_activities', first_button_text='Добавить активность'):
    '''Собираем клавиатуру'''
    '''Клавиатура собирается в зависимости от того, какой какой колбэк и какие состояния есть у кнопок'''
    '''Передав свою функцию get_callback_data_and_status_activity_function можно настроить состояния кнопок и колбэк для этих кнопок'''

    user_activities = get_user_activities(chat_id)

    # Инициализируем клавиатуру
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(
        text=first_button_text, callback_data=first_button_callback))

    # Собираем клавиатуру активностей
    for i in user_activities[page_number * SHOW_ACTIVITIES_SIZE: (page_number + 1) * SHOW_ACTIVITIES_SIZE]:
        # Проверяем отслеживание активности
        callback_data, status_activity = get_callback_data_and_status_activity_function(
            chat_id=chat_id, activity=i)

        # Создаем клавиатуру
        keyboard.add(types.InlineKeyboardButton(text=i,
                                                callback_data=status_activity + ":" + i),
                     types.InlineKeyboardButton(text=status_activity, callback_data=status_activity + ":" + i))

    # Создаем кнопки управления
    keyboard.add(types.InlineKeyboardButton(text='<', callback_data=callback_data[0] + str(page_number - 1)),
                 types.InlineKeyboardButton(text='>', callback_data=callback_data[1] + str(page_number + 1)))

    return keyboard


def unselect_acticity_for_delete(chat_id: int, activity: str):
    try:
        users_selected_delete_button[chat_id].append(activity)
    except KeyError:
        users_selected_delete_button[chat_id] = []
        users_selected_delete_button[chat_id].append(activity)


def select_acticity_for_delete(chat_id: int, activity: str):
    try:
        users_selected_delete_button.pop(chat_id)
    except:
        pass

def delete_activities(chat_id: int):
    try:
        delete_activities = users_selected_delete_button[chat_id]
        delete_activities_db(chat_id=chat_id, delete_activities=delete_activities)
    except KeyError:
        pass


def get_static_keyboard():
    '''Возвращяет кнопки с командой вывода консоли и статистики'''

    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add(types.KeyboardButton(text='/console'),
                 types.KeyboardButton(text='/stat'))
    keyboard.add(types.KeyboardButton(text='/delete'))

    return keyboard

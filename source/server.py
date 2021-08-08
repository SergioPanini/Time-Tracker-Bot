import logging
import os
import typing
from datetime import datetime

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import reply_keyboard
from aiogram.types.message import Message
from messages import START_MESSAGE

from db import add_user, add_activity, get_user_activities, start_activity, stop_activity, get_stat

from services import get_activities_console, get_static_keyboard, DontGetPage, get_delete_activities_console
from services import select_acticity_for_delete, unselect_acticity_for_delete, delete_activities

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
    start_keyboard = get_activities_console(message.chat.id)
    static_keyboard = get_static_keyboard()

    await message.answer('🖐🏻', reply_markup=static_keyboard)
    await message.answer(START_MESSAGE, reply_markup=start_keyboard)


@dp.message_handler(commands=['console'])
async def show_main_console(message: types.Message):
    '''Отправляет основную консоль'''
    await message.answer(text='Панель управления временем', reply_markup=get_activities_console(message.chat.id))


@dp.callback_query_handler(lambda callback_query: callback_query.data.split(':')[0] in ['<', '>', '<del', '>del'])
async def console_move(callback_query: types.CallbackQuery):
    '''Функция двигает активности в консолях'''

    # Получаем  номер страницы, которую нужно показать
    console, page = callback_query.data.split(':')

    try:

        # Создаем новую клавиатуру(start_stop клавиатуру или delete клавиатуру)
        new_keyboard = get_activities_console(callback_query.message.chat.id, int(page)) \
            if console in ['<', '>'] else get_delete_activities_console(callback_query.message.chat.id, int(page))

        await callback_query.message.edit_reply_markup(new_keyboard)
        await callback_query.answer('Готово')

    except DontGetPage:
        await callback_query.answer('Больше нет активностей')


@dp.callback_query_handler(lambda callback_query: callback_query.data == "Add_new_activities")
async def activety_select(callback_query: types.CallbackQuery):
    '''Callback на кнопки добавления активности'''

    await bot.send_message(chat_id=callback_query.message.chat.id, text='Введите название активности')
    await callback_query.answer('Введите активность')

    # Сохраняем флаг, что следующее сообщени пользователя будет активность
    set_activety_user_dict[callback_query.message.chat.id] = True


@dp.callback_query_handler(lambda callback_query: callback_query.data.split(':')[0] in ['✅ START', '⛔️ STOP', '☠️ Select', '💙 Unselect'])
async def start_stop_activities(callback_query: types.CallbackQuery):
    '''Включает и выключает отслеживание активностей'''

    # Получаем активность и задачу для отслеживания(начать или прекратить)
    command, activity = callback_query.data.split(':')

    if command == "✅ START":
        start_activity(callback_query.message.chat.id, activity)

    elif command == "⛔️ STOP":
        stop_activity(callback_query.message.chat.id, activity)

    elif command == "☠️ Select":
        select_acticity_for_delete(callback_query.message.chat.id, activity)

    else:
        unselect_acticity_for_delete(callback_query.message.chat.id, activity)
    
    

    # Получаем обновленную консоль
    if command in ['✅ START', '⛔️ STOP']:
        updated_keyboard = get_activities_console(callback_query.message.chat.id,
                                              _get_actual_page(callback_query.message.reply_markup.inline_keyboard))
    else:
        updated_keyboard = get_delete_activities_console(callback_query.message.chat.id,
                                              _get_actual_page(callback_query.message.reply_markup.inline_keyboard))

    # Меняем консоль и отвечаем на callback
    await callback_query.message.edit_reply_markup(updated_keyboard)
    await callback_query.answer(text="Команда выполнена")


def _get_actual_page(inline_keyboard: list) -> int:
    '''Находим номер страници консоли активности'''

    inline_keyboard_last_row = inline_keyboard[-1]
    next_button = inline_keyboard_last_row[1]
    next_page = next_button.callback_data.split(':')[1]

    return int(next_page) - 1


@dp.message_handler(commands=['stat'])
async def get_stat_user(message: types.Message):
    '''Выводит статистику пользователя'''

    stat = get_stat(message.chat.id)

    s = 'Статистика активности за все время\n'
    for activity_row in stat:
        activity, count, avg = activity_row
        s += f"Активность: {activity}, количество: {count}, среднее время: {avg}\n"

    await message.answer(text=s)


@dp.message_handler(commands=['delete'])
async def delete_activities_command(message: types.Message):
    '''Вывод консоли удаления активностей'''

    await message.answer(text='Отмете активности, которые хотите удалить, затем нажмите "Применить"',
                         reply_markup=get_delete_activities_console(message.chat.id))

@dp.callback_query_handler(lambda callback_query: callback_query.data=='Selected_activities_delete')
async def delete_activities_callback(callback_query: types.CallbackQuery):

    delete_activities(callback_query.message.chat.id)
    updated_keyboard = get_delete_activities_console(callback_query.message.chat.id)
    await callback_query.message.edit_reply_markup(updated_keyboard)
    await callback_query.answer(text='Выбраные активности удалены')

@dp.message_handler()
async def set_activety(message: types.Message):
    '''Запись новой активности от пользователя в бд'''

    if set_activety_user_dict.get(message.chat.id) == True:
        set_activety_user_dict[message.chat.id] = False
        await message.answer(text='Запомнил %s' % message.text)

        add_activity(chat_id=message.chat.id, activity=message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

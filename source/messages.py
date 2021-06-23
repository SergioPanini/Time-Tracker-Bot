from aiogram import types

'''В этом модуле лежат все сообщения бота'''

START_MESSAGE = "Привет, я бот который помогает отслеживать на что ты уходит твое время. \n\
У тебя есть несколько предустановленых активностей: работа, спорт, отдых. Нажимая на кнопку \
активности \"Начать\" ты запускаешь отслеживание, нажимая на кнопку активности \"Остановить\" \
ты останавливаешь отслеживание активности. \n Несколько активностей могут отслеживатся независимо \
друг от друга. \n Главное не забывай их останавливать."


START_KEYBOARD = types.InlineKeyboardMarkup()

START_KEYBOARD.add(types.InlineKeyboardButton(
    text='Добавить активность', callback_data='Add_new_activities'))
START_KEYBOARD.add(types.InlineKeyboardButton(text='<', callback_data='<'),
                   types.InlineKeyboardButton(text='>', callback_data='>'))

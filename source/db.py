import sqlite3
import os
from sqlite3.dbapi2 import connect
from typing import List

conn = sqlite3.connect('/home/bot/source/data/db.sqlite3')
coursor = conn.cursor()

def add_user(chat_id: int):
    '''Добавляет пользователя в БД'''

    coursor.execute("SELECT * FROM users WHERE chat_id = ?", [(chat_id)])
    user = coursor.fetchall()

    if len(user) == 0:
        coursor.execute(
            "INSERT INTO users(chat_id, types_activities) VALUES (?, ?)", (chat_id, ""))
        conn.commit()
        print('Добавил нового пользователя')


def get_user_activities(chat_id: int) -> list:
    '''Получает активности пользователя'''

    coursor.execute("SELECT * FROM users WHERE chat_id = ?", [(chat_id)])
    user = coursor.fetchall()
    user_activities = user[0][1]
    return user_activities.split(',')[1:]


def add_activity(chat_id: int, activity: str):
    '''Добавляет новую активность пользователю'''

    coursor.execute("SELECT * FROM users WHERE chat_id = ?", [(chat_id)])
    user = coursor.fetchall()
    user_activities = user[0][1]

    coursor.execute("UPDATE users SET types_activities = ? WHERE users.chat_id = ?",
                    (','.join([user_activities, activity]), chat_id))
    conn.commit()

def set_start_activities(chat_id: int, activities_name: str) -> None:
    '''Стартует активность пользователя'''

    coursor.execute("INSERT INTO activities(user_chat_id, type_activities, start)\
         VALUES (?, ?, ?);")
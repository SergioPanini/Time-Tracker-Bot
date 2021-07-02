import sqlite3
import os
from sqlite3.dbapi2 import connect
from typing import List

from datetime import datetime
import logging

logging.basicConfig(filename='app.log', filemode='w', level=logging.INFO)

conn = sqlite3.connect('/home/bot/source/data/db.sqlite3')
coursor = conn.cursor()

def add_user(chat_id: int):
    '''Добавляет пользователя в БД'''

    coursor.execute("SELECT * FROM users WHERE chat_id = ?", [(chat_id)])
    user = coursor.fetchall()
    is_user = len(user) == 0

    if is_user:
        coursor.execute(
            "INSERT INTO users(chat_id, types_activities) VALUES (?, ?)", (chat_id, ",Работа,Спорт,Отдых"))
        conn.commit()

    logging.info(f'add_user [{locals()}]')


def get_user_activities(chat_id: int) -> list:
    '''Получает список активностей пользователя'''

    coursor.execute("SELECT * FROM users WHERE chat_id = ?", [(chat_id)])
    user = coursor.fetchall()
    user_activities = user[0][1]

    logging.info(f'get_user_activities [{locals()}]')

    return user_activities.split(',')[1:]


def check_start_activity(chat_id: int, activity_name: str) -> str:
    '''Проверяет запущена ли активность или нет'''

    # Пытаемся найти начатую активность
    coursor.execute("SELECT * FROM activities WHERE user_chat_id = ? AND \
                    type_activities = ? AND start NOT NULL AND stop IS NULL;",
                    (chat_id, activity_name))
    sql_result = coursor.fetchall()

    logging.info(f'check_start_activity [{locals()}]')
    
    # Проверяем нашлось ли что то
    if sql_result:
        return True
    return False


def add_activity(chat_id: int, activity: str):
    '''Добавляет новую активность пользователю'''

    # Достаем активности ползователя
    coursor.execute("SELECT * FROM users WHERE chat_id = ?", [(chat_id)])
    user = coursor.fetchall()
    user_activities = user[0][1]

    # Добавляем новую активность
    coursor.execute("UPDATE users SET types_activities = ? WHERE users.chat_id = ?",
                    (','.join([user_activities, activity]), chat_id))
    conn.commit()

    logging.info(f'add_activity [{locals()}]')



def start_activity(chat_id: int, activity_name: str) -> None:
    '''Начинает отслеживание активность пользователя'''

    # Добавляем старт активности в БД
    coursor.execute("INSERT INTO activities(id, user_chat_id, type_activities, start)\
         VALUES (?, ?, ?, ?);", (None, chat_id, activity_name, datetime.now()))

    conn.commit()

    logging.info(f'start_activity [{locals()}]')



def stop_activity(chat_id: int, activity_name: str) -> None:
    '''Останавливает отслеживание активности пользователя'''

    # Останавливаем отслеживание активности в БД
    coursor.execute("UPDATE activities SET stop = ? WHERE user_chat_id = ? AND\
         type_activities = ?;", (datetime.now(), chat_id, activity_name))

    conn.commit()

    logging.info(f'stop_activity [{locals()}]')


def show_all() -> None:
    coursor.execute("SELECT * FROM activities")

    print(coursor.fetchall())


def get_stat(chat_id: int) -> list:
    '''Достает статистику'''

    coursor.execute('SELECT\
         activities.type_activities as activities,\
         count(activities.start) as count,\
         time(avg(strftime("%s", activities.stop) - strftime("%s", activities.start)), "unixepoch") as avg\
              FROM activities WHERE activities.user_chat_id = ? AND activities.stop NOT NULL\
              GROUP BY activities.type_activities;', [(chat_id)])
    
    sql_result = coursor.fetchall()

    logging.info(f'get_stat [{locals()}]')

    return sql_result

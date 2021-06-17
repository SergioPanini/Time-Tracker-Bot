import sqlite3
import os

conn = sqlite3.connect('/home/bot/source/data/db.sqlite3')
coursor = conn.cursor()

def check_init_db():
    '''Проверяет инициализарована ли база'''

    coursor.execute("\
    SELECT name FROM sqlite_master WHERE type='table' AND name='user_info'\
        ")
    
    table_exist = coursor.fetchall()
    if table_exist:
        return
    _init_db()

def _init_db():
    """Инициализирует БД"""
    with open("/home/bot/source/createdb.sql", "r") as f:
        sql = f.read()
    coursor.executescript(sql)
    conn.commit()

check_init_db()

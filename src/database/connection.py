import sqlite3
from pathlib import Path

DATABASE_PATH = Path('data/database.db')

def get_db_connection():
    """Создает подключение к базе данных"""
    connection = sqlite3.connect(DATABASE_PATH)
    return connection

def init_db():
    """
    """
    connection = get_db_connection()
    cursor = connection.cursor()
        
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY,
        group_id INTEGER NOT NULL
        )
        ''')

    # Сохраняем изменения и закрываем соединение
    connection.commit()
    connection.close()



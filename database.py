import os
import sqlite3

# Путь к базе данных и создание папки db
DB_DIR = os.path.join(os.path.dirname(__file__), "db")
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)
DB_PATH = os.path.join(DB_DIR, "tasks.db")

def get_connection():
    """Получить соединение с базой данных"""
    return sqlite3.connect(DB_PATH)

def create_table(conn):
    """Создать таблицу задач, если не существует"""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT,
            created TEXT,
            updated TEXT
        )
    """)
    conn.commit()
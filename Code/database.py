# database.py
import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT
            )
        ''')
        self.conn.commit()

    def add_user(self, username, password):
        self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        self.conn.commit()

    def get_user(self, username):
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        return self.cursor.fetchone()

    def get_all_users(self):
        self.cursor.execute('SELECT * FROM users')
        return self.cursor.fetchall()

    def delete_user(self, username):
        self.cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        self.conn.commit()
        self.reset_autoincrement("users")  # Вызовите reset_autoincrement после удаления записи

    def reset_autoincrement(self, table_name):
        # Получите максимальное значение id после удаления записи
        self.cursor.execute(f"SELECT MAX(id) FROM {table_name}")
        max_id = self.cursor.fetchone()[0]

        # Если max_id равно None, установите его в 0
        max_id = 0 if max_id is None else max_id

        # Обновите таблицу sqlite_sequence
        self.cursor.execute(f"UPDATE sqlite_sequence SET seq={max_id} WHERE name=?", (table_name,))
        self.conn.commit()

    def close(self):
        self.conn.close()

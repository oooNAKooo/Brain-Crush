# database.py
import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
    
    def create_users_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL UNIQUE,
                                password TEXT NOT NULL,
                                snake_score INTEGER DEFAULT 0,
                                tic_tac_toe_wins INTEGER DEFAULT 0,
                                sudoku_solved INTEGER DEFAULT 0
                            )''')
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

    def update_snake_score(self, username, score):
        self.cursor.execute('UPDATE users SET snake_score = ? WHERE username = ?', (score, username))
        self.conn.commit()

    def update_tic_tac_toe_wins(self, username, wins):
        self.cursor.execute('UPDATE users SET tic_tac_toe_wins = ? WHERE username = ?', (wins, username))
        self.conn.commit()

    def update_sudoku_solved(self, username, solved_count):
        self.cursor.execute('UPDATE users SET sudoku_solved = ? WHERE username = ?', (solved_count, username))
        self.conn.commit()

    def get_tic_tac_toe_score(self, username):
        self.cursor.execute('SELECT tic_tac_toe_wins FROM users WHERE username = ?', (username,))
        return self.cursor.fetchone()[0]  # возвращает количество побед в крестики-нолики

    
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

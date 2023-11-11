import tkinter as tk
from tkinter import messagebox
import sqlite3
import random

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

    def close(self):
        self.conn.close()

class TicTacToeGame:
    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.current_player = "X"

    def make_move(self, position):
        if self.board[position] == " ":
            self.board[position] = self.current_player
            self.check_winner()
            self.switch_player()
            return True
        else:
            return False

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        # Проверка по горизонтали
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i + 1] == self.board[i + 2] != " ":
                return self.board[i]

        # Проверка по вертикали
        for i in range(3):
            if self.board[i] == self.board[i + 3] == self.board[i + 6] != " ":
                return self.board[i]

        # Проверка по диагоналям
        if self.board[0] == self.board[4] == self.board[8] != " ":
            return self.board[0]
        if self.board[2] == self.board[4] == self.board[6] != " ":
            return self.board[2]

        # Проверка на ничью
        if " " not in self.board:
            return "ничья"

        return None

    def is_board_full(self):
        return " " not in self.board


    # Другие методы TicTacToeGame

class TicTacToeApp:
    def __init__(self, root, db, show_game_menu_callback):
        self.root = root
        self.db = db
        self.show_game_menu_callback = show_game_menu_callback

        # Создаем новое окно для игры
        self.game_window = tk.Toplevel(root)
        self.game_window.title("Крестики-нолики")
        self.game_window.geometry("400x400")

        self.frame = tk.Frame(self.game_window)
        self.frame.grid(row=0, column=0, padx=10, pady=10)  # Используем grid для фрейма

        self.game = TicTacToeGame()
        self.create_board()

    def create_board(self):
        self.buttons = [[None, None, None] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                button = tk.Button(self.frame, text="", font=("Arial", 20), width=5, height=2,
                                   command=lambda row=i, col=j: self.make_move(row, col))
                button.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = button

    def make_move(self, row, col):
        if self.game.make_move(row * 3 + col):
            self.update_board()
            if not self.game.check_winner():
                self.root.after(500, self.computer_move)

    def computer_move(self):
        if not self.game.is_board_full() and not self.game.check_winner():
            empty_positions = [i for i in range(9) if self.game.board[i] == " "]
            computer_choice = random.choice(empty_positions)
            self.game.make_move(computer_choice)
            self.update_board()

    def update_board(self):
        winner = self.game.check_winner()

        if winner:
            if winner == "ничья":
                messagebox.showinfo("Ничья!", "Игра окончена, ничья!")
            else:
                messagebox.showinfo("Победитель!", f"Игра окончена, победил игрок {winner}!")

            self.show_game_menu_callback()
        else:
            for i in range(3):
                for j in range(3):
                    value = self.game.board[i * 3 + j]
                    self.buttons[i][j].config(text=value)


class BrainCrushApp:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.title("Brain Crush")
        self.root.geometry("800x600")

        self.show_welcome_frame()
        self.root.mainloop()

    def show_welcome_frame(self):
        title_label = tk.Label(self.root, text="BRAIN CRUSH", font=("Arial", 30))
        title_label.pack(pady=50)

        subtitle_label = tk.Label(self.root, text="Нажмите Enter для продолжения", font=("Arial", 10))
        subtitle_label.pack(pady=20)

        self.root.bind("<Return>", lambda event: self.show_main_menu())

    def show_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        main_menu_frame = tk.Frame(self.root)
        main_menu_frame.pack()

        title_label = tk.Label(main_menu_frame, text="BRAIN CRUSH", font=("Arial", 30))
        title_label.pack(pady=20)

        def login_clicked():
            self.show_login_window()

        def register_clicked():
            self.show_registration_window()

        def view_profiles():
            profiles = self.db.get_all_users()
            for profile in profiles:
                print(profile)

        def exit_clicked():
            self.root.destroy()

        login_button = tk.Button(main_menu_frame, text="Войти в профиль", command=login_clicked)
        login_button.pack(pady=10)

        register_button = tk.Button(main_menu_frame, text="Зарегистрировать профиль", command=register_clicked)
        register_button.pack(pady=10)

        view_profiles_button = tk.Button(main_menu_frame, text="Просмотреть профили", command=view_profiles)
        view_profiles_button.pack(pady=10)

        exit_button = tk.Button(main_menu_frame, text="Выйти из приложения", command=exit_clicked)
        exit_button.pack(pady=10)

    def show_login_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        login_frame = tk.Frame(self.root)
        login_frame.pack()

        title_label = tk.Label(login_frame, text="BRAIN CRUSH", font=("Arial", 30))
        title_label.pack(pady=20)

        username_label = tk.Label(login_frame, text="Имя пользователя:")
        username_label.pack()
        username_entry = tk.Entry(login_frame)
        username_entry.pack()

        password_label = tk.Label(login_frame, text="Пароль:")
        password_label.pack()
        password_entry = tk.Entry(login_frame, show="*")
        password_entry.pack()

        def login_user():
            username = username_entry.get()
            password = password_entry.get()
            user = self.db.get_user(username)

            if user and user[2] == password:
                messagebox.showinfo("Успех", "Вход успешный")
                self.show_game_menu()
            else:
                messagebox.showwarning("Предупреждение", "Имя пользователя и/или пароль введены не верно")

        login_button = tk.Button(login_frame, text="Войти", command=login_user)
        login_button.pack(pady=20)

        back_button = tk.Button(login_frame, text="Вернуться в главное меню", command=self.show_main_menu)
        back_button.pack(pady=10)

    def show_registration_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        registration_frame = tk.Frame(self.root)
        registration_frame.pack()

        title_label = tk.Label(registration_frame, text="BRAIN CRUSH", font=("Arial", 30))
        title_label.pack(pady=20)

        username_label = tk.Label(registration_frame, text="Имя пользователя:")
        username_label.pack()
        username_entry = tk.Entry(registration_frame)
        username_entry.pack()

        password_label = tk.Label(registration_frame, text="Пароль:")
        password_label.pack()
        password_entry = tk.Entry(registration_frame, show="*")
        password_entry.pack()

        repeat_password_label = tk.Label(registration_frame, text="Повторите пароль:")
        repeat_password_label.pack()
        repeat_password_entry = tk.Entry(registration_frame, show="*")
        repeat_password_entry.pack()

        def register_user():
            username = username_entry.get()
            password = password_entry.get()
            repeat_password = repeat_password_entry.get()

            if password == repeat_password:
                self.db.add_user(username, password)
                messagebox.showinfo("Успех", "Пользователь успешно зарегистрирован")
                self.show_game_menu()
            else:
                messagebox.showwarning("Предупреждение", "Пароли не совпадают")

        register_button = tk.Button(registration_frame, text="Зарегистрировать", command=register_user)
        register_button.pack(pady=20)

        back_button = tk.Button(registration_frame, text="Вернуться в главное меню", command=self.show_main_menu)
        back_button.pack(pady=10)

    def show_game_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        game_menu_frame = tk.Frame(self.root)
        game_menu_frame.pack()

        title_label = tk.Label(game_menu_frame, text="Выберите игру", font=("Arial", 30))
        title_label.pack(pady=20)

        def tic_tac_toe_clicked():
            TicTacToeApp(self.root, self.db, self.show_game_menu)

        def snake_clicked():
            # Реализуйте запуск игры "змейка" здесь
            pass

        def sudoku_clicked():
            # Реализуйте запуск игры "судоку" здесь
            pass

        def exit_clicked():
            self.root.destroy()

        tic_tac_toe_button = tk.Button(game_menu_frame, text="Крестики-нолики", command=tic_tac_toe_clicked)
        tic_tac_toe_button.pack(pady=10)

        snake_button = tk.Button(game_menu_frame, text="Змейка", command=snake_clicked)
        snake_button.pack(pady=10)

        sudoku_button = tk.Button(game_menu_frame, text="Судоку", command=sudoku_clicked)
        sudoku_button.pack(pady=10)

        exit_button = tk.Button(game_menu_frame, text="Выйти из программы", command=exit_clicked)
        exit_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = BrainCrushApp(root)

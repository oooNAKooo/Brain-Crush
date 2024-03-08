# main.py
import tkinter as tk
from tkinter import messagebox
from database import Database
from tictactoe import TicTacToeApp
from admin import AdminApp
from snake import SnakeGame
from dino import DinoGame
from race import RaceGame
from sudoku import SudokuGame, SudokuApp  # Импортируем класс SudokuGame из файла sudoku.py
from statistics_window import StatisticsWindow  # Импорт класса StatisticsWindow

# Инициализация Pygame перед созданием объекта BrainCrushApp
import pygame
pygame.init()



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

        subtitle_label = tk.Label(self.root, text="Нажмите Space для продолжения...", font=("Arial", 10))
        subtitle_label.pack(pady=20)

        self.root.bind("<space>", lambda event: self.show_main_menu())

    def show_admin_menu(self):
        # Передайте объект Database при создании AdminApp
        AdminApp(self.root, self.db, lambda: self.show_main_menu())


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

        def exit_clicked():
            self.root.destroy()

        login_button = tk.Button(main_menu_frame, text="Войти в профиль", command=login_clicked)
        login_button.pack(pady=10)

        register_button = tk.Button(main_menu_frame, text="Зарегистрировать профиль", command=register_clicked)
        register_button.pack(pady=10)

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

            if username == "admin" and password == "1111":
                messagebox.showinfo("Успех", "Вы вошли в режим администратора!")
                self.show_admin_menu()
            else:
                user = self.db.get_user(username)
                if user and user[2] == password:
                    messagebox.showinfo("Успех", "Вход успешный!")
                    self.show_game_menu(username)
                elif not user:
                    messagebox.showwarning("Предупреждение", "Пользователя с таким именем не существует!")
                else:
                    messagebox.showwarning("Ошибка", "Имя пользователя и/или пароль введены не верно!")

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
                user_exists = self.db.get_user(username)
                if not user_exists:
                    self.db.add_user(username, password)
                    messagebox.showinfo("Успех", "Пользователь успешно зарегистрирован")
                    self.show_main_menu()
                else:
                    messagebox.showwarning("Предупреждение", "Пользователь с таким именем уже существует")
            else:
                messagebox.showwarning("Предупреждение", "Пароли не совпадают")

        register_button = tk.Button(registration_frame, text="Зарегистрировать", command=register_user)
        register_button.pack(pady=20)

        back_button = tk.Button(registration_frame, text="Вернуться в главное меню", command=self.show_main_menu)
        back_button.pack(pady=10)

    def show_game_menu(self, username):
        for widget in self.root.winfo_children():
            widget.destroy()

        game_menu_frame = tk.Frame(self.root)
        game_menu_frame.pack()

        title_label_text = f"Выберите игру, {username}"
        title_label = tk.Label(game_menu_frame, text=title_label_text, font=("Arial", 30))
        title_label.pack(pady=20)

        def tic_tac_toe_clicked():
            TicTacToeApp(self.root, self.db, lambda: self.show_game_menu_callback, username)

        def snake_clicked():
            self.start_snake_game(username)

        def sudoku_clicked():
            self.start_sudoku_game(username)

        def dino_clicked():
            self.start_dino_game(username)

        def race_clicked():
            self.start_race_game(username)

        def exit_clicked():
            self.root.destroy()

        def statistic_clicked():
            self.show_statistics(username)

        tic_tac_toe_button = tk.Button(game_menu_frame, text="Крестики-нолики", command=tic_tac_toe_clicked)
        tic_tac_toe_button.pack(pady=10)

        snake_button = tk.Button(game_menu_frame, text="Змейка", command=snake_clicked)
        snake_button.pack(pady=10)

        sudoku_button = tk.Button(game_menu_frame, text="Судоку", command=sudoku_clicked)
        sudoku_button.pack(pady=10)

        sudoku_button = tk.Button(game_menu_frame, text="Динозавр", command=dino_clicked)
        sudoku_button.pack(pady=10)

        sudoku_button = tk.Button(game_menu_frame, text="Гонки", command=race_clicked)
        sudoku_button.pack(pady=10)

        statistics_button = tk.Button(game_menu_frame, text="Статистика", command=statistic_clicked)
        statistics_button.pack(pady=10)

        back_button = tk.Button(game_menu_frame, text="Вернуться в главное меню", command=self.show_main_menu)
        back_button.pack(pady=10)

        exit_button = tk.Button(game_menu_frame, text="Выйти из программы", command=exit_clicked)
        exit_button.pack(pady=10)

    def show_statistics(self, username):
        StatisticsWindow(self.root, self.db, username, lambda: self.show_game_menu_callback)

    def start_sudoku_game(self, username):
        SudokuApp(self.root, self.db, username, lambda: self.show_main_menu())

    def start_snake_game(self, username):
        snake_game = SnakeGame(self.db, username)
        snake_game.run()

    def start_dino_game(self, username):
        DinoGame(self.root, self.db, username)

    def start_race_game(self, username):
        RaceGame(self.db, username)


if __name__ == "__main__":
    root = tk.Tk()
    app = BrainCrushApp(root)

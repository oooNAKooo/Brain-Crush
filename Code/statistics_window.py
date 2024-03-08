import tkinter as tk
from tkinter import messagebox

class StatisticsWindow(tk.Toplevel):
    def __init__(self, master, db, username, show_game_menu_callback):
        super().__init__(master)
        self.db = db
        self.username = username
        self.show_game_menu_callback = show_game_menu_callback
        self.title("Статистика игр")
        self.geometry("400x300")

        self.label = tk.Label(self, text=f"Статистика игр для пользователя {username}", font=("Arial", 14))
        self.label.pack(pady=10)

        self.tic_tac_toe_button = tk.Button(self, text="Крестики-нолики", command=self.show_tic_tac_toe_statistics)
        self.tic_tac_toe_button.pack(pady=5)
        
        self.snake_button = tk.Button(self, text="Змейка", command=self.show_snake_statistics)
        self.snake_button.pack(pady=5)
        
        self.sudoku_button = tk.Button(self, text="Судоку", command=self.show_sudoku_statistics)
        self.sudoku_button.pack(pady=5)

        self.dino_button = tk.Button(self, text="Динозавр", command=self.show_dino_statistics)
        self.dino_button.pack(pady=5)

        self.race_button = tk.Button(self, text="Гонки", command=self.show_race_statistics)
        self.race_button.pack(pady=5)

    def show_snake_statistics(self):
        snake_record = self.db.get_snake_score(self.username)
        messagebox.showinfo("Статистика Змейки", f"Рекорд в Змейке: {snake_record}")

    def show_tic_tac_toe_statistics(self):
        # Получаем статистику по игре "Крестики-нолики" для выбранного пользователя
        tic_tac_toe_wins = self.db.get_tic_tac_toe_score(self.username)
        messagebox.showinfo("Статистика Крестиков-ноликов", f"Количество побед в Крестики-нолики: {tic_tac_toe_wins}")
        
    def show_sudoku_statistics(self):
        sudoku_solved = self.db.get_sudoku_score(self.username)
        messagebox.showinfo("Статистика Судоку", f"Количество решенных партий в Судоку: {sudoku_solved}")

    def show_dino_statistics(self):
        dino_run = self.db.get_dino_score(self.username)
        messagebox.showinfo("Статистика Динозавра", f"Количество решенных партий в Судоку: {dino_run}")

    def show_race_statistics(self):
        race_run = self.db.get_race_score(self.username)
        messagebox.showinfo("Статистика Гонок", f"Количество набранных очков: {race_run}")

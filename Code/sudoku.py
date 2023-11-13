import tkinter as tk
from tkinter import messagebox
import random
from database import Database
from tictactoe import TicTacToeApp


class SudokuGame:
    def __init__(self):
        self.board = [[0] * 9 for _ in range(9)]
        self.initialize_board()

    def initialize_board(self):
        # Начальное состояние доски Судоку
        # Ваш код для генерации начальной доски
        pass

    def make_move(self, row, col, value):
        # Обработка хода игрока
        if self.board[row][col] == 0:
            self.board[row][col] = value
            return True
        else:
            return False

    def is_board_full(self):
        # Проверка, заполнена ли доска полностью
        for row in self.board:
            if 0 in row:
                return False
        return True

    def check_winner(self):
        # Проверка победы
        # Для Судоку, победы обычно не проверяются,
        # так как игра завершается, когда доска полностью заполнена
        return None

class SudokuApp:
    def __init__(self, root, db, show_game_menu_callback):
        self.root = root
        self.db = db
        self.show_game_menu_callback = show_game_menu_callback

        self.game_window = tk.Toplevel(root)
        self.game_window.title("Судоку")
        self.game_window.geometry("400x400")

        self.frame = tk.Frame(self.game_window)
        self.frame.grid(row=0, column=0, padx=10, pady=10)

        self.game = SudokuGame()
        self.create_board()

    def create_board(self):
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(self.frame, width=3, font=("Arial", 16), justify="center")
                entry.grid(row=i, column=j, padx=2, pady=2)

                # Заполнение начального состояния доски
                value = self.game.board[i][j]
                if value != 0:
                    entry.insert(0, str(value))
                    entry.config(state="disabled")

                entry.bind("<FocusIn>", lambda event, row=i, col=j: self.on_entry_click(event, row, col))
                entry.bind("<Key>", lambda event, row=i, col=j: self.on_key_press(event, row, col))

    def on_entry_click(self, event, row, col):
        # Обработчик события щелчка на поле ввода
        entry = event.widget
        entry.config(fg="black")

    def on_key_press(self, event, row, col):
        # Обработчик события нажатия клавиши на поле ввода
        entry = event.widget
        value = entry.get()
        if value.isdigit() and 1 <= int(value) <= 9:
            self.make_move(row, col, int(value))
            self.update_board()

    def make_move(self, row, col, value):
        if self.game.make_move(row, col, value):
            self.update_board()
            if not self.game.check_winner() and not self.game.is_board_full():
                self.root.after(500, self.computer_move)

    def computer_move(self):
        if not self.game.is_board_full() and not self.game.check_winner():
            empty_positions = [(i, j) for i in range(9) for j in range(9) if self.game.board[i][j] == 0]
            computer_choice = random.choice(empty_positions)
            self.game.make_move(computer_choice[0], computer_choice[1], 2)
            self.update_board()

    def update_board(self):
        if self.game.check_winner() or self.game.is_board_full():
            self.show_game_menu_callback()
        else:
            for i in range(9):
                for j in range(9):
                    value = self.game.board[i][j]
                    entry = self.get_entry(i, j)
                    entry.delete(0, tk.END)
                    entry.insert(0, str(value))

    def get_entry(self, row, col):
        for widget in self.frame.winfo_children():
            if widget.grid_info()["row"] == row and widget.grid_info()["column"] == col:
                return widget

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

        def tic_tac_toe_clicked():
            TicTacToeApp(self.root, self.db, self.show_game_menu)

        def sudoku_clicked():
            SudokuApp(self.root, self.db, self.show_game_menu)

        def exit_clicked():
            self.root.destroy()

        tic_tac_toe_button = tk.Button(main_menu_frame, text="Крестики-нолики", command=tic_tac_toe_clicked)
        tic_tac_toe_button.pack(pady=10)

        sudoku_button = tk.Button(main_menu_frame, text="Судоку", command=sudoku_clicked)
        sudoku_button.pack(pady=10)

        exit_button = tk.Button(main_menu_frame, text="Выйти из приложения", command=exit_clicked)
        exit_button.pack(pady=10)

    def show_game_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        game_menu_frame = tk.Frame(self.root)
        game_menu_frame.pack()

        title_label = tk.Label(game_menu_frame, text="Выберите игру", font=("Arial", 30))
        title_label.pack(pady=20)

        def tic_tac_toe_clicked():
            TicTacToeApp(self.root, self.db, self.show_game_menu)

        def sudoku_clicked():
            SudokuApp(self.root, self.db, self.show_game_menu)

        def exit_clicked():
            self.root.destroy()

        tic_tac_toe_button = tk.Button(game_menu_frame, text="Крестики-нолики", command=tic_tac_toe_clicked)
        tic_tac_toe_button.pack(pady=10)

        sudoku_button = tk.Button(game_menu_frame, text="Судоку", command=sudoku_clicked)
        sudoku_button.pack(pady=10)

        exit_button = tk.Button(game_menu_frame, text="Выйти из программы", command=exit_clicked)
        exit_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = BrainCrushApp(root)

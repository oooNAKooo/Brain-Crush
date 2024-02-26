# tictactoe.py
import tkinter as tk
from tkinter import messagebox
import random


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


class TicTacToeApp:
    def __init__(self, root, db, show_game_menu_callback, username):
        self.username = username
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
                                   command=lambda row=i, col=j: self.make_move(row, col, self.username))
                button.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = button

    def make_move(self, row, col, username):
        if self.game.make_move(row * 3 + col):
            self.update_board()
            winner = self.game.check_winner()
            if winner:
                if winner == "ничья":
                    messagebox.showinfo("Ничья!", "Игра окончена, ничья!")
                else:
                    messagebox.showinfo("Победитель!", f"Игра окончена, победил игрок {winner}!")
                    # Обновляем статистику побед для текущего игрока
                    current_wins = self.db.get_tic_tac_toe_score(username)
                    if current_wins is None:
                        current_wins = 0
                    if winner == "X":
                        updated_wins = current_wins + 1
                        self.db.update_tic_tac_toe_wins(username, updated_wins)
                    else:
                        self.db.update_tic_tac_toe_wins(username, current_wins)
                self.root.after(1000, self.game_window.destroy)  # Закрываем окно через 1 секунду
            else:
                self.root.after(500, self.computer_move)

    def computer_move(self):
        if not self.game.is_board_full() and not self.game.check_winner():
            empty_positions = [i for i in range(9) if self.game.board[i] == " "]
            computer_choice = random.choice(empty_positions)
            self.game.make_move(computer_choice)
            self.update_board()

    def update_board(self):
        for i in range(3):
            for j in range(3):
                value = self.game.board[i * 3 + j]
                self.buttons[i][j].config(text=value)

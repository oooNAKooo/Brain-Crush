# sudoku.py
import tkinter as tk
from database import Database
from tkinter import messagebox

class SudokuGame:
    def __init__(self, parent, root, show_rules_func, db, username, back_callback):
        self.parent = parent
        self.show_rules_func = show_rules_func
        self.db = db
        self.root = root
        self.username = username
        self.back_callback = back_callback

        # Создание и отрисовка игрового поля
        self.board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]

        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.draw_board()

    def draw_board(self):
        frame = tk.Frame(self.parent)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Функция для валидации ввода
        def validate_input(char, index, current_value):
            return char.isdigit() and 0 < int(char) <= 9 and len(current_value) <= 1

        vcmd = (frame.register(validate_input), '%S', '%i', '%P')

        for i in range(9):
            for j in range(9):
                cell_value = self.board[i][j]
                is_initial_value = cell_value != 0

                # Определение цвета текста в ячейке
                text_color = "red" if is_initial_value else "black"

                cell_entry = tk.Entry(frame, width=3, font=("Arial", 24), justify="center", validate="key", validatecommand=vcmd)
                cell_entry.grid(row=i, column=j)
                cell_entry.insert(0, str(cell_value))

                # Установка цвета текста
                cell_entry.config(fg=text_color)

                self.entries[i][j] = cell_entry

                # Разграничение блоков 3x3
                if i % 3 == 0 and i > 0:
                    cell_entry.grid(pady=(10, 0))
                if j % 3 == 0 and j > 0:
                    cell_entry.grid(padx=(10, 0))

        check_button = tk.Button(frame, text="Тест", command=self.check_solution, font=("Arial", 16))
        check_button.grid(row=9, column=4, pady=20)

        back_button = tk.Button(frame, text="Назад", command=self.back_to_game_menu, font=("Arial", 16))
        back_button.grid(row=10, column=4, pady=20)

    def check_solution(self):
        user_solution = []
        for i in range(9):
            row_values = []
            for j in range(9):
                value = self.entries[i][j].get()
                row_values.append(int(value) if value else 0)
            user_solution.append(row_values)

        if any(any(val != 0 for val in row) for row in user_solution):
            if self.is_solution_valid(user_solution):
                messagebox.showinfo("Поздравляем", "Вы правильно решили Судоку !")
                current_wins = self.db.get_sudoku_score(self.username)
                if current_wins is None:
                    current_wins = 0
                updated_wins = current_wins + 1
                self.db.update_sudoku_solved(self.username, updated_wins)
            else:
                messagebox.showerror("Неправильное решение", "Ваше решение неверное. Пожалуйста, попробуйте ещё.")
        else:
            messagebox.showerror("Нет данных", "Пожалуйста, заполните хотя бы одну ячейку перед проверкой.")

    def is_solution_valid(self, solution):
        # Проверка по строкам и столбцам
        for i in range(9):
            if not self.is_unit_valid(solution[i]) or not self.is_unit_valid([solution[j][i] for j in range(9)]):
                return False

        # Проверка по блокам 3x3
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                block = [solution[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
                if not self.is_unit_valid(block):
                    return False

        return True

    def is_unit_valid(self, unit):
        # Проверка, что все элементы в строке/столбце/блоке уникальны
        seen = set()
        for num in unit:
            if num != 0:
                if num in seen:
                    return False
                seen.add(num)
        return True

    def back_to_game_menu(self):
        self.parent.destroy()  # Закрываем окно с игрой
        self.back_callback()   # Возвращаемся в меню с выбором игр

class SudokuApp:
    def __init__(self, root, db, username, back_callback):
        self.root = root
        self.db = db
        self.username = username
        self.back_callback = back_callback

        self.game_window = tk.Toplevel(root)
        self.game_window.title("Судоку")
        self.game_window.geometry("1600x600")

        self.frame = tk.Frame(self.game_window)
        self.frame.grid(row=0, column=0, padx=10, pady=10)  # Используем grid для фрейма

        # Показываем правила игры перед началом игры
        self.show_rules()

    def show_rules(self):
        rules_text = (
            "Правила игры в судоку:\n\n"
            "1. Заполните каждую ячейку числом от 1 до 9 так, чтобы каждая цифра встречалась "
            "в каждой строке, в каждом столбце и в каждом блоке 3x3.\n"
            "2. Заполните все ячейки, чтобы завершить игру."
        )

        rules_label = tk.Label(self.frame, text=rules_text, font=("Arial", 18), justify="left")
        rules_label.grid(row=0, column=0, padx=20, pady=20)

        start_button = tk.Button(self.frame, text="Начать игру", command=self.start_sudoku_game, font=("Arial", 16))
        start_button.grid(row=1, column=0, pady=20)

    def start_sudoku_game(self):
        # Удаляем правила и начинаем игру
        for widget in self.frame.winfo_children():
            widget.destroy()
        SudokuGame(self.game_window, self.root, self.show_rules, self.db, self.username, self.back_to_game_menu)

    def back_to_game_menu(self):
        self.game_window.destroy()  # Закрываем окно с игрой
        self.back_callback()        # Возвращаемся в меню с выбором игр

if __name__ == "__main__":
    root = tk.Tk()
    SudokuApp(root, Database(), lambda: print("Back to game menu"))
    root.mainloop()

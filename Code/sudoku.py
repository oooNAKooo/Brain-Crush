import tkinter as tk
from tkinter import messagebox

class SudokuGame:
    def __init__(self, parent, show_rules_func):
        self.parent = parent
        self.show_rules_func = show_rules_func

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

        check_button = tk.Button(frame, text="Check", command=self.check_solution, font=("Arial", 16))
        check_button.grid(row=9, column=4, pady=20)

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
                messagebox.showinfo("Congratulations!", "You solved the Sudoku puzzle!")
            else:
                messagebox.showerror("Incorrect Solution", "Your solution is incorrect. Please try again.")
        else:
            messagebox.showerror("No Input", "Please fill in at least one cell before checking.")

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


class BrainCrushApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Brain Crush")
        self.root.geometry("800x600")

        # Показываем правила игры перед началом игры
        self.show_rules()

    def show_rules(self):
        rules_text = (
            "Правила игры в судоку:\n\n"
            "1. Заполните каждую ячейку числом от 1 до 9 так, чтобы каждая цифра встречалась "
            "в каждой строке, в каждом столбце и в каждом блоке 3x3.\n"
            "2. Заполните все ячейки, чтобы завершить игру."
        )

        rules_label = tk.Label(self.root, text=rules_text, font=("Arial", 18), justify="left")
        rules_label.pack(padx=20, pady=20)

        start_button = tk.Button(self.root, text="Начать игру", command=self.start_sudoku_game, font=("Arial", 16))
        start_button.pack(pady=20)

    def start_sudoku_game(self):
        # Удаляем правила и начинаем игру
        for widget in self.root.winfo_children():
            widget.destroy()
        sudoku_game = SudokuGame(self.root, self.show_rules)


if __name__ == "__main__":
    root = tk.Tk()
    app = BrainCrushApp(root)
    root.mainloop()

# admin.py
import tkinter as tk
from tkinter import messagebox
from database import Database


class AdminApp:
    def __init__(self, root, db, back_callback):
        self.root = root
        self.db = db 
        self.back_callback = back_callback

        self.show_admin_menu()

    def show_admin_menu(self):
        # Уничтожаем предыдущие виджеты в self.root
        for widget in self.root.winfo_children():
            widget.destroy()

        admin_menu_frame = tk.Frame(self.root)
        admin_menu_frame.pack()

        title_label = tk.Label(admin_menu_frame, text="Режим администратора", font=("Arial", 30))
        title_label.pack(pady=20)

        view_profiles_button = tk.Button(admin_menu_frame, text="Просмотреть профили", command=self.show_profiles_window)
        view_profiles_button.pack(pady=10)

        view_stats_profiles_button = tk.Button(admin_menu_frame, text="Cтатистика профилей", command=self.show_stats_profiles_window)
        view_stats_profiles_button.pack(pady=10)

        delete_profile_button = tk.Button(admin_menu_frame, text="Удалить профиль", command=self.show_delete_profile_window)
        delete_profile_button.pack(pady=10)

        back_button = tk.Button(admin_menu_frame, text="Вернуться в главное меню", command=self.back_to_main_menu)
        back_button.pack(pady=10)

    def show_profiles_window(self):
        profiles = self.db.get_all_users()

        if not profiles:
            messagebox.showinfo("Информация", "База данных профилей пуста!")
            self.show_admin_menu()

        else:
            profiles_text = "\n".join([f"'ID': {profile[0]}, 'Username': {profile[1]}, 'Password': {profile[2]}" for profile in profiles])
            messagebox.showinfo("Список профилей", profiles_text)

        def show_stats_profiles_window(self):
            profiles = self.db.get_all_users()
            if not profiles:
                messagebox.showinfo("Информация", "Нет доступных профилей для просмотра!")
                self.show_admin_menu()
                return
    
            for widget in self.root.winfo_children():
                widget.destroy()
    
            stats_profile_frame = tk.Frame(self.root)
            stats_profile_frame.pack()
    
            title_label = tk.Label(stats_profile_frame, text="Режим администратора", font=("Arial", 30))
            title_label.pack(pady=20)
    
            username_label = tk.Label(stats_profile_frame, text="Выберите профиль для просмотра:")
            username_label.pack()
    
            profile_names = [profile[1] for profile in profiles]
    
            selected_profile = tk.StringVar(value=profile_names[0])
    
            profiles_menu = tk.OptionMenu(stats_profile_frame, selected_profile, *profile_names)
            profiles_menu.pack(pady=10)
    
            def stats_profile():
                username_to_show = selected_profile.get()
                user_data = self.db.get_user(username_to_show)
    
                if not user_data:
                    messagebox.showinfo("Ошибка", f"Профиль {username_to_show} не найден!")
                    return
    
                # Извлекаем данные профиля
                username = user_data[1]
                snake_score = user_data[4]
                tic_tac_toe_wins = user_data[3]
                sudoku_solved = user_data[5]
                race_score = user_data[6]
                dino_score = user_data[7]
    
                # Формируем текст статистики
                stats_text = f"Имя пользователя: {username}\n" \
                             f"Очки в змейку: {snake_score}\n" \
                             f"Победы в крестики-нолики: {tic_tac_toe_wins}\n" \
                             f"Решенные судоку: {sudoku_solved}\n" \
                             f"Рекорд в динозавре: {dino_score}\n" \
                             f"Рекорд в гонках: {race_score}"
    
                messagebox.showinfo("Статистика профиля", stats_text)
    
            delete_button = tk.Button(stats_profile_frame, text="Просмотреть профиль", command=stats_profile)
            delete_button.pack(pady=20)
    
            back_button = tk.Button(stats_profile_frame, text="Назад", command=self.show_admin_menu)
            back_button.pack(pady=10)

    def show_delete_profile_window(self):
        profiles = self.db.get_all_users()
        if not profiles:
            messagebox.showinfo("Информация", "Нет доступных профилей для удаления!")
            self.show_admin_menu()
            return

        for widget in self.root.winfo_children():
            widget.destroy()

        delete_profile_frame = tk.Frame(self.root)
        delete_profile_frame.pack()

        title_label = tk.Label(delete_profile_frame, text="Режим администратора", font=("Arial", 30))
        title_label.pack(pady=20)

        username_label = tk.Label(delete_profile_frame, text="Выберите профиль для удаления:")
        username_label.pack()

        profile_names = [profile[1] for profile in profiles]

        selected_profile = tk.StringVar(value=profile_names[0])

        profiles_menu = tk.OptionMenu(delete_profile_frame, selected_profile, *profile_names)
        profiles_menu.pack(pady=10)

        def delete_profile():
            username_to_delete = selected_profile.get()
            self.db.delete_user(username_to_delete)
            messagebox.showinfo("Успех", f"Профиль {username_to_delete} удален!")
            self.show_admin_menu()

        delete_button = tk.Button(delete_profile_frame, text="Удалить профиль", command=delete_profile)
        delete_button.pack(pady=20)

        back_button = tk.Button(delete_profile_frame, text="Назад", command=self.show_admin_menu)
        back_button.pack(pady=10)

    def back_to_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.back_callback()


if __name__ == "__main__":
    root = tk.Tk()
    app = AdminApp(root, Database(), lambda: print("Back to main menu"))
    root.mainloop()

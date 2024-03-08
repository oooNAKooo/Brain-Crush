# snake.py
import pygame
import random
import sys

class SnakeGame:
    def __init__(self, db, username):
        self.db = db
        self.username = username
        self.window_width = 800
        self.window_height = 600
        self.segment_size = 20
        self.segment_speed = 20
        self.game_window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.font_style = pygame.font.SysFont(None, 50)
        self.direction = "RIGHT"
        self.game_over = False
        self.snake_segments = [(self.window_width / 2, self.window_height / 2)]
        self.food_position = self.generate_food_position()
        self.score = 0  # Добавляем атрибут score и инициализируем его

    def show_score(self, score):
        score_text = self.font_style.render("Score: " + str(score), True, (255, 255, 255))  # Белый цвет текста
        self.game_window.blit(score_text, [10, 10])

    def draw_snake(self):
        for segment in self.snake_segments:
            pygame.draw.rect(self.game_window, (0, 255, 0), [segment[0], segment[1], self.segment_size, self.segment_size])

    def generate_food_position(self):
        x = round(random.randrange(0, self.window_width - self.segment_size) / self.segment_size) * self.segment_size
        y = round(random.randrange(0, self.window_height - self.segment_size) / self.segment_size) * self.segment_size
        return x, y

    def draw_food(self):
        pygame.draw.rect(self.game_window, (255, 0, 0), [self.food_position[0], self.food_position[1], self.segment_size, self.segment_size])

    def on_key_press(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and self.direction != "RIGHT":
                self.direction = "LEFT"
            elif event.key == pygame.K_RIGHT and self.direction != "LEFT":
                self.direction = "RIGHT"
            elif event.key == pygame.K_UP and self.direction != "DOWN":
                self.direction = "UP"
            elif event.key == pygame.K_DOWN and self.direction != "UP":
                self.direction = "DOWN"

    def move(self):
        x, y = self.snake_segments[0]
        if self.direction == "UP":
            y -= self.segment_speed
        elif self.direction == "DOWN":
            y += self.segment_speed
        elif self.direction == "LEFT":
            x -= self.segment_speed
        elif self.direction == "RIGHT":
            x += self.segment_speed
        self.snake_segments.insert(0, (x, y))

    def check_collision(self):
        x, y = self.snake_segments[0]
        if x >= self.window_width or x < 0 or y >= self.window_height or y < 0:
            self.game_over = True

        if self.snake_segments[0] == self.food_position:
            self.food_position = self.generate_food_position()
        else:
            self.snake_segments.pop()

    def update_display(self):
        self.game_window.fill((0, 0, 0))

        # Отрисовка границ экрана
        pygame.draw.rect(self.game_window, (255, 255, 255), [0, 0, self.window_width, self.segment_size])
        pygame.draw.rect(self.game_window, (255, 255, 255), [0, 0, self.segment_size, self.window_height])
        pygame.draw.rect(self.game_window, (255, 255, 255),
                         [0, self.window_height - self.segment_size, self.window_width, self.segment_size])
        pygame.draw.rect(self.game_window, (255, 255, 255),
                         [self.window_width - self.segment_size, 0, self.segment_size, self.window_height])

        self.draw_food()
        self.draw_snake()
        self.show_score(len(self.snake_segments))
        pygame.display.update()

    def game_over_screen(self, username, score):
        self.update_record(username, len(self.snake_segments))
        game_over_text = self.font_style.render("Game Over", True, (255, 255, 255))
        self.game_window.blit(game_over_text, [self.window_width / 4, self.window_height / 2])
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return

        # Пользователь возвращается в меню
        self.start_menu()

    def game_loop(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                else:
                    self.on_key_press(event)

            self.move()
            self.check_collision()
            self.update_display()

            self.clock.tick(self.segment_speed)

        # После выхода из игры, проверяем, был ли пользовательский ввод для выхода из программы
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pygame.quit()
                sys.exit()

        self.game_over_screen(self.username, self.score)
        pygame.quit()

    def start_menu(self):
        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        intro = False

            self.game_window.fill((0, 0, 0))
            start_text = self.font_style.render("Press SPACE to Play", True, (255, 255, 255))
            self.game_window.blit(start_text, [self.window_width / 4, self.window_height / 2])
            pygame.display.update()

        self.game_loop()

    def run(self):
        pygame.init()
        self.start_menu()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.on_key_press(event)

            if not self.game_over:
                self.on_key_press(pygame.event)

        pygame.quit()  # После выхода из цикла закрываем pygame, но не выходим из программы

    def update_record(self, username, score):
        try:
            # Получаем текущий рекорд пользователя из базы данных
            current_record = self.db.get_snake_score(username)
            if current_record is None:
                current_record = 0

            # Сравниваем текущий рекорд с новым счетом и обновляем его, если новый счет выше
            if score > current_record:
                self.db.update_snake_score(username, score)
        except Exception as e:
            print("Error updating record:", e)


if __name__ == "__main__":
    SnakeGame().run()

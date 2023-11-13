import turtle
import time
import random

score = 0
high_score = 0
delay = 0.1

# Creating a window screen
wind = turtle.Screen()
wind.title("Snake Maze")
wind.bgcolor("green")

# the width and height can be put as user's choice
wind.setup(width=600, height=600)
wind.tracer(0)

# head of the snake
head = turtle.Turtle()
head.shape("square")
head.color("white")
head.penup()
head.goto(0, 0)
head.direction = "Stop"

# food in the game
food = turtle.Turtle()
colors = random.choice(['red', 'green', 'black'])
shapes = random.choice(['square', 'triangle', 'circle'])
food.speed(0)
food.shape(shapes)
food.color(colors)
food.penup()
food.goto(0, 100)

pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 250)
pen.write("Score : 0  High Score : 0", align="center",
          font=("Arial", 24, "bold"))

# assigning key directions
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y+20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y-20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x-20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x+20)

def handle_keypress():
    wind.listen()
    wind.onkeypress(go_up, "w")
    wind.onkeypress(go_down, "s")
    wind.onkeypress(go_left, "a")
    wind.onkeypress(go_right, "d")

# Set up key bindings
handle_keypress()

def spawn_food():
    x = random.randint(-270, 270)
    y = random.randint(-270, 270)
    food.goto(x, y)

# Main Gameplay
def game_loop():
    global score, high_score, delay
    wind.update()

    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "Stop"
        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()
        score = 0
        delay = 0.1
        pen.clear()
        pen.write("Score : {} High Score : {} ".format(
            score, high_score), align="center", font=("Arial", 24, "bold"))

    if head.distance(food) < 20:
        spawn_food()
        create_segment()
        update_score()

    handle_collision()
    move_segments()
    move_head()

    wind.ontimer(game_loop, int(delay * 1000))

def create_segment():
    new_segment = turtle.Turtle()
    new_segment.speed(0)
    new_segment.shape("square")
    new_segment.color("orange")
    new_segment.penup()
    segments.append(new_segment)

def update_score():
    global score, high_score, delay
    score += 10
    if score > high_score:
        high_score = score
    pen.clear()
    pen.write("Score : {} High Score : {} ".format(
        score, high_score), align="center", font=("Arial", 24, "bold"))
    delay -= 0.001

def handle_collision():
    for segment in segments:
        if segment.distance(head) < 20:
            game_over()

def move_segments():
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

def move_head():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    elif head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
    elif head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
    elif head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

def game_over():
    time.sleep(1)
    head.goto(0, 0)
    head.direction = "Stop"
    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()

    score = 0
    delay = 0.1
    pen.clear()
    pen.write("Score : {} High Score : {} ".format(
        score, high_score), align="center", font=("Arial", 24, "bold"))

# Initial setup
segments = []

# Initial spawn
spawn_food()

# Start game loop
game_loop()

wind.mainloop()

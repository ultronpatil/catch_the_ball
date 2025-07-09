import tkinter as tk
import random

WIDTH = 400
HEIGHT = 500
BALL_SIZE = 30
PADDLE_WIDTH = 80
PADDLE_HEIGHT = 15
PADDLE_SPEED = 20

LEVEL_SPEED = {1: 5, 2: 8, 3: 12}

FIREBALL_SIZE = 30
LEVEL_FIREBALLS = {1: 1, 2: 2, 3: 3}        # Number of fireballs
LEVEL_FIREBALL_SPEED = {1: 3, 2: 6, 3: 9}   # Speed based on difficulty


class CatchTheBallGame:
    def __init__(self, root, canvas, level, back_to_menu):
        self.root = root
        self.canvas = canvas
        self.level = level
        self.back_to_menu = back_to_menu
        self.ball_speed = LEVEL_SPEED.get(level, 5)
        self.score = 0
        self.game_over = False
        self.back_button = None

        self.fireballs = []
        self.fireball_speed = LEVEL_FIREBALL_SPEED.get(level, 3)
        self.num_fireballs = LEVEL_FIREBALLS.get(level, 1)
        self.create_fireballs()


        self.ball = self.canvas.create_oval(0, 0, BALL_SIZE, BALL_SIZE, fill="red")
        self.paddle = self.canvas.create_rectangle(
            WIDTH//2 - PADDLE_WIDTH//2,
            HEIGHT - PADDLE_HEIGHT - 10,
            WIDTH//2 + PADDLE_WIDTH//2,
            HEIGHT - 10,
            fill="black"
        )
        self.text = self.canvas.create_text(WIDTH//2, 20, text="Score: 0", font=("Arial", 16))

        self.ball_x = random.randint(0, WIDTH - BALL_SIZE)
        self.ball_y = 0
        self.canvas.move(self.ball, self.ball_x, self.ball_y)

        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)

        self.update_game()

    def move_left(self, event):
        if not self.game_over:
            self.canvas.move(self.paddle, -PADDLE_SPEED, 0)

    def move_right(self, event):
        if not self.game_over:
            self.canvas.move(self.paddle, PADDLE_SPEED, 0)
    
    def create_fireballs(self):
        for _ in range(self.num_fireballs):
            x = random.randint(0, WIDTH - FIREBALL_SIZE)
            fb = self.canvas.create_oval(x, 0, x + FIREBALL_SIZE, FIREBALL_SIZE, fill="orange", outline="black")
            self.fireballs.append(fb)


    def update_game(self):
        if self.game_over:
            return

        # Move normal ball
        self.canvas.move(self.ball, 0, self.ball_speed)
        ball_pos = self.canvas.coords(self.ball)

        if ball_pos[3] >= HEIGHT:
            paddle_pos = self.canvas.coords(self.paddle)
            if paddle_pos[0] < ball_pos[2] and paddle_pos[2] > ball_pos[0]:
                self.score += 1
                self.canvas.itemconfig(self.text, text=f"Score: {self.score}")
                self.reset_ball()
            else:
                self.end_game()
                return

        # Move fireballs
        for fb in self.fireballs:
            self.canvas.move(fb, 0, self.fireball_speed)
            fb_pos = self.canvas.coords(fb)

            # If fireball touches paddle → game over!
            paddle_pos = self.canvas.coords(self.paddle)
            if paddle_pos[0] < fb_pos[2] and paddle_pos[2] > fb_pos[0] and fb_pos[3] >= paddle_pos[1]:
                self.end_game()
                return

            # Reset fireball if it goes off screen
            if fb_pos[3] > HEIGHT:
                self.canvas.coords(fb, random.randint(0, WIDTH - FIREBALL_SIZE), 0,
                                   random.randint(0, WIDTH - FIREBALL_SIZE) + FIREBALL_SIZE, FIREBALL_SIZE)

        self.root.after(30, self.update_game)


    def reset_ball(self):
        self.canvas.coords(self.ball, 0, 0, BALL_SIZE, BALL_SIZE)
        self.ball_x = random.randint(0, WIDTH - BALL_SIZE)
        self.canvas.move(self.ball, self.ball_x, 0)
    
    def clean_and_go_back(self):
        if self.back_button:
            self.back_button.destroy()  # 🧼 Remove button
        self.back_to_menu()


    def end_game(self):
        self.game_over = True
        self.canvas.create_text(WIDTH//2, HEIGHT//2, text="Game Over!", font=("Arial", 24), fill="red")

        # 🧠 Create and store the button
        self.back_button = tk.Button(self.root, text="Back to Menu", command=self.clean_and_go_back)
        self.back_button.place(x=160, y=HEIGHT//2 + 40)


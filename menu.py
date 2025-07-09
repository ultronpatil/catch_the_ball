import tkinter as tk

class MenuScreen:
    def __init__(self, root, canvas, start_callback):
        self.root = root
        self.canvas = canvas
        self.start_callback = start_callback
        self.buttons = []  # 🧠 Track buttons to destroy later

        self.draw_menu()

    def draw_menu(self):
        self.canvas.delete("all")
        self.canvas.create_text(200, 100, text="Catch the Ball", font=("Arial", 24, "bold"))

        self.canvas.create_text(200, 160, text="Select Level", font=("Arial", 16))
        self.add_button("Easy", 190, lambda: self.start_game(1))
        self.add_button("Medium", 230, lambda: self.start_game(2))
        self.add_button("Hard", 270, lambda: self.start_game(3))
        self.add_button("Exit", 310, self.root.destroy)

    def add_button(self, text, y, command):
        btn = tk.Button(self.root, text=text, width=10, command=command)
        btn.place(x=170, y=y)
        self.buttons.append(btn)

    def start_game(self, level):
        for btn in self.buttons:
            btn.destroy()  # 🧹 Clean up buttons
        self.start_callback(level)

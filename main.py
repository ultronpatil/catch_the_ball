import tkinter as tk
from menu import MenuScreen
from game import CatchTheBallGame

class GameApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=400, height=500, bg="lightblue")
        self.canvas.pack()
        self.show_menu()

    def show_menu(self):
        self.menu = MenuScreen(self.root, self.canvas, self.start_game)

    def start_game(self, level):
        self.canvas.delete("all")
        CatchTheBallGame(self.root, self.canvas, level, self.show_menu)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Catch the Ball")
    app = GameApp(root)
    root.mainloop()

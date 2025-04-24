
import tkinter as tk

class SpriteGirl:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = 50
        self.y = 50
        self.direction = 1  # 1 means right, -1 means left
        self.sprite = self.canvas.create_oval(self.x, self.y, self.x+20, self.y+20, fill="black")

    def move(self):
        # Move the sprite randomly on the canvas
        if self.x > 400 or self.x < 0:
            self.direction *= -1
        self.x += 5 * self.direction
        self.canvas.coords(self.sprite, self.x, self.y, self.x + 20, self.y + 20)
        self.canvas.after(50, self.move)

# Create the GUI window
def create_sprite_window():
    root = tk.Tk()
    root.title("Sprite Girl")
    canvas = tk.Canvas(root, width=500, height=500)
    canvas.pack()
    sprite = SpriteGirl(canvas)
    sprite.move()
    root.mainloop()

create_sprite_window()

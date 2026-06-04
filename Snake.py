import random
import tkinter as tk

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
GAME_SPEED = 120  # milliseconds between moves


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.canvas = tk.Canvas(
            root,
            width=CELL_SIZE * GRID_WIDTH,
            height=CELL_SIZE * GRID_HEIGHT,
            bg="#111111",
            highlightthickness=0,
        )
        self.canvas.pack()

        self.score = 0
        self.direction = "Right"
        self.next_direction = self.direction
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.snake_length = 4
        self.food = None
        self.game_over = False

        self.score_text = self.canvas.create_text(
            10,
            10,
            anchor="nw",
            fill="#ffffff",
            font=("Arial", 14, "bold"),
            text=f"Score: {self.score}",
        )

        self.spawn_food()
        self.draw_objects()

        self.root.bind("<Up>", lambda event: self.change_direction("Up"))
        self.root.bind("<Down>", lambda event: self.change_direction("Down"))
        self.root.bind("<Left>", lambda event: self.change_direction("Left"))
        self.root.bind("<Right>", lambda event: self.change_direction("Right"))
        self.root.bind("<Return>", lambda event: self.restart())

        self.run()

    def spawn_food(self):
        available_positions = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in self.snake
        ]
        if not available_positions:
            self.food = None
            return
        self.food = random.choice(available_positions)

    def change_direction(self, new_direction):
        opposite = {
            "Up": "Down",
            "Down": "Up",
            "Left": "Right",
            "Right": "Left",
        }
        if new_direction != opposite.get(self.direction):
            self.next_direction = new_direction

    def move_snake(self):
        if self.game_over:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        if self.direction == "Up":
            head_y -= 1
        elif self.direction == "Down":
            head_y += 1
        elif self.direction == "Left":
            head_x -= 1
        elif self.direction == "Right":
            head_x += 1

        new_head = (head_x, head_y)

        if (
            head_x < 0
            or head_x >= GRID_WIDTH
            or head_y < 0
            or head_y >= GRID_HEIGHT
            or new_head in self.snake
        ):
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.snake_length += 1
            self.spawn_food()
            self.canvas.itemconfigure(self.score_text, text=f"Score: {self.score}")
        if len(self.snake) > self.snake_length:
            self.snake.pop()

    def draw_objects(self):
        self.canvas.delete("snake")
        self.canvas.delete("food")
        self.canvas.delete("game_over")

        for index, (x, y) in enumerate(self.snake):
            color = "#00ff00" if index == 0 else "#88ff88"
            self.canvas.create_rectangle(
                x * CELL_SIZE,
                y * CELL_SIZE,
                (x + 1) * CELL_SIZE,
                (y + 1) * CELL_SIZE,
                fill=color,
                width=0,
                tags="snake",
            )

        if self.food:
            fx, fy = self.food
            self.canvas.create_oval(
                fx * CELL_SIZE + 2,
                fy * CELL_SIZE + 2,
                (fx + 1) * CELL_SIZE - 2,
                (fy + 1) * CELL_SIZE - 2,
                fill="#ff4444",
                outline="",
                tags="food",
            )

        if self.game_over:
            self.canvas.create_text(
                CELL_SIZE * GRID_WIDTH // 2,
                CELL_SIZE * GRID_HEIGHT // 2,
                text="Game Over\nPress Enter to Restart",
                fill="#ffffff",
                font=("Arial", 24, "bold"),
                justify="center",
                tags="game_over",
            )

    def restart(self):
        if not self.game_over:
            return
        self.score = 0
        self.direction = "Right"
        self.next_direction = self.direction
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.snake_length = 4
        self.food = None
        self.game_over = False
        self.canvas.itemconfigure(self.score_text, text=f"Score: {self.score}")
        self.spawn_food()
        self.draw_objects()
        self.run()

    def run(self):
        self.move_snake()
        self.draw_objects()
        if not self.game_over:
            self.root.after(GAME_SPEED, self.run)


if __name__ == "__main__":
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()

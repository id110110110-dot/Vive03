import random
import tkinter as tk

CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20
GAME_SPEED = 120  # milliseconds between moves

DIRECTIONS = {
    "Up": (0, -1),
    "Down": (0, 1),
    "Left": (-1, 0),
    "Right": (1, 0),
}
OPPOSITE = {
    "Up": "Down",
    "Down": "Up",
    "Left": "Right",
    "Right": "Left",
}


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game: Human vs AI")
        self.canvas = tk.Canvas(
            root,
            width=CELL_SIZE * GRID_WIDTH,
            height=CELL_SIZE * GRID_HEIGHT,
            bg="#111111",
            highlightthickness=0,
        )
        self.canvas.pack()

        self.food = None
        self.human_alive = True
        self.ai_alive = True

        self.human_score = 0
        self.ai_score = 0

        self.human_direction = "Right"
        self.human_next_direction = "Right"
        self.human_snake = [(5, GRID_HEIGHT // 2)]
        self.human_length = 5

        self.ai_direction = "Left"
        self.ai_snake = [(GRID_WIDTH - 6, GRID_HEIGHT // 2)]
        self.ai_length = 5

        self.status_text = self.canvas.create_text(
            10,
            10,
            anchor="nw",
            fill="#ffffff",
            font=("Arial", 14, "bold"),
            text=self._score_text(),
        )

        self.spawn_food()
        self.draw_objects()

        self.root.bind("<Up>", lambda event: self.change_direction("Up"))
        self.root.bind("<Down>", lambda event: self.change_direction("Down"))
        self.root.bind("<Left>", lambda event: self.change_direction("Left"))
        self.root.bind("<Right>", lambda event: self.change_direction("Right"))
        self.root.bind("<Return>", lambda event: self.restart())

        self.run()

    def _score_text(self):
        return f"Human: {self.human_score}   AI: {self.ai_score}"

    def spawn_food(self):
        occupied = set(self.human_snake + self.ai_snake)
        available_positions = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in occupied
        ]
        self.food = random.choice(available_positions) if available_positions else None

    def change_direction(self, new_direction):
        if not self.human_alive:
            return
        if new_direction != OPPOSITE.get(self.human_direction):
            self.human_next_direction = new_direction

    def safe_move(self, new_head, snake_body):
        if (
            new_head[0] < 0
            or new_head[0] >= GRID_WIDTH
            or new_head[1] < 0
            or new_head[1] >= GRID_HEIGHT
        ):
            return False
        return new_head not in snake_body

    def choose_ai_direction(self):
        best_move = None
        best_score = float('inf')
        head_x, head_y = self.ai_snake[0]
        occupied = set(self.human_snake + self.ai_snake[:-1])

        for direction, delta in DIRECTIONS.items():
            if direction == OPPOSITE.get(self.ai_direction):
                continue
            new_head = (head_x + delta[0], head_y + delta[1])
            if not self.safe_move(new_head, occupied):
                continue
            if self.food:
                score = abs(new_head[0] - self.food[0]) + abs(new_head[1] - self.food[1])
            else:
                score = random.random()
            if score < best_score:
                best_score = score
                best_move = direction

        return best_move or self.ai_direction

    def move_snake(self, snake, direction, next_direction, length, occupied_other):
        if not snake:
            return snake, direction, length, False

        direction = next_direction
        head_x, head_y = snake[0]
        dx, dy = DIRECTIONS[direction]
        new_head = (head_x + dx, head_y + dy)

        collision = (
            new_head[0] < 0
            or new_head[0] >= GRID_WIDTH
            or new_head[1] < 0
            or new_head[1] >= GRID_HEIGHT
            or new_head in snake
            or new_head in occupied_other
        )
        if collision:
            return snake, direction, length, True

        snake = [new_head] + snake
        ate_food = new_head == self.food
        if ate_food:
            length += 1
        if len(snake) > length:
            snake.pop()

        return snake, direction, length, False

    def draw_objects(self):
        self.canvas.delete("snake")
        self.canvas.delete("ai_snake")
        self.canvas.delete("food")
        self.canvas.delete("game_over")

        for index, (x, y) in enumerate(self.human_snake):
            color = "#00ff00" if index == 0 else "#55ff55"
            self.canvas.create_rectangle(
                x * CELL_SIZE,
                y * CELL_SIZE,
                (x + 1) * CELL_SIZE,
                (y + 1) * CELL_SIZE,
                fill=color,
                width=0,
                tags="snake",
            )

        for index, (x, y) in enumerate(self.ai_snake):
            color = "#ffcc00" if index == 0 else "#ffaa33"
            self.canvas.create_rectangle(
                x * CELL_SIZE,
                y * CELL_SIZE,
                (x + 1) * CELL_SIZE,
                (y + 1) * CELL_SIZE,
                fill=color,
                width=0,
                tags="ai_snake",
            )

        if self.food:
            fx, fy = self.food
            self.canvas.create_oval(
                fx * CELL_SIZE + 3,
                fy * CELL_SIZE + 3,
                (fx + 1) * CELL_SIZE - 3,
                (fy + 1) * CELL_SIZE - 3,
                fill="#ff4444",
                outline="",
                tags="food",
            )

        self.canvas.itemconfigure(self.status_text, text=self._score_text())

        if not self.human_alive and not self.ai_alive:
            winner_text = "Draw"
            if self.human_score > self.ai_score:
                winner_text = "Human Wins"
            elif self.ai_score > self.human_score:
                winner_text = "AI Wins"
            self.canvas.create_text(
                CELL_SIZE * GRID_WIDTH // 2,
                CELL_SIZE * GRID_HEIGHT // 2,
                text=f"Game Over\n{winner_text}\nPress Enter to Restart",
                fill="#ffffff",
                font=("Arial", 24, "bold"),
                justify="center",
                tags="game_over",
            )

    def restart(self):
        self.human_alive = True
        self.ai_alive = True
        self.human_score = 0
        self.ai_score = 0
        self.human_direction = "Right"
        self.human_next_direction = "Right"
        self.human_snake = [(5, GRID_HEIGHT // 2)]
        self.human_length = 5
        self.ai_direction = "Left"
        self.ai_snake = [(GRID_WIDTH - 6, GRID_HEIGHT // 2)]
        self.ai_length = 5
        self.food = None
        self.spawn_food()
        self.draw_objects()
        self.run()

    def run(self):
        if self.human_alive:
            self.human_direction = self.human_next_direction
        if self.ai_alive:
            self.ai_direction = self.choose_ai_direction()

        occupied_by_human = set(self.human_snake[1:])
        occupied_by_ai = set(self.ai_snake[1:])

        if self.human_alive:
            self.human_snake, self.human_direction, self.human_length, human_dead = self.move_snake(
                self.human_snake,
                self.human_direction,
                self.human_next_direction,
                self.human_length,
                occupied_by_ai,
            )
            self.human_alive = not human_dead

        if self.ai_alive:
            self.ai_snake, self.ai_direction, self.ai_length, ai_dead = self.move_snake(
                self.ai_snake,
                self.ai_direction,
                self.ai_direction,
                self.ai_length,
                occupied_by_human,
            )
            self.ai_alive = not ai_dead

        if self.human_alive and self.ai_alive and self.human_snake[0] == self.ai_snake[0]:
            self.human_alive = False
            self.ai_alive = False

        if self.food:
            if self.human_alive and self.human_snake[0] == self.food:
                self.human_score += 1
                self.spawn_food()
            elif self.ai_alive and self.ai_snake[0] == self.food:
                self.ai_score += 1
                self.spawn_food()

        self.draw_objects()

        if self.human_alive or self.ai_alive:
            self.root.after(GAME_SPEED, self.run)


if __name__ == "__main__":
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()

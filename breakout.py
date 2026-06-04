import tkinter as tk


class Breakout:
    def __init__(self, root):
        self.root = root
        self.W, self.H = 800, 600
        self.canvas = tk.Canvas(root, width=self.W, height=self.H, bg="#111")
        self.canvas.pack()

        self.paddle_w, self.paddle_h = 100, 12
        self.paddle = self.canvas.create_rectangle(0, 0, self.paddle_w, self.paddle_h, fill="#fff")
        self.reset_paddle()

        self.ball_r = 8
        self.ball = self.canvas.create_oval(0, 0, self.ball_r*2, self.ball_r*2, fill="#ffcc00")
        self.ball_dx = 4
        self.ball_dy = -4
        self.reset_ball()

        self.brick_rows = 5
        self.brick_cols = 8
        self.brick_padding = 6
        self.brick_area_h = 200
        self.bricks = []
        self.create_bricks()

        self.score = 0
        self.lives = 3
        self.text_score = self.canvas.create_text(70, 20, text=f"Score: {self.score}", fill="#fff", font=(None, 14))
        self.text_lives = self.canvas.create_text(720, 20, text=f"Lives: {self.lives}", fill="#fff", font=(None, 14))

        self.running = True
        self.root.bind("<Left>", lambda e: self.move_paddle(-30))
        self.root.bind("<Right>", lambda e: self.move_paddle(30))
        self.root.bind("<KeyPress-a>", lambda e: self.move_paddle(-30))
        self.root.bind("<KeyPress-d>", lambda e: self.move_paddle(30))

        self.update()

    def reset_paddle(self):
        x = (self.W - self.paddle_w) / 2
        y = self.H - 40
        self.canvas.coords(self.paddle, x, y, x + self.paddle_w, y + self.paddle_h)

    def reset_ball(self):
        px1, py1, px2, py2 = self.canvas.coords(self.paddle)
        bx = (px1 + px2) / 2
        by = py1 - self.ball_r*2 - 2
        self.canvas.coords(self.ball, bx - self.ball_r, by - self.ball_r, bx + self.ball_r, by + self.ball_r)
        self.ball_dx = 4
        self.ball_dy = -4

    def move_paddle(self, dx):
        x1, y1, x2, y2 = self.canvas.coords(self.paddle)
        nx1 = max(0, x1 + dx)
        nx2 = min(self.W, x2 + dx)
        if nx2 - nx1 < self.paddle_w:
            # hit edge
            if nx1 == 0:
                nx2 = self.paddle_w
            else:
                nx1 = self.W - self.paddle_w
        self.canvas.coords(self.paddle, nx1, y1, nx2, y2)

    def create_bricks(self):
        self.bricks.clear()
        brick_w = (self.W - (self.brick_cols + 1) * self.brick_padding) / self.brick_cols
        brick_h = (self.brick_area_h - (self.brick_rows + 1) * self.brick_padding) / self.brick_rows
        colors = ["#ff6b6b", "#ff9f43", "#feca57", "#48dbfb", "#5f27cd"]
        for r in range(self.brick_rows):
            y1 = self.brick_padding + r * (brick_h + self.brick_padding)
            for c in range(self.brick_cols):
                x1 = self.brick_padding + c * (brick_w + self.brick_padding)
                x2 = x1 + brick_w
                y2 = y1 + brick_h
                b = self.canvas.create_rectangle(x1, y1, x2, y2, fill=colors[r % len(colors)], width=1, outline="#222", tags=("brick",))
                self.bricks.append(b)

    def update(self):
        if not self.running:
            return

        # move ball
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        bx1, by1, bx2, by2 = self.canvas.coords(self.ball)

        # wall collisions
        if bx1 <= 0:
            self.ball_dx = abs(self.ball_dx)
        if bx2 >= self.W:
            self.ball_dx = -abs(self.ball_dx)
        if by1 <= 0:
            self.ball_dy = abs(self.ball_dy)

        # bottom (lose life)
        if by2 >= self.H:
            self.lives -= 1
            self.canvas.itemconfigure(self.text_lives, text=f"Lives: {self.lives}")
            if self.lives <= 0:
                self.game_over(False)
                return
            else:
                self.reset_ball()
                self.root.after(500, self.update)
                return

        # check collisions
        items = self.canvas.find_overlapping(bx1, by1, bx2, by2)
        for it in items:
            if it == self.ball:
                continue
            tags = self.canvas.gettags(it)
            if "brick" in tags:
                # remove brick, bounce
                try:
                    self.canvas.delete(it)
                    self.bricks.remove(it)
                except Exception:
                    pass
                self.score += 10
                self.canvas.itemconfigure(self.text_score, text=f"Score: {self.score}")
                self.ball_dy *= -1
                break
            elif it == self.paddle:
                # bounce with angle based on hit position
                px1, py1, px2, py2 = self.canvas.coords(self.paddle)
                paddle_center = (px1 + px2) / 2
                ball_center = (bx1 + bx2) / 2
                offset = (ball_center - paddle_center) / (self.paddle_w / 2)
                self.ball_dx = max(-6, min(6, self.ball_dx + offset * 3))
                self.ball_dy = -abs(self.ball_dy)
                break

        # check win
        if not any(self.canvas.find_withtag("brick")):
            self.game_over(True)
            return

        self.root.after(16, self.update)

    def game_over(self, win):
        self.running = False
        msg = "You Win!" if win else "Game Over"
        self.canvas.create_text(self.W/2, self.H/2 - 20, text=msg, fill="#fff", font=(None, 36))
        self.canvas.create_text(self.W/2, self.H/2 + 20, text=f"Score: {self.score}", fill="#ddd", font=(None, 20))


def main():
    root = tk.Tk()
    root.title("Breakout - tkinter")
    game = Breakout(root)
    root.mainloop()


if __name__ == "__main__":
    main()

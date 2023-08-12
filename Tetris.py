import tkinter as tk
import random

WIDTH = 10
HEIGHT = 20
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 0], [1, 1, 1]],
]
COLORS = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF", "#00FFFF"]



class TetrisGame:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(master, width=WIDTH * 30, height=HEIGHT * 30, borderwidth=0, highlightthickness=0)
        self.canvas.pack()
        self.board = [[0] * WIDTH for _ in range(HEIGHT)]
        self.current_shape, self.current_shape_color_index = self.create_shape()
        self.current_shape_x = 0
        self.current_shape_y = 0
        self.score = 0
        self.is_game_over = False

        self.master.bind("<Left>", self.move_left)
        self.master.bind("<Right>", self.move_right)
        self.master.bind("<Down>", self.move_down)
        self.master.bind("<Up>", self.rotate_shape)

        self.timer()

    def timer(self):
        if not self.is_game_over:
            self.update()
            self.master.after(500, self.timer)

    def update(self):
        if self.can_move_down():
            self.current_shape_y += 1
        else:
            self.place_shape()
            self.check_lines()
            if self.is_game_over:
                return
            self.current_shape, self.current_shape_color_index = self.create_shape()
            self.current_shape_x = WIDTH // 2 - len(self.current_shape[0]) // 2
            self.current_shape_y = 0
            if not self.can_move_down():
                self.is_game_over = True

        self.draw_board()

    def move_left(self, event):
        if self.can_move_left():
            self.current_shape_x -= 1
            self.draw_board()

    def move_right(self, event):
        if self.can_move_right():
            self.current_shape_x += 1
            self.draw_board()

    def move_down(self, event):
        if self.can_move_down():
            self.current_shape_y += 1
            self.draw_board()

    def rotate_shape(self, event):
        rotated_shape = list(zip(*reversed(self.current_shape)))
        if self.can_rotate(rotated_shape):
        # Store the current position before rotating
            original_x = self.current_shape_x
            original_y = self.current_shape_y

        # Update the shape and draw it at the original position
        self.current_shape = rotated_shape
        self.draw_board()

        # If the rotated shape is not valid, revert to the original position
        if not self.can_move_down():
            self.current_shape_x = original_x
            self.current_shape_y = original_y
            self.current_shape = self.create_shape()[0]


    def can_move_left(self):
        for row in range(len(self.current_shape)):
            for col in range(len(self.current_shape[row])):
                if self.current_shape[row][col] and (
                    self.current_shape_x + col <= 0 or self.board[self.current_shape_y + row][self.current_shape_x + col - 1]
                ):
                    return False
        return True

    def can_move_right(self):
        for row in range(len(self.current_shape)):
            for col in range(len(self.current_shape[row])):
                if self.current_shape[row][col] and (
                    self.current_shape_x + col >= WIDTH - 1 or self.board[self.current_shape_y + row][self.current_shape_x + col + 1]
                ):
                    return False
        return True

    def can_move_down(self):
        for row in range(len(self.current_shape)):
            for col in range(len(self.current_shape[row])):
                if self.current_shape[row][col]:
                    next_row = self.current_shape_y + row + 1
                    if (
                        next_row >= HEIGHT or
                        (self.board[next_row][self.current_shape_x + col] and
                        self.board[next_row][self.current_shape_x + col] != self.current_shape_color_index)
                    ):
                        return False
        return True



    def can_rotate(self, rotated_shape):
        for row in range(len(rotated_shape)):
            for col in range(len(rotated_shape[row])):
                if (
                    rotated_shape[row][col]
                    and (
                        self.current_shape_x + col < 0
                        or self.current_shape_x + col >= WIDTH
                        or self.current_shape_y + row < 0
                        or self.current_shape_y + row >= HEIGHT
                        or self.board[self.current_shape_y + row][self.current_shape_x + col]
                    )
                ):
                    return False
        return True

    def place_shape(self):
        for row in range(len(self.current_shape)):
            for col in range(len(self.current_shape[row])):
                if self.current_shape[row][col]:
                    self.board[self.current_shape_y + row][self.current_shape_x + col] = self.current_shape_color_index


    def check_lines(self):
        full_lines = []
        for row in range(HEIGHT):
            if all(self.board[row]):
                full_lines.append(row)

        for row in full_lines:
            self.board.pop(row)
            self.board.insert(0, [0] * WIDTH)
            self.score += 10

    def create_shape(self):
        index = random.randint(0, len(SHAPES) - 1)
        shape = SHAPES[index]
        color_index = index % (len(COLORS) - 1)  # Modulo to avoid the black color index
        return shape, color_index


    def draw_board(self):
        self.canvas.delete("block")
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell:
                    x1 = x * 30
                    y1 = y * 30
                    x2 = x1 + 30
                    y2 = y1 + 30
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLORS[cell], tags="block")

        for row in range(len(self.current_shape)):
            for col in range(len(self.current_shape[row])):
                if self.current_shape[row][col]:
                    x = self.current_shape_x + col
                    y = self.current_shape_y + row
                    x1 = x * 30
                    y1 = y * 30
                    x2 = x1 + 30
                    y2 = y1 + 30
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLORS[self.current_shape_color_index], tags="block")




root = tk.Tk()
root.title("Tetris")
game = TetrisGame(root)
root.mainloop()

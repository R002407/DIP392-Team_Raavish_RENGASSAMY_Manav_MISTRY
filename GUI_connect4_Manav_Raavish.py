import tkinter as tk
from tkinter import messagebox
import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER_ONE = 1
PLAYER_TWO = 2
CELL_SIZE = 100

def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def is_board_full(board):
    return not any(is_valid_location(board, c) for c in range(COLUMN_COUNT))

class ConnectFourGame:
    def __init__(self, root, player1_name, player2_name):
        self.root = root
        self.root.title("Connect Four")
        self.board = create_board()
        self.turn = PLAYER_ONE
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.create_widgets()

    def create_widgets(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10, fill=tk.X)

        self.turn_label = tk.Label(top_frame, text=f"Turn: {self.player1_name}", font=("Helvetica", 14))
        self.turn_label.grid(row=0, column=0, padx=5)

        exit_button = tk.Button(top_frame, text="Exit", command=self.root.quit, bg="red", fg="white", font=("Helvetica", 14))
        exit_button.grid(row=0, column=1, padx=5)

        restart_button = tk.Button(top_frame, text="Restart", command=self.reset_game, bg="green", fg="white", font=("Helvetica", 14))
        restart_button.grid(row=0, column=2, padx=5)

        rules_button = tk.Button(top_frame, text="Rules", command=self.show_rules, bg="blue", fg="white", font=("Helvetica", 14))
        rules_button.grid(row=0, column=3, padx=5)

        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=1)
        top_frame.columnconfigure(2, weight=1)
        top_frame.columnconfigure(3, weight=1)

        self.canvas = tk.Canvas(self.root, width=COLUMN_COUNT*CELL_SIZE, height=(ROW_COUNT+1)*CELL_SIZE, bg="blue")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)

        self.draw_board()

    def handle_click(self, event):
        col = event.x // CELL_SIZE
        if is_valid_location(self.board, col):
            row = get_next_open_row(self.board, col)
            drop_piece(self.board, row, col, self.turn)
            self.draw_board()  # Redraw the board to reflect the new piece

            if winning_move(self.board, self.turn):
                self.root.after(100, self.show_winner, self.turn)  # Delay to allow the board to update
                return

            if is_board_full(self.board):
                self.root.after(100, self.show_draw)  # Delay to allow the board to update
                return

            self.turn = PLAYER_TWO if self.turn == PLAYER_ONE else PLAYER_ONE
            self.update_turn_label()
        else:
            messagebox.showwarning("Connect Four", "Column is full! Choose another one.")

    def draw_board(self):
        self.canvas.delete("all")

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                x_start = c * CELL_SIZE
                y_start = (ROW_COUNT - r) * CELL_SIZE  # Invert row index to draw from bottom
                x_end = x_start + CELL_SIZE
                y_end = y_start + CELL_SIZE
                color = "black"
                if self.board[r][c] == PLAYER_ONE:
                    color = "red"
                elif self.board[r][c] == PLAYER_TWO:
                    color = "yellow"
                self.canvas.create_oval(x_start+10, y_start+10, x_end-10, y_end-10, fill=color, outline="white")

        # Draw the grid
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                x_start = c * CELL_SIZE
                y_start = (ROW_COUNT - r) * CELL_SIZE
                x_end = x_start + CELL_SIZE
                y_end = y_start + CELL_SIZE
                self.canvas.create_rectangle(x_start, y_start, x_end, y_end, outline="white")

    def show_winner(self, winner):
        winner_text = self.player1_name if winner == PLAYER_ONE else self.player2_name
        messagebox.showinfo("Connect Four", f"{winner_text} wins !")
        self.reset_game()

    def show_draw(self):
        messagebox.showinfo("Connect Four", "We have a draw !")
        self.reset_game()

    def reset_game(self):
        self.board = create_board()
        self.turn = PLAYER_ONE
        self.update_turn_label()
        self.draw_board()

    def show_rules(self):
        rules = ("To play, take turns inserting a disc of your color into one of the columns of the grid, "
                 "trying to form a line of four.\n\n"
                 "To win Connect 4, align four of your tokens horizontally, vertically, or diagonally "
                 "before your opponent.")
        messagebox.showinfo("Connect Four Rules", rules)

    def update_turn_label(self):
        current_player = self.player1_name if self.turn == PLAYER_ONE else self.player2_name
        self.turn_label.config(text=f"Turn: {current_player}")

def start_game(player1_name, player2_name):
    root = tk.Tk()
    game = ConnectFourGame(root, player1_name, player2_name)
    root.mainloop()

def show_start_screen():
    start_screen = tk.Tk()
    start_screen.title("Connect Four - Start Game")

    tk.Label(start_screen, text="Player 1 :").grid(row=0, column=0, padx=10, pady=10)
    player1_entry = tk.Entry(start_screen)
    player1_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(start_screen, text="Player 2 :").grid(row=1, column=0, padx=10, pady=10)
    player2_entry = tk.Entry(start_screen)
    player2_entry.grid(row=1, column=1, padx=10, pady=10)

    def on_start_game():
        player1_name = player1_entry.get()
        player2_name = player2_entry.get()
        if not player1_name or not player2_name:
            messagebox.showwarning("Connect Four", "Please enter names for both players.")
            return
        start_screen.destroy()
        start_game(player1_name, player2_name)

    start_button = tk.Button(start_screen, text="Start Game", command=on_start_game, bg="green", fg="white", font=("Helvetica", 16, "bold"))
    start_button.grid(row=2, columnspan=2, pady=20)

    start_screen.mainloop()

if __name__ == "__main__":
    show_start_screen()

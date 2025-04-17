import tkinter as tk
from tkinter import font
from typing import NamedTuple

# --- Data Models ---
class Player(NamedTuple):
    label: str
    color: str
    is_human: bool

class Move(NamedTuple):
    row: int
    col: int
    label: str = ""

# --- Constants ---
BOARD_SIZE = 3
HUMAN = Player(label="X", color="blue", is_human=True)
AI = Player(label="O", color="green", is_human=False)

# --- Game Logic ---
class TicTacToeGame:
    def __init__(self):
        self.players = (HUMAN, AI)
        self.current_player = HUMAN
        self.board_size = BOARD_SIZE
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self._setup_board()

    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self):
        rows = [[(r, c) for c in range(self.board_size)] for r in range(self.board_size)]
        cols = [[(r, c) for r in range(self.board_size)] for c in range(self.board_size)]
        diag1 = [(i, i) for i in range(self.board_size)]
        diag2 = [(i, self.board_size - 1 - i) for i in range(self.board_size)]
        return rows + cols + [diag1, diag2]

    def is_valid_move(self, move):
        return (
            not self._has_winner
            and self._current_moves[move.row][move.col].label == ""
        )

    def process_move(self, move):
        self._current_moves[move.row][move.col] = move
        for combo in self._winning_combos:
            results = set(self._current_moves[r][c].label for r, c in combo)
            if len(results) == 1 and "" not in results:
                self._has_winner = True
                self.winner_combo = combo
                break

    def has_winner(self):
        return self._has_winner

    def is_tied(self):
        return (
            not self._has_winner
            and all(cell.label != "" for row in self._current_moves for cell in row)
        )

    def reset_game(self):
        self._setup_board()
        self._has_winner = False
        self.winner_combo = []
        self.current_player = HUMAN

    def toggle_player(self):
        self.current_player = AI if self.current_player == HUMAN else HUMAN

    def best_move(self):
        def minimax(board, player):
            if self._check_win(board, AI.label):
                return 1
            elif self._check_win(board, HUMAN.label):
                return -1
            elif all(cell.label != "" for row in board for cell in row):
                return 0

            if player == AI.label:
                best_score = -float("inf")
                for row in range(self.board_size):
                    for col in range(self.board_size):
                        if board[row][col].label == "":
                            board[row][col] = Move(row, col, AI.label)
                            score = minimax(board, HUMAN.label)
                            board[row][col] = Move(row, col, "")
                            best_score = max(score, best_score)
                return best_score
            else:
                best_score = float("inf")
                for row in range(self.board_size):
                    for col in range(self.board_size):
                        if board[row][col].label == "":
                            board[row][col] = Move(row, col, HUMAN.label)
                            score = minimax(board, AI.label)
                            board[row][col] = Move(row, col, "")
                            best_score = min(score, best_score)
                return best_score

        best_score = -float("inf")
        move = None
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self._current_moves[row][col].label == "":
                    self._current_moves[row][col] = Move(row, col, AI.label)
                    score = minimax(self._current_moves, HUMAN.label)
                    self._current_moves[row][col] = Move(row, col, "")
                    if score > best_score:
                        best_score = score
                        move = Move(row, col, AI.label)
        return move

    def _check_win(self, board, label):
        for combo in self._winning_combos:
            if all(board[r][c].label == label for r, c in combo):
                return True
        return False

# --- GUI Board ---
class TicTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Unbeatable Tic-Tac-Toe")
        self.geometry("400x450")
        self._game = game
        self._cells = {}
        self._create_menu()
        self._create_display()
        self._create_grid()
        self._update_display(f"{self._game.current_player.label}'s turn")

    def _create_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Play Again", command=self.reset_board)
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def _create_display(self):
        display_frame = tk.Frame(self, height=50)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            display_frame,
            text="",
            font=font.Font(size=20, weight="bold"),
            pady=10
        )
        self.display.pack()

    def _create_grid(self):
        grid_frame = tk.Frame(self)
        grid_frame.pack(expand=True, fill=tk.BOTH)
        for row in range(self._game.board_size):
            grid_frame.rowconfigure(row, weight=1)
            grid_frame.columnconfigure(row, weight=1)
            for col in range(self._game.board_size):
                button = tk.Button(
                    grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    highlightbackground="lightblue",
                    width=5,
                    height=2
                )
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def play(self, event):
        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        move = Move(row, col, self._game.current_player.label)

        if self._game.is_valid_move(move):
            self._game.process_move(move)
            self._update_button(clicked_btn)
            if self._check_end():
                return
            self._game.toggle_player()
            self._update_display(f"{self._game.current_player.label}'s turn")

            if not self._game.current_player.is_human:
                self.after(500, self._ai_move)

    def _ai_move(self):
        move = self._game.best_move()
        if move:
            btn = self._get_button_by_position(move.row, move.col)
            self._game.process_move(move)
            self._update_button(btn)
            if self._check_end():
                return
            self._game.toggle_player()
            self._update_display(f"{self._game.current_player.label}'s turn")

    def _get_button_by_position(self, row, col):
        for btn, position in self._cells.items():
            if position == (row, col):
                return btn

    def _update_button(self, btn):
        btn.config(text=self._game.current_player.label, fg=self._game.current_player.color)

    def _update_display(self, msg, color="black"):
        self.display.config(text=msg, fg=color)

    def _highlight_cells(self):
        for btn, pos in self._cells.items():
            if pos in self._game.winner_combo:
                btn.config(highlightbackground="red")

    def _check_end(self):
        if self._game.has_winner():
            self._highlight_cells()
            self._update_display(f"{self._game.current_player.label} wins!", self._game.current_player.color)
            return True
        elif self._game.is_tied():
            self._update_display("It's a tie!", "orange")
            return True
        return False

    def reset_board(self):
        self._game.reset_game()
        for btn in self._cells:
            btn.config(text="", fg="black", highlightbackground="lightblue")
        self._update_display(f"{self._game.current_player.label}'s turn")

# --- Main ---
def main():
    game = TicTacToeGame()
    board = TicTacToeBoard(game)
    board.mainloop()

if __name__ == "__main__":
    main()

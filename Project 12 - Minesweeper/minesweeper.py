import random
from colorama import Fore, Style, init

init(autoreset=True)

class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs
        self.board = self.make_new_board()
        self.dug = set()

    def make_new_board(self):
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size ** 2 - 1)
            row, col = loc // self.dim_size, loc % self.dim_size
            if board[row][col] == '*':
                continue
            board[row][col] = '*'
            bombs_planted += 1

        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if board[r][c] == '*':
                    continue
                num_bombs = 0
                for i in range(max(0, r - 1), min(r + 2, self.dim_size)):
                    for j in range(max(0, c - 1), min(c + 2, self.dim_size)):
                        if board[i][j] == '*':
                            num_bombs += 1
                board[r][c] = num_bombs
        return board

    def print_board(self, reveal=False):
        print("\n" + "-" * (self.dim_size * 2 + 1))
        for r in range(self.dim_size):
            row = ''
            for c in range(self.dim_size):
                if (r, c) in self.dug or reveal:
                    row += self.colored(self.board[r][c]) + " "
                else:
                    row += Fore.CYAN + "*" + Style.RESET_ALL + " "
            print(row)
        print("-" * (self.dim_size * 2 + 1))

    def colored(self, cell):
        if cell == '*':
            return Fore.RED + '💣' + Style.RESET_ALL
        elif cell == 0:
            return Fore.WHITE + ' ' + Style.RESET_ALL
        elif cell == 1:
            return Fore.BLUE + '1' + Style.RESET_ALL
        elif cell == 2:
            return Fore.GREEN + '2' + Style.RESET_ALL
        elif cell == 3:
            return Fore.YELLOW + '3' + Style.RESET_ALL
        elif cell == 4:
            return Fore.MAGENTA + '4' + Style.RESET_ALL
        else:
            return Fore.LIGHTRED_EX + str(cell) + Style.RESET_ALL

    def dig(self, row, col):
        if self.board[row][col] == '*':
            self.dug.add((row, col))
            return False
        self.dug.add((row, col))
        return True

def play(dim_size=5, num_bombs=5):
    print(Fore.LIGHTGREEN_EX + "\n💣 Welcome to Minesweeper! 💣" + Style.RESET_ALL)
    board = Board(dim_size, num_bombs)
    while len(board.dug) < dim_size ** 2 - num_bombs:
        board.print_board()
        user_input = input(Fore.LIGHTYELLOW_EX + "Where would you like to dig? (format: row,col): " + Style.RESET_ALL)

        try:
            row, col = map(int, user_input.split(','))
            if row < 0 or row >= dim_size or col < 0 or col >= dim_size:
                print(Fore.YELLOW + "⚠️ Invalid location. Try again." + Style.RESET_ALL)
                continue
        except ValueError:
            print(Fore.YELLOW + "⚠️ Invalid input. Please enter in format 'row,col'." + Style.RESET_ALL)
            continue

        if not board.dig(row, col):
            print(Fore.RED + "\n💥 Boom! You hit a bomb! Game over! 💥" + Style.RESET_ALL)
            board.print_board(reveal=True)
            return

    print(Fore.LIGHTGREEN_EX + "\n🎉 Congratulations, you cleared the board! You win! 🎉" + Style.RESET_ALL)
    board.print_board(reveal=True)

# Start the game
play(dim_size=5, num_bombs=5)


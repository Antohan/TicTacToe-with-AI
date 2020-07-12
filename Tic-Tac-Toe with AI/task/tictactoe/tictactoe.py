import random


class TicTacToe:
    def __init__(self, first_player, second_player):
        self.first_player = self.user if first_player == "user" else self.computer
        self.second_player = self.user if second_player == "user" else self.computer
        self.board = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "],
        ]
        self.current_player = "X"

    def computer(self):
        """Bot moves"""

        while True:
            row, col = random.randint(1, 3), random.randint(1, 3)

            if self.board[row - 1][col - 1] == " ":
                self.board[row - 1][col - 1] = self.current_player
                print("Making move level \"easy\"")
                break

    def user(self):
        """Player moves"""

        while True:
            coords = input("Enter the coordinates:").split()

            if len(coords) < 2 or not all(c.isdigit() for c in coords):
                print("You should enter numbers!")
                continue

            col, row = int(coords[0]), int(coords[1])

            if col > 3 or row > 3:
                print("Coordinates should be from 1 to 3!")
                continue

            if self.board[row - 1][col - 1] != " ":
                print("This cell is occupied! Choose another one!")
                continue

            self.board[row - 1][col - 1] = self.current_player
            break

    def flat_board(self):
        """Return flat game field"""

        return [cell for row in self.board for cell in row]

    def print_board(self):
        """Print board state"""

        print("---------")
        for row in range(len(self.board)):
            print("|", *self.board[::-1][row], "|")
        print("---------")

    def check_win(self, player: str):
        """Check winn"""

        winning_combos = [
            [self.board[0][0], self.board[0][1], self.board[0][2]],
            [self.board[1][0], self.board[1][1], self.board[1][2]],
            [self.board[2][0], self.board[2][1], self.board[2][2]],
            [self.board[0][0], self.board[1][0], self.board[2][0]],
            [self.board[0][1], self.board[1][1], self.board[2][1]],
            [self.board[0][2], self.board[1][2], self.board[2][2]],
            [self.board[0][0], self.board[1][1], self.board[2][2]],
            [self.board[2][0], self.board[1][1], self.board[0][2]],
        ]

        # Check that at least one combo contains the same symbols (X or O)
        return any(all(player == c for c in combo) for combo in [_ for _ in winning_combos])

    def game_over(self):
        """Return string with game result"""

        if self.check_win("O"):
            return "O wins"
        elif self.check_win("X"):
            return "X wins"
        elif " " in self.flat_board():
            return "Continue"
        else:
            return "Draw"

    def start(self):
        """Start game"""

        while True:
            self.print_board()

            if self.current_player == "X":
                self.first_player()
            else:
                self.second_player()

            self.current_player = "O" if self.current_player == "X" else "X"
            result = self.game_over()

            if result == "Continue":
                continue
            else:
                self.print_board()
                print(result)
                break


while True:
    command = input("Input command:").split()

    if command[0] == "exit":
        break
    elif len(command) < 3 and command[0] != "start":
        print("Bad parameters!")
        continue

    game = TicTacToe(command[1], command[2])
    game.start()

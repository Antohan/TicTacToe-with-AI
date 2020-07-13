import abc
import random


class Player(abc.ABC):
    def __init__(self, sign: str):
        self.sign = sign

    def check_win(self, board):
        winning_combos = [
            [board[0][0], board[0][1], board[0][2]],
            [board[1][0], board[1][1], board[1][2]],
            [board[2][0], board[2][1], board[2][2]],
            [board[0][0], board[1][0], board[2][0]],
            [board[0][1], board[1][1], board[2][1]],
            [board[0][2], board[1][2], board[2][2]],
            [board[0][0], board[1][1], board[2][2]],
            [board[2][0], board[1][1], board[0][2]],
        ]

        return any(
            all(self.sign == c for c in combo) for combo in [_ for _ in winning_combos]
        )

    @abc.abstractmethod
    def make_move(self, board):
        pass


class User(Player):
    def make_move(self, board):
        while True:
            coords = input("Enter the coordinates:").split()

            if len(coords) < 2 or not all(c.isdigit() for c in coords):
                print("You should enter numbers!")
                continue

            col, row = int(coords[0]), int(coords[1])

            if col > 3 or row > 3:
                print("Coordinates should be from 1 to 3!")
                continue

            if board[row - 1][col - 1] != " ":
                print("This cell is occupied! Choose another one!")
                continue

            board[row - 1][col - 1] = self.sign
            break
        return board


class Bot(Player):
    def __init__(self, sign, level):
        super().__init__(sign)
        self.level = level

    def __str__(self):
        return self.level

    def make_move(self, board):
        while True:
            row, col = random.randint(1, 3), random.randint(1, 3)

            if board[row - 1][col - 1] == " ":
                board[row - 1][col - 1] = self.sign
                print(f"Making move level \"{self}\"")
                break
        return board


class TicTacToe:
    def __init__(self, x_player, o_player):
        if x_player == "user":
            self.x_player = User("X")
        else:
            self.x_player = Bot("X", x_player)

        if o_player == "user":
            self.o_player = User("O")
        else:
            self.o_player = Bot("O", o_player)

        self.board = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "],
        ]
        self.current_player = "X"

    def __str__(self):
        result = "---------\n"
        result += "\n".join([f"| {' '.join(row)} |" for row in self.board[::-1]])
        result += "\n---------"

        return result

    def flat_board(self):
        """Return flat game field"""
        return [cell for row in self.board for cell in row]

    def game_over(self):
        """Return string with game result"""
        if self.o_player.check_win(self.board):
            return "O wins"
        elif self.x_player.check_win(self.board):
            return "X wins"
        elif " " in self.flat_board():
            return "Continue"
        else:
            return "Draw"

    def start(self):
        """Start game"""
        while True:
            print(self)

            if self.current_player == "X":
                self.x_player.make_move(self.board)
            else:
                self.o_player.make_move(self.board)

            self.current_player = "O" if self.current_player == "X" else "X"
            result = self.game_over()

            if result == "Continue":
                continue
            else:
                print(self)
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

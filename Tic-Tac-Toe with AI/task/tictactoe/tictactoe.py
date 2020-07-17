import abc
import random
import sys


EMPTY_CELL = " "


class Player(abc.ABC):
    def __init__(self, sign: str):
        self.sign = sign
        self.opponent_sign = 'X' if self.sign == "O" else "X"

    @staticmethod
    def get_winning_combos(board):
        return [
            {(0, 0): board[0][0], (0, 1): board[0][1], (0, 2): board[0][2]},
            {(1, 0): board[1][0], (1, 1): board[1][1], (1, 2): board[1][2]},
            {(2, 0): board[2][0], (2, 1): board[2][1], (2, 2): board[2][2]},
            {(0, 0): board[0][0], (1, 0): board[1][0], (2, 0): board[2][0]},
            {(0, 1): board[0][1], (1, 1): board[1][1], (2, 1): board[2][1]},
            {(0, 2): board[0][2], (1, 2): board[1][2], (2, 2): board[2][2]},
            {(0, 0): board[0][0], (1, 1): board[1][1], (2, 2): board[2][2]},
            {(2, 0): board[2][0], (1, 1): board[1][1], (0, 2): board[0][2]},
        ]

    def check_win(self, board, sign: str):
        winning_combos = self.get_winning_combos(board)
        combo_values = [list(c.values()) for c in [combo for combo in winning_combos]]

        return any(
            all(sign == c for c in combo) for combo in [_ for _ in combo_values]
        )

    @staticmethod
    def check_draw(board):
        count = 0
        for y in range(3):
            count += 1 if EMPTY_CELL in board[y] else 0
        return count == 0

    @abc.abstractmethod
    def make_move(self, board):
        """Make move"""
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

            if board[row - 1][col - 1] != EMPTY_CELL:
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

    def random_move(self, board):
        """Get random coordinates."""
        while True:
            row, col = random.randint(0, 2), random.randint(0, 2)

            if board[row][col] == EMPTY_CELL:
                board[row][col] = self.sign
                print(f"Making move level \"{self}\"")
                break
        return board

    def minimax(self, board, depth, is_self_turn):
        if self.check_win(board, self.sign):
            return 100
        if self.check_win(board, self.opponent_sign):
            return -100
        if self.check_draw(board):
            0

        if is_self_turn:
            best_score = -sys.maxsize
            for row in range(3):
                for col in range(3):
                    if board[row][col] == EMPTY_CELL:
                        board[row][col] = self.sign
                        score = self.minimax(board, depth + 1, False)
                        best_score = max(best_score, score)
        else:
            best_score = sys.maxsize
            for row in range(3):
                for col in range(3):
                    if board[row][col] == EMPTY_CELL:
                        board[row][col] = self.opponent_sign
                        score = self.minimax(board, depth + 1, True)
                        best_score = max(best_score, score)

        return best_score

    def make_move(self, board):
        if self.level == "easy":
            return self.random_move(board)

        if self.level == "medium":
            winning_combos = self.get_winning_combos(board)

            # Check that it can win in one move
            for i in range(len(winning_combos)):
                if len([sign for sign in list(winning_combos[i].values()) if sign == self.sign]) == 2:
                    for key, value in winning_combos[i].items():
                        if value == EMPTY_CELL:
                            board[key[0]][key[1]] = self.sign
                            print(f"Making move level \"{self}\"")
                            return board
            # Block the opponent to win
            for i in range(len(winning_combos)):
                if len([sign for sign in list(winning_combos[i].values()) if sign == self.opponent_sign]) == 2:
                    for key, value in winning_combos[i].items():
                        if value == EMPTY_CELL:
                            board[key[0]][key[1]] = self.sign
                            print(f"Making move level \"{self}\"")
                            return board

            return self.random_move(board)

        if self.level == "hard":
            # Use minimax algorithm
            best_score = -sys.maxsize
            copy_board = [board[i].copy() for i in range(3)]

            for row in range(3):
                for col in range(3):
                    if copy_board[row][col] == EMPTY_CELL:
                        copy_board[row][col] = self.sign
                        score = self.minimax(copy_board, 0, False)
                        copy_board[row][col] = EMPTY_CELL
                        if score > best_score:
                            best_score = score
                            board[row][col] = self.sign
            print("Making move level \"hard\"")
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

        # Empty board 3x3
        self.board = [
            [EMPTY_CELL for _ in range(3)] for _ in range(3)
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
        if self.o_player.check_win(self.board, "O"):
            return "O wins"
        elif self.x_player.check_win(self.board, "X"):
            return "X wins"
        elif EMPTY_CELL in self.flat_board():
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

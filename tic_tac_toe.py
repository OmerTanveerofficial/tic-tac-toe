import os
import random
import time
import math


# ─────────────────────── COLORS ───────────────────────

class Color:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    BG_RED  = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_BLUE = "\033[44m"


WIN_COMBOS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6],
]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def check_winner(board, player):
    for combo in WIN_COMBOS:
        if all(board[i] == player for i in combo):
            return combo
    return None


def is_draw(board):
    return all(cell in ("X", "O") for cell in board)


def get_available(board):
    return [i for i in range(9) if board[i] not in ("X", "O")]


def print_board(board):
    print()
    for i in range(3):
        row = " | ".join(board[i * 3:(i + 1) * 3])
        print(f"  {row}")
        if i < 2:
            print("  ---------")
    print()


def get_player_move(board):
    while True:
        try:
            move = int(input("Your move (1-9): ")) - 1
            if 0 <= move <= 8 and board[move] not in ("X", "O"):
                return move
            print("Invalid move. Try again.")
        except ValueError:
            print("Enter a number 1-9.")


def get_computer_move(board, computer, _player):
    for i in get_available(board):
        board[i] = computer
        if check_winner(board, computer):
            board[i] = str(i + 1)
            return i
        board[i] = str(i + 1)
    return random.choice(get_available(board))


def play():
    board = [str(i + 1) for i in range(9)]
    player, computer = "X", "O"
    current = "X"
    print("Tic Tac Toe — You are X, Computer is O")
    print_board(board)

    while True:
        if current == player:
            move = get_player_move(board)
            board[move] = player
        else:
            move = get_computer_move(board, computer, player)
            board[move] = computer
            print(f"Computer plays position {move + 1}")

        print_board(board)

        winner = current if current == player else computer
        if check_winner(board, winner):
            if winner == player:
                print("You win!")
            else:
                print("Computer wins!")
            break
        if is_draw(board):
            print("It's a draw!")
            break
        current = "O" if current == "X" else "X"


if __name__ == "__main__":
    play()

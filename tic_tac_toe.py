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


BANNER = f"""
{Color.CYAN}{Color.BOLD}
  ╔════════════════════════════════════════╗
  ║                                        ║
  ║     ╔╦╗╦╔═╗  ╔╦╗╔═╗╔═╗  ╔╦╗╔═╗╔═╗   ║
  ║      ║ ║║     ║ ╠═╣║     ║ ║ ║║╣    ║
  ║      ╩ ╩╚═╝   ╩ ╩ ╩╚═╝   ╩ ╚═╝╚═╝   ║
  ║                                        ║
  ╚════════════════════════════════════════╝
{Color.RESET}"""

WIN_COMBOS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6],
]


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def colorize_cell(cell, winning_cells=None, index=None):
    if cell == "X":
        if winning_cells and index in winning_cells:
            return f"{Color.BG_GREEN}{Color.BOLD} X {Color.RESET}"
        return f"{Color.GREEN}{Color.BOLD} X {Color.RESET}"
    elif cell == "O":
        if winning_cells and index in winning_cells:
            return f"{Color.BG_RED}{Color.BOLD} O {Color.RESET}"
        return f"{Color.RED}{Color.BOLD} O {Color.RESET}"
    else:
        return f"{Color.DIM} {cell} {Color.RESET}"


def print_board(board, winning_cells=None):
    print()
    print(f"  {Color.CYAN}┌───┬───┬───┐{Color.RESET}")
    for i in range(3):
        cells = [colorize_cell(board[i * 3 + j], winning_cells, i * 3 + j) for j in range(3)]
        print(f"  {Color.CYAN}│{Color.RESET}{cells[0]}{Color.CYAN}│{Color.RESET}{cells[1]}{Color.CYAN}│{Color.RESET}{cells[2]}{Color.CYAN}│{Color.RESET}")
        if i < 2:
            print(f"  {Color.CYAN}├───┼───┼───┤{Color.RESET}")
    print(f"  {Color.CYAN}└───┴───┴───┘{Color.RESET}")
    print()


def animated_text(text, delay=0.03):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def thinking_animation():
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    duration = random.uniform(0.4, 0.8)
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(f"\r  {Color.YELLOW}{frames[i % len(frames)]} Computer is thinking...{Color.RESET}", end="", flush=True)
        time.sleep(0.08)
        i += 1
    print(f"\r{' ' * 40}\r", end="")


def check_winner(board, player):
    for combo in WIN_COMBOS:
        if all(board[i] == player for i in combo):
            return combo
    return None


def is_draw(board):
    return all(cell in ("X", "O") for cell in board)


def get_available(board):
    return [i for i in range(9) if board[i] not in ("X", "O")]


def get_player_move(board):
    while True:
        try:
            move = input(f"  {Color.CYAN}➤ {Color.WHITE}Your move (1-9): {Color.RESET}")
            move = int(move) - 1
            if 0 <= move <= 8 and board[move] not in ("X", "O"):
                return move
            print(f"  {Color.RED}✗ Invalid move. Choose an empty cell (1-9).{Color.RESET}")
        except (ValueError, EOFError):
            print(f"  {Color.RED}✗ Please enter a number from 1 to 9.{Color.RESET}")


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

    clear_screen()
    print(BANNER)
    print(f"  {Color.BOLD}You: {Color.GREEN}X{Color.RESET}  │  {Color.BOLD}Computer: {Color.RED}O{Color.RESET}")

    while True:
        if current == player:
            print_board(board)
            move = get_player_move(board)
            board[move] = player
        else:
            thinking_animation()
            move = get_computer_move(board, computer, player)
            board[move] = computer
            print(f"  {Color.YELLOW}● Computer placed O at position {move + 1}{Color.RESET}")

        winner = current if current == player else computer
        win_combo = check_winner(board, winner)
        if win_combo:
            clear_screen()
            print(BANNER)
            print_board(board, winning_cells=win_combo)
            if winner == player:
                animated_text(f"  {Color.GREEN}{Color.BOLD}🎉 Congratulations! You win!{Color.RESET}", 0.04)
            else:
                animated_text(f"  {Color.RED}{Color.BOLD}💀 Computer wins! Better luck next time.{Color.RESET}", 0.04)
            break
        if is_draw(board):
            clear_screen()
            print(BANNER)
            print_board(board)
            animated_text(f"  {Color.YELLOW}{Color.BOLD}🤝 It's a draw!{Color.RESET}", 0.04)
            break

        if current == player:
            clear_screen()
            print(BANNER)
            print(f"  {Color.BOLD}You: {Color.GREEN}X{Color.RESET}  │  {Color.BOLD}Computer: {Color.RED}O{Color.RESET}")

        current = "O" if current == "X" else "X"


if __name__ == "__main__":
    clear_screen()
    print(BANNER)
    animated_text(f"  {Color.WHITE}{Color.BOLD}Welcome to Tic Tac Toe!{Color.RESET}", 0.04)

    while True:
        play()
        print()
        try:
            again = input(f"  {Color.CYAN}➤ {Color.WHITE}Play again? (y/n): {Color.RESET}").lower()
        except EOFError:
            again = "n"
        if again != "y":
            print()
            animated_text(f"  {Color.CYAN}{Color.BOLD}Thanks for playing! See you next time! 👋{Color.RESET}", 0.03)
            print()
            break

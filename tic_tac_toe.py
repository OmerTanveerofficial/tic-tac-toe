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


# ─────────────────────── DISPLAY ──────────────────────

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


def print_scoreboard(scores):
    p = scores["player"]
    c = scores["computer"]
    d = scores["draws"]
    print(f"  {Color.BOLD}{'─' * 36}{Color.RESET}")
    print(f"  {Color.GREEN}  Player: {p}{Color.RESET}  │  {Color.RED}Computer: {c}{Color.RESET}  │  {Color.YELLOW}Draws: {d}{Color.RESET}")
    print(f"  {Color.BOLD}{'─' * 36}{Color.RESET}")


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


# ─────────────────────── GAME LOGIC ──────────────────

def check_winner(board, player):
    for combo in WIN_COMBOS:
        if all(board[i] == player for i in combo):
            return combo
    return None


def is_draw(board):
    return all(cell in ("X", "O") for cell in board)


def get_available(board):
    return [i for i in range(9) if board[i] not in ("X", "O")]


# ─────────────────────── AI (MINIMAX) ────────────────

def minimax(board, depth, is_maximizing, computer, player, alpha, beta):
    if check_winner(board, computer):
        return 10 - depth
    if check_winner(board, player):
        return depth - 10
    if is_draw(board):
        return 0

    if is_maximizing:
        best = -math.inf
        for i in get_available(board):
            board[i] = computer
            score = minimax(board, depth + 1, False, computer, player, alpha, beta)
            board[i] = str(i + 1)
            best = max(best, score)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return best
    else:
        best = math.inf
        for i in get_available(board):
            board[i] = player
            score = minimax(board, depth + 1, True, computer, player, alpha, beta)
            board[i] = str(i + 1)
            best = min(best, score)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best


def get_computer_move_hard(board, computer, player):
    best_score = -math.inf
    best_move = None
    for i in get_available(board):
        board[i] = computer
        score = minimax(board, 0, False, computer, player, -math.inf, math.inf)
        board[i] = str(i + 1)
        if score > best_score:
            best_score = score
            best_move = i
    return best_move


def get_computer_move_medium(board, computer, player):
    # 60% chance of playing optimally, 40% random
    if random.random() < 0.6:
        return get_computer_move_hard(board, computer, player)
    return random.choice(get_available(board))


def get_computer_move_easy(board, computer, _player):
    # Win if possible, otherwise random
    for i in get_available(board):
        board[i] = computer
        if check_winner(board, computer):
            board[i] = str(i + 1)
            return i
        board[i] = str(i + 1)
    return random.choice(get_available(board))


# ─────────────────────── INPUT ───────────────────────

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


def choose_difficulty():
    print(f"\n  {Color.BOLD}{Color.WHITE}Select Difficulty:{Color.RESET}")
    print(f"  {Color.GREEN}[1]{Color.RESET} Easy   {Color.DIM}— Computer makes random moves{Color.RESET}")
    print(f"  {Color.YELLOW}[2]{Color.RESET} Medium {Color.DIM}— Computer plays smart sometimes{Color.RESET}")
    print(f"  {Color.RED}[3]{Color.RESET} Hard   {Color.DIM}— Unbeatable AI (Minimax){Color.RESET}")
    print()
    while True:
        try:
            choice = input(f"  {Color.CYAN}➤ {Color.WHITE}Choose (1-3): {Color.RESET}")
            if choice in ("1", "2", "3"):
                return int(choice)
            print(f"  {Color.RED}✗ Enter 1, 2, or 3.{Color.RESET}")
        except EOFError:
            return 2


def choose_marker():
    print(f"\n  {Color.BOLD}{Color.WHITE}Choose Your Marker:{Color.RESET}")
    print(f"  {Color.GREEN}[X]{Color.RESET} Play as X {Color.DIM}(goes first){Color.RESET}")
    print(f"  {Color.RED}[O]{Color.RESET} Play as O {Color.DIM}(goes second){Color.RESET}")
    print()
    while True:
        try:
            choice = input(f"  {Color.CYAN}➤ {Color.WHITE}Choose (X/O): {Color.RESET}").upper()
            if choice in ("X", "O"):
                return choice
            print(f"  {Color.RED}✗ Enter X or O.{Color.RESET}")
        except EOFError:
            return "X"


def choose_mode():
    print(f"\n  {Color.BOLD}{Color.WHITE}Game Mode:{Color.RESET}")
    print(f"  {Color.GREEN}[1]{Color.RESET} Player vs Computer")
    print(f"  {Color.MAGENTA}[2]{Color.RESET} Player vs Player")
    print()
    while True:
        try:
            choice = input(f"  {Color.CYAN}➤ {Color.WHITE}Choose (1/2): {Color.RESET}")
            if choice in ("1", "2"):
                return int(choice)
            print(f"  {Color.RED}✗ Enter 1 or 2.{Color.RESET}")
        except EOFError:
            return 1


# ─────────────────────── GAME LOOP ───────────────────

def play(scores):
    clear_screen()
    print(BANNER)
    print_scoreboard(scores)

    mode = choose_mode()
    player_marker = choose_marker()

    if mode == 1:
        difficulty = choose_difficulty()
        ai_move_fn = {1: get_computer_move_easy, 2: get_computer_move_medium, 3: get_computer_move_hard}[difficulty]
        diff_label = {1: f"{Color.GREEN}Easy", 2: f"{Color.YELLOW}Medium", 3: f"{Color.RED}Hard"}[difficulty]
    else:
        difficulty = None
        ai_move_fn = None
        diff_label = None

    if mode == 1:
        computer_marker = "O" if player_marker == "X" else "X"
    else:
        computer_marker = None

    board = [str(i + 1) for i in range(9)]
    current = "X"
    move_count = 0
    move_history = []

    clear_screen()
    print(BANNER)
    print_scoreboard(scores)

    if mode == 1:
        print(f"  {Color.BOLD}You: {Color.GREEN}{player_marker}{Color.RESET}  │  "
              f"{Color.BOLD}Computer: {Color.RED}{computer_marker}{Color.RESET}  │  "
              f"{Color.BOLD}Difficulty: {diff_label}{Color.RESET}")
    else:
        other = "O" if player_marker == "X" else "X"
        print(f"  {Color.BOLD}Player 1: {Color.GREEN}{player_marker}{Color.RESET}  │  "
              f"{Color.BOLD}Player 2: {Color.MAGENTA}{other}{Color.RESET}")

    while True:
        is_player_turn = (mode == 2) or (current == player_marker)

        if is_player_turn:
            print_board(board)
            if mode == 2:
                label = "Player 1" if current == player_marker else "Player 2"
                print(f"  {Color.BOLD}{label}'s turn ({current}){Color.RESET}")
            move = get_player_move(board)
            board[move] = current
        else:
            thinking_animation()
            move = ai_move_fn(board, computer_marker, player_marker)
            board[move] = computer_marker
            print(f"  {Color.YELLOW}● Computer placed {computer_marker} at position {move + 1}{Color.RESET}")

        move_count += 1
        move_history.append((current if is_player_turn else computer_marker, move + 1))

        win_combo = check_winner(board, current if is_player_turn else computer_marker)
        if win_combo:
            clear_screen()
            print(BANNER)
            print_board(board, winning_cells=win_combo)

            if mode == 2:
                label = "Player 1" if current == player_marker else "Player 2"
                animated_text(f"  🎉 {label} ({current}) wins!", 0.04)
                scores["player"] += 1
            elif is_player_turn:
                print("\a")  # terminal bell
                animated_text(f"  {Color.GREEN}{Color.BOLD}🎉 Congratulations! You win!{Color.RESET}", 0.04)
                scores["player"] += 1
            else:
                print("\a")  # terminal bell
                animated_text(f"  {Color.RED}{Color.BOLD}💀 Computer wins! Better luck next time.{Color.RESET}", 0.04)
                scores["computer"] += 1
            break

        if is_draw(board):
            clear_screen()
            print(BANNER)
            print_board(board)
            animated_text(f"  {Color.YELLOW}{Color.BOLD}🤝 It's a draw!{Color.RESET}", 0.04)
            scores["draws"] += 1
            break

        if mode == 1 and is_player_turn:
            clear_screen()
            print(BANNER)
            print_scoreboard(scores)
            if mode == 1:
                print(f"  {Color.BOLD}You: {Color.GREEN}{player_marker}{Color.RESET}  │  "
                      f"{Color.BOLD}Computer: {Color.RED}{computer_marker}{Color.RESET}  │  "
                      f"{Color.BOLD}Difficulty: {diff_label}{Color.RESET}")

        current = "O" if current == "X" else "X"

    print_scoreboard(scores)


def main():
    scores = {"player": 0, "computer": 0, "draws": 0}
    clear_screen()
    print(BANNER)
    animated_text(f"  {Color.WHITE}{Color.BOLD}Welcome to Tic Tac Toe!{Color.RESET}", 0.04)

    while True:
        play(scores)
        print()
        try:
            again = input(f"  {Color.CYAN}➤ {Color.WHITE}Play again? (y/n): {Color.RESET}").lower()
        except EOFError:
            again = "n"
        if again != "y":
            print()
total = scores["player"] + scores["computer"] + scores["draws"]
            if total > 0:
                print(f"\n  {Color.BOLD}{Color.WHITE}Final Stats:{Color.RESET}")
                print(f"  {Color.GREEN}Wins: {scores["player"]}{Color.RESET} | {Color.RED}Losses: {scores["computer"]}{Color.RESET} | {Color.YELLOW}Draws: {scores["draws"]}{Color.RESET}")
                win_rate = (scores["player"] / total) * 100
                print(f"  {Color.CYAN}Win Rate: {win_rate:.0f}%{Color.RESET}\n")
            animated_text(f"  {Color.CYAN}{Color.BOLD}Thanks for playing! See you next time! 👋{Color.RESET}", 0.03)
            print()
            break


if __name__ == "__main__":
    main()

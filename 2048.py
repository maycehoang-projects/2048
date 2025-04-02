import random
import os

def add_num(board):
    """Inserts 2 or 4 into a random empty space, favoring 2."""
    empty_spaces = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if not empty_spaces:
        return None
    
    i, j = random.choice(empty_spaces)
    board[i][j] = 2 if random.random() < 0.9 else 4  # 90% chance of 2, 10% of 4

def shift_and_combine(line):
    """Shifts numbers right and combines identical numbers."""
    new_line = [num for num in line if num != 0]  # Remove zeros
    for i in range(len(new_line) - 1, 0, -1):
        if new_line[i] == new_line[i - 1]:  # Combine identical tiles
            new_line[i] *= 2
            new_line[i - 1] = 0
    new_line = [num for num in new_line if num != 0]  # Remove zeros again
    return [0] * (4 - len(new_line)) + new_line  # Pad with zeros

def move(board, direction):
    """Moves tiles in the given direction: 'left', 'right', 'up', 'down'."""
    if direction in ("right", "left"):
        for i in range(4):
            board[i] = shift_and_combine(board[i][::-1] if direction == "left" else board[i])[::-1] if direction == "left" else shift_and_combine(board[i])
    else:
        rotated = [list(row) for row in zip(*board)]  # Transpose board
        for i in range(4):
            rotated[i] = shift_and_combine(rotated[i][::-1] if direction == "up" else rotated[i])[::-1] if direction == "up" else shift_and_combine(rotated[i])
        for i in range(4):
            for j in range(4):
                board[j][i] = rotated[i][j]  # Transpose back

def board_not_full(board):
    """Checks if there are possible moves left."""
    return any(0 in row for row in board) or any(board[i][j] == board[i][j + 1] for i in range(4) for j in range(3)) or any(board[i][j] == board[i + 1][j] for i in range(3) for j in range(4))

def display_board(board):
    """Displays board in a formatted grid."""
    os.system("cls" if os.name == "nt" else "clear")  # Clear screen for better display
    for row in board:
        print("+----" * 4 + "+")
        print("|" + "|".join(f"{num:^4}" if num else "    " for num in row) + "|")
    print("+----" * 4 + "+")

def display_title():
    """Displays game title in ASCII art."""
    print("2048 - Python Edition")

def play():
    """Runs the game loop."""
    board = [[0] * 4 for _ in range(4)]
    add_num(board)
    add_num(board)

    while board_not_full(board):
        display_board(board)
        move_input = input("Move (WASD): ").strip().lower()
        if move_input in ["w", "a", "s", "d"]:
            prev_board = [row[:] for row in board]  # Copy board before move
            move(board, {"w": "up", "a": "left", "s": "down", "d": "right"}[move_input])
            if prev_board != board:
                add_num(board)  # Add a new number only if the board changed
        elif move_input == "q":
            print("Game Quit!")
            break
    else:
        display_board(board)
        print("Game Over!")

if __name__ == "__main__":
    display_title()
    play()

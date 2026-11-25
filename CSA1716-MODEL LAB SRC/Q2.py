import math

def check_winner(board):
    win_lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)              # Diagonals
    ]
    for a, b, c in win_lines:
        if board[a] == board[b] == board[c] != " ":
            return board[a]
    if " " not in board:
        return "Draw"
    return None

def print_board(board):
    for i in range(0, 9, 3):
        print(f" {board[i]} | {board[i+1]} | {board[i+2]} ")
        if i < 6:
            print("---+---+---")

terminal_nodes = []

def minimax(board, is_maximizing, path):
    winner = check_winner(board)
    if winner is not None:
        utility = 1 if winner == "O" else (-1 if winner == "X" else 0)
        terminal_nodes.append((path, winner, utility))
        return utility

    if is_maximizing:  # O is MAX
        best_val = -math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                val = minimax(board, False, path + [f"O->({i//3},{i%3})"])
                board[i] = " "
                best_val = max(best_val, val)
        return best_val
    else:              # X is MIN
        best_val = math.inf
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                val = minimax(board, True, path + [f"X->({i//3},{i%3})"])
                board[i] = " "
                best_val = min(best_val, val)
        return best_val

def find_best_move(board):
    best_val = -math.inf
    best_move = -1
    move_values = {}

    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            val = minimax(board, False, [f"O->({i//3},{i%3})"])
            board[i] = " "
            move_values[(i // 3, i % 3)] = val
            if val > best_val:
                best_val = val
                best_move = i

    return best_move, best_val, move_values

# Given Tic-Tac-Toe board (O is MAX and makes the next move)
board = [
    "X", "O", " ",
    " ", "O", "X",
    "X", " ", "O"
]

print("Initial Board (O = MAX, next move):")
print_board(board)

best_move, best_val, move_values = find_best_move(board)

print("\nTerminal Nodes and Utility Values:")
for path, outcome, util in terminal_nodes:
    print(f"  Path: {' -> '.join(path)} | Outcome: {outcome:4s} | Utility: {util:+d}")

print("\nMinimax Value for Each Possible Move by O:")
for pos, val in move_values.items():
    print(f"  Move {pos}: Utility = {val:+d}")

print(f"\nSelected Best Move for O: Row {best_move // 3}, Col {best_move % 3} (Index {best_move}) with Utility = {best_val:+d}")

board[best_move] = "O"
print("\nBoard After O's Move:")
print_board(board)

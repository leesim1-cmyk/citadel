import math

# Constants for the game pieces
X = "X"
O = "O"
EMPTY = " "

def print_board(board):
    """Renders the 3x3 board cleanly to the console."""
    print(f"\n {board[0]} | {board[1]} | {board[2]} ")
    print("-----------")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("-----------")
    print(f" {board[6]} | {board[7]} | {board[8]} \n")

def check_winner(board):
    """Checks the board for a winner. Returns 'X', 'O', or None."""
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # Columns
        [0, 4, 8], [2, 4, 6]             # Diagonals
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] != EMPTY:
            return board[condition[0]]
    return None

def is_board_full(board):
    """Returns True if no empty spaces remain, otherwise False."""
    return EMPTY not in board

def minimax(board, depth, is_maximizing):
    """
    Core Minimax algorithm. 
    AI tries to maximize its score, while assuming the player minimizes it.
    """
    winner = check_winner(board)
    if winner == O:  # AI wins
        return 10 - depth
    if winner == X:  # Human wins
        return depth - 10
    if is_board_full(board):  # Draw
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = O
                score = minimax(board, depth + 1, False)
                board[i] = EMPTY
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == EMPTY:
                board[i] = X
                score = minimax(board, depth + 1, True)
                board[i] = EMPTY
                best_score = min(score, best_score)
        return best_score

def find_best_move(board):
    """Evaluates all available moves and returns the optimal index for the AI."""
    best_score = -math.inf
    best_move = -1
    for i in range(9):
        if board[i] == EMPTY:
            board[i] = O
            move_score = minimax(board, 0, False)
            board[i] = EMPTY
            if move_score > best_score:
                best_score = move_score
                best_move = i
    return best_move

def play_game():
    """Main game loop managing turns and terminal interaction."""
    board = [EMPTY] * 9
    print("Welcome to Tic-Tac-Toe vs Unbeatable AI!")
    print("Positions are numbered 1 through 9 like this:")
    print(" 1 | 2 | 3 \n-----------\n 4 | 5 | 6 \n-----------\n 7 | 8 | 9 ")
    
    # Human plays as 'X' (goes first), AI plays as 'O'
    while True:
        print_board(board)
        
        # Human Player Turn
        while True:
            try:
                move = int(input("Enter your move (1-9): ")) - 1
                if 0 <= move <= 8 and board[move] == EMPTY:
                    board[move] = X
                    break
                else:
                    print("Invalid move! The slot is taken or out of range.")
            except ValueError:
                print("Please enter a valid number between 1 and 9.")
        
        if check_winner(board) == X:
            print_board(board)
            print("Congratulations! You won! (This shouldn't happen!)")
            break
        if is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break
            
        # AI Player Turn
        print("AI is making its move...")
        ai_move = find_best_move(board)
        if ai_move != -1:
            board[ai_move] = O
            
        if check_winner(board) == O:
            print_board(board)
            print("The AI won! Better luck next time.")
            break
        if is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break

if __name__ == "__main__":
    play_game()

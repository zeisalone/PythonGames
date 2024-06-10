import numpy as np


ROW_COUNT = 6
COLUMN_COUNT = 7

def board_def():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def get_board(board):
    print(np.flip(board, 0))

def make_move(board, row, col, player):
    board[row][col] = player

def is_valid_move(board, col):
    if col < 0 or col >= COLUMN_COUNT:
        print(f"Invalid Column! Choose a value between 1 and {COLUMN_COUNT}.")
        return False

    if board[ROW_COUNT - 1][col] != 0:
        print("Row is full! Try Another One.")
        return False

    return True

def get_row(board, col):
    for row in range(ROW_COUNT):
        if board[row][col] == 0:
            return row

def win(board,piece):
    # Horizontal
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
               return True
    # Vertical 
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True
    # Diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True        
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT): 
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

board = board_def()
finish = False
playerturn = 1

def no_winner(board):
  for col in range(COLUMN_COUNT):
    if board[ROW_COUNT - 1][col] == 0:
      return False
  return True

get_board(board)

while not finish:
    
    if playerturn == 1:
        col = int(input("Make your move Player 1 (1-7): ")) - 1

        if is_valid_move(board, col):
            row = get_row(board, col)
            make_move(board,row,col,1)
            if win(board,1):
                print ("Player 1 Wins!")
                finish = True
            elif no_winner(board):
                print("It's a Tie!")
                finish = True
        else:
            continue

        playerturn += 1
        get_board(board)

        

    else:
        col = int(input("Make your move Player 2 (1-7): ")) - 1

        if is_valid_move(board, col):
            row = get_row(board, col)
            make_move(board,row,col,2)
            if win(board, 2):
                print("Player 2 Wins!")
                finish = True
            elif no_winner(board):
                print("It's a Tie!")
                finish = True    
        else:
            continue

        playerturn -= 1
        get_board(board)
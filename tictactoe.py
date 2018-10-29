import math

N = 3
board = [" "]*(N**2)
player1 = "p1" #X 
player2 = "p2" #O


def drawBoard(board, N):
    numItems = N**2
    print("_____________")
    for i in range(0, numItems, N):
        print("| " + board[i] + " | " + board[i+1] + " | " + board[i+2] + " |")
    print("_____________")

def rowcolToIndex(row, col, N):
    if ((row < 0) or (col < 0) or (row >= N) or (col >= N)):
        print("Invalid row,col!")
        return -1

    return row*N + col

# Return if the space on the board is empty
def validMove(board, index):
    return board[index] == " "

def makeMove(board, row, col, player, N):
    index = rowcolToIndex(row, col, N)

    if (player == "p1"):
        symbol = "X"
    else:
        symbol = "O"

    if (not validMove(board, index)):
        print("Invalid move!")
        return

    board[index] = symbol

# returns True if a player has won
def gameOver(board, player):
    if (player == "p1"):
        symbol = "XXX"
    else:
        symbol = "OOO"

    row1 = board[0] + board[1] + board[2] == symbol
    row2 = board[3] + board[4] + board[5] == symbol
    row3 = board[6] + board[7] + board[8] == symbol
    col1 = board[0] + board[1] + board[2] == symbol
    col2 = board[3] + board[4] + board[5] == symbol
    col3 = board[6] + board[7] + board[8] == symbol
    diag1 =board[0] + board[4] + board[8] == symbol
    diag2 = board[6] + board[4] + board[2] == symbol

    return row1 or row2 or row3 or col1 or col2 or col3 or diag1 or diag2




drawBoard(board, N)
makeMove(board, 0,0, player1, N)
drawBoard(board, N)
makeMove(board, 2,0, player2, N)
drawBoard(board, N)
makeMove(board, 2,2, player1, N)
drawBoard(board, N)
print(gameOver(board, player1))
makeMove(board, 0,2, player2, N)
drawBoard(board, N)
makeMove(board, 1,1, player1, N)
drawBoard(board, N)
#print(gameOver(board, player1))
#print(gameOver(board, player2))
makeMove(board, 1,1, player1, N)
drawBoard(board, N)
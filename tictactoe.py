import math

class TicTacToe:
    def __init__(self, N):
        self.N = N
        self.board = self.newBoard()
        self.player1 = "p1" #X 
        self.player2 = "p2" #O

    def newBoard(self):
        board = [" "]*(self.N**2)
        return board

    def drawBoard(self):
        N = self.N
        board = self.board

        numItems = N**2
        print("_____________")
        for i in range(0, numItems, N):
            print("| " + board[i] + " | " + board[i+1] + " | " + board[i+2] + " |")
        print("_____________")

    def rowcolToIndex(self,row, col):
        N = self.N

        if ((row < 0) or (col < 0) or (row >= N) or (col >= N)):
            print("Invalid row,col!")
            return -1

        return row*N + col

    # Return if the space on the board is empty
    def validMove(self, index):
        return self.board[index] == " "

    def makeMove(self, row, col, player):
        index = self.rowcolToIndex(row, col)

        if (player == "p1"):
            symbol = "X"
        else:
            symbol = "O"

        if (not self.validMove(index)):
            print("Invalid move!")
            return -1

        self.board[index] = symbol
        return 0

    def isGameOver(self, player):
        if (player == "p1"):
            symbol = "XXX"
        else:
            symbol = "OOO"

        board = self.board

        row1 = board[0] + board[1] + board[2] == symbol
        row2 = board[3] + board[4] + board[5] == symbol
        row3 = board[6] + board[7] + board[8] == symbol
        col1 = board[0] + board[1] + board[2] == symbol
        col2 = board[3] + board[4] + board[5] == symbol
        col3 = board[6] + board[7] + board[8] == symbol
        diag1 =board[0] + board[4] + board[8] == symbol
        diag2 = board[6] + board[4] + board[2] == symbol

        gameOver = row1 or row2 or row3 or col1 or col2 or col3 or diag1 or diag2

        if (gameOver):
            #print("Player %s wins!" % player)
            return True

        return False

    def gameOver(self):
        if (self.isGameOver(self.player1)):
            print("Player %s wins!" % self.player1)
            return True
        elif (self.isGameOver(self.player2)):
            print("Player %s wins!" % self.player2)
            return True
        else:
            return False

    def getBoard(self):
        return self.board




def testGame():
    N = 3
    TTT = TicTacToe(N)
    TTT.drawBoard()
    TTT.makeMove(0,0, TTT.player1)
    TTT.drawBoard()
    TTT.makeMove(2,0, TTT.player2)
    TTT.drawBoard()
    TTT.makeMove(2,2, TTT.player1)
    TTT.drawBoard()
    print(TTT.gameOver())
    TTT.makeMove(0,2, TTT.player2)
    TTT.drawBoard()
    TTT.makeMove(1,1, TTT.player1)
    TTT.drawBoard()
    print(TTT.gameOver())
    TTT.makeMove(1,1, TTT.player1)
    TTT.drawBoard()

#testGame()
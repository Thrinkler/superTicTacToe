
"""
[[1, 2, 3], 
 [4, 5, 6], 
 [7, 8, 9]]
 """

from typing import Literal


class Game:
    def __init__(self) -> None:
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.check_board = [[0 for _ in range(3)] for _ in range(3)]
        self.subboard = 0
        self.player = -1



    def play(self):
        if self.subboard == 0:
            self.choose_board()
        isValid = False
        while not isValid:
            row = int(input("choose row: "))
            column = int(input("choose column: "))
            isValid = self.choose_position(row, column, self.player)
            if not isValid: print("Position not allowed")

        self.player = -self.player

    def choose_position(self, row : int, col: int, player : int ):
        if player not in [1,-1]: raise Exception("No es un jugador")
        


        board_row = (self.subboard-1) // 3

        board_column = (self.subboard-1) % 3

        absolute_row = board_row*3 + row
        absolute_col = board_column*3 + col
        if self.board[absolute_row][absolute_col] != 0: return False
        self.board[absolute_row][absolute_col] = player
        self.check_win_subgame()

        self.subboard = 1+ row*3+col
        self.check_pos()

        return True

    def check_win_subgame(self):
        board_row = (self.subboard-1) // 3
        board_column = (self.subboard-1) % 3

        win = 0
        
        k = 0
        r = [0,0,0]
        for i in range(3):

            for j in range(3):

                absolute_row = board_row*3 + i
                absolute_col = board_column*3 + j
                if self.board[absolute_row][absolute_col] != 0:
                    r[j] +=1
                    k+=1
            win = max(win,k,r[0],r[1],r[2])
            k = 0
        diagonals = [0,0]
        for i in range(3):
            absolute_row = board_row*3 + i
            absolute_col = board_column*3 + i
            diagonals[0] += 1 if self.board[absolute_row][absolute_col] != 0 else 0
            absolute_row = board_row*3 + 2-i
            absolute_col = board_column*3 +2- i
            diagonals[1] += 1 if self.board[absolute_row][absolute_col] != 0 else 0
        win = max(win, diagonals[0],diagonals[1])
        if win == 3:
            self.check_board[board_row][board_column] = self.player



    def check_pos(self):
        board_row = (self.subboard-1) // 3
        board_column = (self.subboard-1) % 3

        print(self.check_board, board_row,board_column)
        print(self.check_board[board_row][board_column])
        if self.check_board[board_row][board_column] != 0:
            print(self.__str__())
            self.choose_board()


    def choose_board(self, pos = 0):
        board_row = (self.subboard-1) // 3
        board_column = (self.subboard-1) % 3
        for j in range(3):            
            print([i+j*3+1 for i in range(3)])
        while self.check_board[board_row][board_column] != 0 or pos == 0:
            if pos != 0: print("position not allowed... ")
            board_row = (self.subboard-1) // 3
            board_column = (self.subboard-1) % 3
            pos = int(input("choose your position: "))
        self.subboard = pos
    
    def big_X_O(self, x_o: Literal["x", "o"]) -> list:
        if x_o == "x":
            return [["X", " ", "X"],
                   [" ", "X", " "],
                   ["X", " ", "X"]]
        elif x_o == "o":
            return [[" ", "O", " "],
                   ["O", " ", "O"],
                   [" ", "O", " "]]
        else:
            raise ValueError("x_o must be 'x' or 'o'")

    def __str__(self) -> str:
        vals = ""
        out = ""
        big_x = self.big_X_O("x")
        big_o = self.big_X_O("o")

        for i,b in enumerate(self.board):
            vals = ""
            for j,n in enumerate(b):
                line = " * "if j%3 == 0 else " "
                player = "_"
                if self.check_board[i//3][j//3] == 0:
                   if abs(n) == 1:
                        player = "X" if n ==1 else "O"
                else:
                    player = big_x[i%3][j%3] if self.check_board[i//3][j//3] == 1 else big_o[i%3][j%3]
                vals += line + " " + player + " "
            
            line = "".join([" * " for _ in range(15)]) if i%3 == 0 else ""

            out+= line + "\n"
            out+= vals + "*\n"
        
        out += "".join([" * " for _ in range(15)])

        return out
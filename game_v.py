





class TikTakToe:
    def __init__(self) -> None:
        self.board = [[0 for _ in range(3)] for _ in range(3)]
        self.detailed_board = []
        self.who_won = 0
        self.moves = 0
    
    def play(self, player, man_inputs = True, aut_row = [0], aut_col = [0]):

        isValid = False
        row = 0
        column = 0
        while not isValid:
            if man_inputs:
                row = int(input("choose row: "))
                column = int(input("choose column: "))
            else:
                row = aut_row.pop()
                column = aut_col.pop()
            isValid = self.board[row] [column] == 0
            if not isValid: 
                print("Position not allowed")
                man_inputs = True
            
        self.board[row][column] = player
        self.check_win(player)

        self.moves +=1

        return [row,column]
    
    def check_win(self, player):
        if self.moves == 8:
            self.who_won = 2
        win = 0
        k = 0
        r = [0,0,0]
        for i in range(3):
            for j in range(3):
                r[j] += self.board[i][j] if self.board[i][j] < 2 else 0
                k+=self.board[i][j] if self.board[i][j] < 2 else 0
            win = max(win,abs(k),abs(r[0]),abs(r[1]),abs(r[2]))
            k = 0
        diagonals = [0,0]
        for i in range(3):

            diagonals[0] += self.board[i][i] if self.board[i][i] < 2 else 0
            diagonals[1] += self.board[i][2-i] if self.board[i][2-i] < 2 else 0
        win = max(win, abs(diagonals[0]),abs(diagonals[1]))
        if win == 3:
            self.who_won = player

    
    def __str__(self) -> str:
        outp = [[] for _ in range(3)]
        for i,line in enumerate(self.board):
            for item in line:
                player = "_"
                if abs(item) == 1:
                    player = "X" if item ==1 else "O"
                outp[i].append(player)
                    

        out = "\n".join([str(b) for b in outp])
        return out


class RecursiveTikTakToe(TikTakToe):
    def __init__(self, depth = 1) -> None:
        self.depth = depth
        self.board = [[0 for _ in range(3)] for _ in range(3)]
        if depth == 1:
            self.detailed_board = [[TikTakToe() for _ in range(3)] for _ in range(3)]
        else:
            self.detailed_board = [[RecursiveTikTakToe(depth=depth-1) for _ in range(3)] for _ in range(3)]
        
        self.who_won = 0
        self.moves = 0
        self.last_row_col = [-1,-1]

    def play(self, player, man_inputs = True, aut_row = [0,0], aut_col = [0,0]):

        isValid = self.board[self.last_row_col[0]][self.last_row_col[1]] == 0 if self.last_row_col != [-1,-1] else False
        row = self.last_row_col[0]
        column = self.last_row_col[1]
        while not isValid:
            
            if not man_inputs and len(aut_row) <self.depth+1 and len(aut_col) <self.depth+1:
                man_inputs = True
            if man_inputs:
                print("board number " , self.depth)
                row = int(input("choose row: "))
                column = int(input("choose column: "))
            else:
                row, column = aut_row.pop(), aut_col.pop()

            isValid = self.board[row][column] == 0
            if not isValid: 
                print("Position not allowed")
                man_inputs = True
        self.last_row_col = self.detailed_board[row][column].play(player, man_inputs=man_inputs,aut_row=aut_row,aut_col=aut_col)
        

        if self.detailed_board[row][column].who_won != 0:
            self.board[row][column] = self.detailed_board[row][column].who_won
            self.moves +=1
            self.check_win(player)
        return [row,column]
    
    def complete_board(self):
        return [[tik.board for tik in p] for p in self.detailed_board]
    
    def __str__(self) -> str:
        out = ""
        for g in self.detailed_board:
            l = [[],[],[]]
            for h in g:
                for i in range(3):
                    play_line = []
                    if self.depth == 1:
                        for play in h.board[i]:
                            player = "_"
                            if abs(play) == 1:
                                player = "X" if play ==1 else "O"
                            play_line.append(player)
                    else:
                        for play in h.detailed_board[i]:
                            play_line.append(play.__str__())
                    l[i].append(play_line)
            
            for k in l:
                out = out + str(k) + "\n"
            out = out + "\n"
        return out
    


class GameController:
    def __init__(self, game = RecursiveTikTakToe(depth=1)) -> None:

        self.game = game
        self.player = -1
        self.who_won = 0
    
    def play(self):
        if self.who_won == 0:
            self.print_board()
            self.player = -self.player
            self.who_won = self.game.who_won
            print(self.who_won)
        return self.who_won
    
    def print_board(self):
        #print("Player: ", "X" if self.player == 1 else "O")
        print(self.game.__str__())
        for g in self.game.board:
            print(g)
        get_board_to_play = self.get_board_to_play()
        if get_board_to_play != [-1,-1]:
            print("subBoard: ")
            print(self.game.detailed_board[get_board_to_play[0]][get_board_to_play[1]].__str__())
    def play_no_prints(self):
        if self.who_won == 0:
            self.game.play(self.player)
            self.player = -self.player
            self.who_won = self.game.who_won
        return self.who_won

    def aut_play(self, aut_row,aut_col):
        if self.who_won == 0:
            self.game.play(self.player,man_inputs=False,aut_row=aut_row,aut_col=aut_col)
            self.player = -self.player
            self.who_won = self.game.who_won
        return self.who_won

    def get_game_state(self):
        return self.game.complete_board()
    
    def get_board_to_play(self) -> list[int]:
        if self.game.board[self.game.last_row_col[0]][self.game.last_row_col[1]] != 0:
            return [-1,-1] #si es [-1,-1] entonces tiene que escoger
        return self.game.last_row_col
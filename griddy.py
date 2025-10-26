import random
import game_v

class Griddy:

    def __init__(self, game : game_v.GameController) -> None:
        self.total_points = 0
        self.game = game
        self.name = "Greedy "

    def check_griddy_pos(self,board,r,c):
        player = -1
        diagonal = [False,False]
        if r == c:
            diagonal[0] = True
        if 2-c == r:
            diagonal[1] = True

        sum_val = 0
        for _ in range(2):
            player = -player

            if player == - board[(r+1)%3][c] \
                or player == - board[(r+2)%3][c]:
                sum_val+=0
            else:
                num_of_signs = 0
                for i in range(1,3):
                    num_of_signs += abs(board[(r+i)%3][c])
                sum_val += 10**num_of_signs

            if player == - board[r][(c+1)%3] \
                or player == - board[r][(c+2)%3]:
                sum_val+=0
            else:
                num_of_signs = 0
                for i in range(1,3):    
                    num_of_signs += abs(board[r][(c+i)%3])
                sum_val += 10**num_of_signs
            
            if diagonal[0]:
                if player == - board[(r+1)%3][(c+1)%3] \
                or player == - board[(r+2)%3][(c+2)%3]:
                    sum_val+=0
                else:
                    num_of_signs = 0
                    for i in range(1,3):
                        num_of_signs += abs(board[(r+i)%3][(c+i)%3])
                    sum_val += 10**num_of_signs
            if diagonal[1]:
                if player == - board[(r+1)%3][(c-1)%3] \
                or player == - board[(r+2)%3][(c-2)%3]:
                    sum_val+=0
                else:
                    num_of_signs = 0
                    for i in range(1,3):
                        num_of_signs += abs(board[(r+i)%3][(c-i)%3])
                    sum_val += 10**num_of_signs
        return sum_val

    def single_board_griddy(self, board):

        heurist_board = [[-abs(board[j][i]) for i in range(3)] for j in range(3)]

        for i,line in enumerate(heurist_board):
            for j,item in enumerate(line):
                if item == 0:
                    heurist_board[i][j] = self.check_griddy_pos(board,i,j)
        return heurist_board
    
    def choose_pos(self,board):
        big_heurist_board = self.single_board_griddy(board)
        r,c = [0],[0]
        max_item = -10
        for i,line in enumerate(big_heurist_board):
            for j,item in enumerate(line):
                if item > max_item:
                    r,c = [i],[j]
                    max_item = item
                elif item == max_item:
                    r.append(i)
                    c.append(j)
        
        chooser = random.randint(0,len(r)-1)
                
        return [r[chooser],c[chooser]]
    
    def evaluate_basic_board(self, pos_to_play = [-1,-1]):
        complete_board = self.game.get_game_state()
        if pos_to_play == [-1,-1]:
            pos_to_play = self.game.get_board_to_play()
        if pos_to_play == [-1,-1]: pos_to_play = self.choose_pos(self.game.game.board)
        board_to_play = complete_board[pos_to_play[0]][pos_to_play[1]]
        board_state = self.single_board_griddy(board_to_play)
        print("Pos: ", board_state)

    def play_game(self, pos_to_play = [-1,-1]):
        complete_board = self.game.get_game_state()
        aut_play = ([],[])
        if pos_to_play == [-1,-1]:
            pos_to_play = self.game.get_board_to_play()
        if pos_to_play == [-1,-1]: 
            pos_to_play = self.choose_pos(self.game.game.board)
            aut_play[0].append(pos_to_play[0])
            aut_play[1].append(pos_to_play[1])
        board_to_play = complete_board[pos_to_play[0]][pos_to_play[1]]

        pos_to_play = self.choose_pos(board_to_play)
        aut_play[0].insert(0,pos_to_play[0])
        aut_play[1].insert(0,pos_to_play[1])

        return aut_play

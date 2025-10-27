import math
import random
import numpy
import game_v
class Minimax:
    def __init__(self, game : game_v.GameController, player: int, depth =3) -> None:
        self.total_points = 0
        self.game = game
        self.player = player
        self.depth = depth
        self.name = "Minimax " + str(depth)

    def check_heur_board(self,board : list[list[int]],next_player):
        player = self.player
        sum_val = 0
        for _ in range(2):
            player = -player
            line_val = [0,0,0]
            col_val = [0,0,0]
            diag_val = [0,0]
            for i,line in enumerate(board):
                for j,item in enumerate(line):
                    if player == -item:
                        col_val[j] = -1
                    if player == item and col_val != -1:
                        col_val[j]+=1

                    if player == -item:
                        line_val[i] = -1
                    elif player == item and line_val[i] != -1:
                        line_val[i]+=1
                    
                    if i == j:
                        if player == -item:
                            diag_val[0] = -1
                        elif player == item and diag_val[0]!= -1:
                            diag_val[0]+=1
                    if i == 2-j:
                        if player == -item:
                            diag_val[1] = -1
                        elif player == item and diag_val[1]!= -1:
                            diag_val[1]+=1
            
            l_val = 0
            c_val = 0
            d_val = 0
            for v in line_val:
                l_val += 10**v
            for v in col_val:
                c_val += 10**v
            for v in diag_val:
                d_val += 10**v
            persp_val = int(l_val+c_val+d_val) *player
            persp_val *= 2 if player == next_player and persp_val >100 else 1

            sum_val += persp_val
        
        return sum_val

    def evaluate_pos(self, pos,game: game_v.GameController,player = 0):
        game.aut_play(pos[0][:],pos[1][:])
        general_board = game.game.board
        can_have_subboard = game.get_board_to_play() != [-1,-1]

        general_score = player *self.check_heur_board(general_board, game.player)
        subboard_score = 0
        if can_have_subboard:
            board_to_play = game.get_board_to_play()
            subboard = game.get_game_state()[board_to_play[0]][board_to_play[1]]
            subboard_score = player *self.check_heur_board(subboard, game.player)
        game.undo_play()
        return general_score*10 + subboard_score, [0,0]

    def recursive_minimax(self, game: game_v.GameController ,depth = 1, player = 0, alfa = -math.inf, beta = math.inf) -> tuple[float | int, list[int]]:
        if player == 0:
            player = self.player
        
        general_board = game.game.board
        can_have_subboard = game.get_board_to_play() != [-1,-1]
        
        #caso base
        if abs(game.who_won) == 1:
            return game.who_won * player* math.inf, [0,0]
        if game.who_won == 2:
            return 0,[0,0]
        
        if depth <= 0:
            general_score = player *self.check_heur_board(general_board, game.player)
            subboard_score = 0
            if can_have_subboard:
                board_to_play = game.get_board_to_play()
                subboard = game.get_game_state()[board_to_play[0]][board_to_play[1]]
                subboard_score = player *self.check_heur_board(subboard, game.player)
            return general_score*10 + subboard_score, [0,0]


        posible_pos = self.moves_from_all_board(game)
        
        if not posible_pos:
            return 0, [0,0]
        best_pos = posible_pos[0]
        for pos in posible_pos:
            game.aut_play(pos[0][:],pos[1][:])
            oponent_score,thought_pos = self.recursive_minimax(game,depth = depth-1, player = -player, alfa = -beta, beta = -alfa)
            game.undo_play()
            if alfa< -oponent_score:
                best_pos = pos
                alfa = -oponent_score
            if alfa >= beta:
                break
        return alfa,best_pos

    def get_posible_pos(self, board)-> list[list[int]]:

        all_pos = [[-abs(board[j][i]) for i in range(3)] for j in range(3)]

        posible_pos = []
        for r,line in enumerate(all_pos):
            for c,item in enumerate(line):
                if item == 0:
                    posible_pos.append([r,c])
        return posible_pos
    
    def moves_from_all_board(self, game: game_v.GameController):
        complete_board = game.get_game_state()
        pos_to_play = game.get_board_to_play()
        out =[]
        if pos_to_play == [-1,-1]: 
            pos_boards = self.get_posible_pos(game.game.board)
            local_pos = []
            for board in pos_boards:
                local_pos = self.get_posible_pos(complete_board[board[0]][board[1]])
                for move in local_pos:
                    all_move_r = [[move[0],board[0]],[move[1],board[1]]]
                    out.append(all_move_r)


        else:
            data =self.get_posible_pos(complete_board[pos_to_play[0]][pos_to_play[1]])
            for s in data:
                out.append([[s[0]],[s[1]]])
        
        return out
    
    def play_game(self):
        val,aut_play = (self.recursive_minimax(self.game,depth=self.depth))
        print("my game is:", aut_play)
        print("val is:", val)
        return aut_play


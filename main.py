import game_controler
from bots.minimax import Minimax
from bots.griddy import Griddy
import game_v

def game_v1():
    game = game_controler.Game()

    for _ in range(50):
        print(game)
        game.play()

def game_v2():
    game = game_v.GameController()
    who_won = 0
    game.aut_play([2,0],[2,0])
    game.aut_play([0],[0])
    game.aut_play([1],[1])
    game.aut_play([0],[0])
    game.aut_play([0],[0])

    game.aut_play([0,1],[2,1])
    game.aut_play([1],[1])
    game.aut_play([0],[1])
    game.aut_play([1],[0])
    game.aut_play([0],[2])
    game.aut_play([2],[2])
    game.aut_play([1],[1])

    game.aut_play([0,0],[0,2])
    game.aut_play([2,2],[2,2])
    game.aut_play([1,0],[1,1])
    game.aut_play([0,1],[1,0])
    game.aut_play([1],[2])



    for _ in range(50):
        
        who_won = game.play()

        if who_won != 0:
            break
    
    print("Player ", "X" if who_won == 1 else "O", " won")
    print(game.game.__str__())




def game_pve(game,robot):
    who_won = 0

    for i in range(50):
        print("turn: ", i)
        print(robot.name + " (O): " )
        r,c = robot.play_game()
        print(r,c)
        who_won = game.aut_play(r,c)

        print( "You (X): " )
        who_won = game.play()

        if who_won != 0:
            break
    
    print("Player ", "X" if who_won == 1 else "O", " won")
    print(game.game.__str__())

def battle_robots(game,robot1,robot2):
    who_won = 0
    for i in range(50):
        print("turn: ", i)
        print(robot1.name + " (X): " )
        r,c = robot1.play_game()
        print(r,c)
        who_won = game.aut_play(r,c)
        game.print_board()

        print(robot2.name + " (O): ")
        r,c = robot2.play_game()
        print(r,c)
        who_won = game.aut_play(r,c)
        game.print_board()

        if who_won != 0:
            break
    if who_won == 2:
        print("it's a tie")
    else:
        print("Player ", "O" if who_won == 1 else "X", " won")
    print(game.game.__str__())

game = game_v.GameController()


if __name__ == "__main__":
    battle_robots(game,Minimax(game,-1, depth=8),Minimax(game,1, depth=9))
    #game_pve(game,Minimax(game,-1,6))
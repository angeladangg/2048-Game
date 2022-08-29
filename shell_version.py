import connectfour
import gamefunctions
'''This module contains the functionalities of the game that can be played without connecting to a server'''
#RED = 1
#YELLOW = 2

def run_game(gamestate: tuple)-> None:
    '''this is the main gameloop where it prints the gamestate and continues
        the game, as long as there's no winner'''
    while True:
        print()
        _players_turn(gamestate) # print whos turn it is
        gamestate = making_moves(gamestate) #asks player for move and column
        if _check_for_winner(gamestate) != 0: #constantly check when to end game
            print("The game has ended!!")
            break 
            
def _check_for_winner(gamestate: tuple)-> int:
    '''checks for winner'''
    winner = connectfour.winner(gamestate)
    if winner == 1:
        print("RED has won!!!")
    elif winner == 2:
        print("YELLOW has won!!!")
    else:
        pass
    return winner

def making_moves(gamestate: tuple)-> "updated gamestate":
    '''asks user for the column, and their desired movement'''
    the_move = _player_move() #asks for move
    while True:
        col = int(_desired_col())-1 #asks for desired column to make move on

        if the_move == "P":
            try:
                after_pop = connectfour.pop(gamestate, col)
            except ValueError:
                print("The column number is out of range")
                
            except connectfour.InvalidMoveError:
                print("Invalid move!!!!")
                
                
            else:
                print()
                gamefunctions._print_board(after_pop.board)
                print()
                return after_pop

        if the_move == "D":
            try:
                after_drop = connectfour.drop(gamestate, col)
            except ValueError:
                print("The column number is out of range")
                
            except connectfour.InvalidMoveError:
                print("Invalid move!!!!")
                
            else:
                print()
                gamefunctions._print_board(after_drop.board)
                print()
                return after_drop

    
def _players_turn(gamestate:tuple)->None:
    '''prints the who's turn it is of the game'''
    turn = gamestate[1]
    if turn == 1:
        print("It's Red's turn\n")
    elif turn == 2:
        print("It's Yellow's turn\n")
    
def _player_move()->None:
    '''ask player for their move'''
    while True:
        try:
            move = input("Do you want to drop or pop? (D: drop, P: pop): \n")
            if move != "D" and move != "P":
                raise ValueError
        except ValueError:
            print("*WRONG INPUT!! Please enter the correct move*")
            print()
        else:
            break
    return move

def _desired_col()->str:
    '''ask player for the desired column to make move on'''
    while True:
        try:
            col = input("Select the column to make your move on: ")
            print()
            if col.isdigit() == False:
                raise ValueError
        except ValueError:
            print("*WRONG INPUT!! Please enter the correct column* ")
            print()
        else:
            break
    return col


    

if __name__ == '__main__':
    gamefunctions.welcome() #prints welcome banner
    game_state = gamefunctions._create_game() #initializes a game board
    run_game(game_state) #runs the game until there's a winner

    


import connectfour
"""this module contains overlapping functions for both user interfaces
    some are modified for the server functions"""


def welcome()-> None:
    '''only prints the welcome banner'''
    
    _print_welcome_banner()

def _print_welcome_banner()->None:
    '''printing welcome banner with my simple ascii art'''
    
    print("+------------------------------------+")
    print("| Welcome to the Connect Four game!  |")
    print("+------------------------------------+")

def _print_board(board)->None:
    '''printing the board'''
    #priting only the numbers on top:
    col_num = "" 
    for i in range(1, len(board)+1):
        space = "  "
        if i >=9: 
            space = " "
        col_num += str(i) + space
    print(col_num)
    
    #printing the actual board:
    for i in range(len(board[0])):
        for j in range(len(board)):
            if board[j][i] == 0:
                print( ".  ", end = "")
                
            elif board[j][i] == 1:
                print("R  ", end = "")
                
            elif board[j][i] == 2:
                print("Y  ", end = "")
        print("")

def _create_game()->'game state':
    '''beginning step of creating a board asks user for the board dimension.
        If no valid dimension, ask again'''
    
    while True:
        try:
            rows = int(input("Please enter a row number between 4-20: "))
            columns = int(input("Please enter a column number between 4-20: "))
            gamestate = connectfour.new_game(columns, rows)
            
        except ValueError:
            print()
            print("*Uh oh... your one or both of your inputs is incorrect*")
            print("*Remember the dimensions should be between 4-20!!!!!!")
            print()
            
        else:
            print()
            _print_board(gamestate.board)
            print()
            break
            
    return gamestate

'''BEGINNING OF FUNCTIONS USED IN SERVER VERSION'''

def _create_game_server()->tuple:
    '''server version of _create_game(). returns
        a list of columns, rows, and finally the gamestate'''
    while True:
        try:
            rows = int(input("Please enter a row number between 4-20: "))
            columns = int(input("Please enter a column number between 4-20: "))
            print()
            gamestate = connectfour.new_game(columns, rows)
        except ValueError:
            print()
            print("*Uh oh... your one or both of your inputs is incorrect*")
            print("*Remember the dimensions should be between 4-20!!!!!!")
            print()
        else:
            _print_board(gamestate.board)
            break
            
    return [columns, rows, gamestate]

def making_moves(gamestate: tuple)-> "gamestate":
    '''asks user for the column to make a move on, and their desired movement'''
    the_move = _player_move()
    while True:
        col = int(_desired_col())-1
    
        if the_move == "P":
            try:
                after_pop = connectfour.pop(gamestate, col)
            except ValueError:
                print("The column number is out of range")
                
            except connectfour.InvalidMoveError:
                print("Invalid move!!!!")
                
            else:
                _print_board(after_pop.board)
                return after_pop

        if the_move == "D":
            try:
                after_drop = connectfour.drop(gamestate, col)
            except ValueError:
                print()
                print("The column number is out of range")
                
            except connectfour.InvalidMoveError:
                print()
                print("Invalid move!!!!")
                
            else:
                _print_board(after_drop.board)
                return after_drop
            

def _player_move()-> None:
    '''ask player for their move. If invalid move, ask again'''
    while True:
        try:
            move = input("Do you want to DROP or POP?: \n")
            if move != "DROP" and move != "POP":
                raise ValueError
        except ValueError:
            print()
            print("* WRONG INPUT!! Please enter the correct move *")
            print()
        else:
            break
    return move

def _desired_col(gamestate: tuple)->str:
    '''ask player for the desired column to make move on.
        if invalid, ask again '''
    while True:
        try:
            col = input("Select the column to make your move on: ")
            print()
            if col.isdigit() == False:
                raise ValueError
            if _check_bounds(gamestate,int(col)):
                return col
            else:
                print()
                print("* WRONG INPUT!! Please enter the correct column * ")
            
            
        except ValueError:
            print("*WRONG INPUT!! Please enter the correct column* ")
        
    return col

def _check_bounds(gamestate:tuple, col)-> bool:
    '''checks if column is out of bound'''
    if col <= len(gamestate.board) and col > 0:
        return True
    else:
        return False
    

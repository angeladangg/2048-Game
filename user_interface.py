import connectfour
import socket_handling
import gamefunctions

def run() -> None:
    '''Runs the console-mode user interface from start to finish.'''
    
    gamefunctions.welcome()#printing welcome banner
    server = socket_handling._ask_host()
    port = socket_handling._ask_port()
    connection = socket_handling.connect(server, port)#making socket handled within the .connect() function

    gamestate = _login(connection)# tuple
    
    no_winner = True
    while no_winner:
        try:
            updated_state = _make_the_move(connection, gamestate)#RED
            #print("red")
            if  _is_there_winner(updated_state) == False:
                break
            gamestate = _servers_move(connection, updated_state) #YELLOW
            #print("yellow")
            if _is_there_winner(gamestate) == False:
                break
        except:
            pass
        
def _is_there_winner(gamestate:tuple)-> bool:
    '''CHECKS FOR A WINNER. RETURN FALSE WHEN THERE'S A WINNER'''
    winner = connectfour.winner(gamestate)
    
    if winner == 1:
        print("RED HAS WON!")
        return False
    
    elif winner == 2:
        print("YELLOW HAS WON!")
        return False
    
    else:
        return True


def _servers_move(connection, gamestate)-> "gamestate":
    '''this funciton controls all the server's actions'''
    
    server_move = socket_handling._read_line(connection)
    col_to_drop = int(server_move[-1])-1
    print("AI's move:")
    print()
    
    if "DROP" in server_move:
        updated_state = connectfour.drop(gamestate, col_to_drop)
        gamefunctions._print_board(updated_state.board)
        print()
        
    elif "POP" in server_move:
        updated_state = connectfour.pop(gamestate, col_to_drop)
        gamefunctions._print_board(updated_state.board)
        print()
    socket_handling._read_line(connection)
    return updated_state

def _make_the_move(connection: tuple, gamestate: tuple)->'gamestate':
    '''update and print the board if MOVE = VALID; server edition'''
    
    valid = False
    while not valid:
        #asking for input
        user_move = gamefunctions._player_move() #asing for move
        col_to_drop = gamefunctions._desired_col(gamestate) #asking for col

        #writing to server:
        socket_handling._write_line(connection, f"{user_move} {col_to_drop}") #putting user input to the server
        valid = _check_move_validity(connection, gamestate) #checks server respose
        if user_move == "DROP":
            try:
                new_state = connectfour.drop(gamestate, int(col_to_drop)-1)
            except:
                #don't change gamestate and preserve board prior to function call
                return gamestate
            print("Your move:")
            print()
            gamefunctions._print_board(new_state.board)
            print()
            
        elif user_move == "POP":
            try:
                new_state = connectfour.pop(gamestate, int(col_to_drop)-1)
            except:
                #don't change gamestate and preserve board prior to function call
                return gamestate
            print()
            gamefunctions._print_board(new_state.board)
            print()

        return new_state

def _check_move_validity(connection:tuple, gamestate:tuple)->bool:
    '''CHECK THE SERVERS RESPONSE TO SEE IF CLIENT MOVE = VALID'''
    response = socket_handling._read_line(connection)
    
    if response == "OKAY":
        return True
    
    elif response == "WINNER_RED" or response == "WINNER_YELLOW":

        socket_handling._close(connection)
        pass
        
    elif response == "INVALID":
        print()
        print("INVALID INPUT! TRY AGAIN PLEASE!!")
        return False
        

def _login(connection: tuple)->"gamestate":
    '''checks for valid username '''
    while True:
        username = _ask_player_username()

        if socket_handling.hello(connection, username):#returns bool
            game_state = _ask_for_col_row(connection) #server says READY
            
            return game_state
        else:
            print('Invalid username. Try again')
            
def _ask_for_col_row(connection: tuple)-> "gamestate":
    '''asks users for columns and rows, write to server with row and col.
        returns the gamestates'''
    col_n_row = gamefunctions._create_game_server() #list = [col, row, gamestate]

    input_col = str(col_n_row[0])
    input_row = str(col_n_row[1])
    test = f"{input_col} {input_row}"
    
    #writing to server:
    socket_handling._write_line(connection, f"AI_GAME {input_col} {input_row}")
    
    #reading from server:
    response2 = socket_handling._read_line(connection)
    
    #check for response from server:
    if response2 == "READY":
        print(response2)
        return col_n_row[2] #gamestate
    else:
        raise socket_handling.ProtocolError()
    
def _ask_player_username() -> str:
    '''
    Asks the user to enter a username and returns it as a string.  Continues
    asking repeatedly until the user enters a username that is non-empty
    ''' 
    while True:
        username = input('Start the game with a lit username: ').strip()

        if len(username) > 0:
            return username
        else:
            print('That username is blank; please try again')

    
if __name__ == '__main__':
    run()

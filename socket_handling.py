import socket
from collections import namedtuple


Game = namedtuple('Game',['socket','input','output'])
#port = 4444
#host = "circinus-32.ics.uci.edu"

class ProtocolError(Exception):
    pass

def _ask_host()-> "host":
    """ask for host from user and returns the host"""
    while True:
        host = input("Enter your host: ")
        if host != "circinus-32.ics.uci.edu":
            print()
            print("Invalid host! try again...")
            print()
        else:
            return host
    
    
def _ask_port()-> "port":
    while True:
        port = int(input("Enter your port: "))
        if port != 4444:
            print()
            print("Invalid port! try again...")
            print()
        else:
            return port
def connect(host:str, port:int)-> "Game": #DONE
    '''connects server and port, return namedtuple of connection
        handle connection error too'''
    try:
        game_socket = socket.socket() # making my tin can
        game_socket.connect((host, port)) # conneting host and port
        game_input = game_socket.makefile('r')
        game_output = game_socket.makefile('w')
        print("Successfully connected!")
    except:
        print("CANNOT CONNECT")
        game_input.close()
        game_output.close()
        game_socket.close()
        
    return Game(socket = game_socket,
                input = game_input,
                output = game_output)

def hello(connection: tuple, username)->bool: #
    '''writes in the connection and says hello back'''
    #connection._write_line(username)
    _write_line(connection, f'I32CFSP_HELLO {username}')
    response = _read_line(connection)
    if response ==  f"WELCOME {username}":
        print("\n"+response)
        print("Let's start playing")
        print()
        return True
    else:
        return False

def _write_line(connection, text:str )-> None:
    '''WRITES LINE TO SERVER WHILE ADHERING TO RULES'''
    connection.output.write(text + '\r\n')
    connection.output.flush()

def _read_line(connection):
    '''ONLY READS LINE FROM SERVER'''
    return connection.input.readline()[:-1] #stripping the \n

def _close(connection)-> None:
    '''close everything, print goodbye file'''
    connection.input.close()
    connection.output.close()
    connection.socket.close()


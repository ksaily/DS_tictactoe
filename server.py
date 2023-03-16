import socket, pickle
from _thread import *
import threading
from time import sleep
import json

server = None
HOST_ADDR = "0.0.0.0"
HOST_PORT = 5555
clients = []
BUFFER_SIZE = 1024
LOCK_TIMEOUT = 20

# Define global variables
game_over = False
lock_manager = threading.Lock()
board = []


# Start server function
def start_server():
    global game_state, board, player_data, clients, server
    game_state = ''
    board = initialize_board()
    clients = []

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(socket.AF_INET)
    print(socket.SOCK_STREAM)

    server.bind((HOST_ADDR, HOST_PORT))

    #Accept incoming connection
    while True:
        server.listen()  # server is listening for client connection
        if len(clients) < 2:
            conn, addr = server.accept()
            print(f"New connection from: {conn}")
            clients.append(conn)
            if len(clients) < 2:
                player_id = 'X'
            else:
                player_id = 'O'
            threading.Thread(target=handle_client, args=(conn,addr, player_id)).start()
        
        
        
def handle_client(conn, addr, player_id):
    global game_state

    #if player_id == 'X':
    #    lock_manager.acquire()
    conn.send(str.encode(player_id))
    while True:
        if len(clients) == 2:
            # Acquire lock before processing request
            lock_acquired = lock_manager.acquire()
            if lock_acquired:
                print(f"Lock acquired by {player_id}")
                # Send current board to client
                boardJson = json.dumps({"a": board})
                conn.send(boardJson.encode())

                #Receive move from client
                data = conn.recv(BUFFER_SIZE)
                coord = json.loads(data.decode())
                move = (coord.get("x"), coord.get("y"))
                
                if is_valid_move(move):
                    make_move(move, player_id)
                    print("Check win")
                    # Send response to client with updated game state
                    resp = check_win(board, player_id)
                    if game_over:
                        print("Game over")
                        #for c in clients:
                        #    if resp == "Tie":
                        #        response = "It's a tie!"
                        #    else:
                        #        response = f"Game over! Player {player_id} won the game!"
                        #    c.send(str.encode(response))
                        sleep(3)
                        break
                    #conn.send(str.encode(resp))
                    print("Releasing lock")
                    lock_manager.release()
                    sleep(5)
                else:
                    #conn.send(str.encode('Invalid move.'))
                    lock_manager.release()
                    sleep(5)
            else:
                conn.sendall(str.encode('ERROR: Timeout waiting for lock'))
                break
        else:
            print("Waiting for an opponent")
            sleep(5)




def is_valid_move(move):
    x, y = move
    if (board[x][y] == None):
        return True
    else:
        return False
        

def make_move(move, player_id):
    global board
    x, y = move
    board[x][y] = player_id


def initialize_board():
    return [[None, None, None], [None, None, None], [None, None, None]]


def display_board(board):
    for row in board:
        print(row)


def check_win(board, player):
    global game_over
    # Check rows
    for row in board:
        if row[0] == player and row[1] == player and row[2] == player:
            game_over = True
            return

    # Check columns
    for col in range(3):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            game_over = True
            return

    # Check diagonals
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        game_over = True
        return

    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        game_over = True
        return

    # Check for tie
    if all(x is not None for row in board for x in row):
        game_over = True
        return "Tie"

    # No winner or tie yet
    return "Continue"


if __name__ == '__main__':
    start_server()
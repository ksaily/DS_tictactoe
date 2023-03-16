import socket, pickle
import json

BUFFER_SIZE=1024
def prompt_move():
    while True:
        try:
            x = int(input("Enter row (0-2): "))
            y = int(input("Enter column (0-2): "))
            return (x, y)
        except ValueError:
            print("Invalid input, please enter integers.")

def display_board(board):
    for row in board:
        print(row)

def main():
    # Connect to server
    host = 'localhost'
    port = 5555
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    success = sock.connect((host, port))
    print("Connected to server.")

    # Get player ID from server
    player_id = sock.recv(1024).decode()
    print(f"You are player {player_id}")

    # Play game
    while True:
        try:
            # Get current game state from server
        
            packet = sock.recv(BUFFER_SIZE)
            data = json.loads(packet.decode())
            board = data.get("a")
            #data = sock.recv(4096)
            #if not data:
            #    print("Connection closed by server")
            #    break
            #board = pickle.(data)

            print("Current game state:")
            display_board(board)

            # Prompt user for move
            print("Your turn:")
            move = prompt_move()
            x, y = move
            move = json.dumps({"x": x, "y": y})
            sock.send(move.encode())
            """
            # Wait for server to respond with updated game state
            status = sock.recv(1024).decode()
            if status == "Invalid move.":
                print("Invalid move, you lost your turn.")
                continue
            elif status == "You lost":
                print("Game over. You lost.")
                break
            elif status == "Continue":
                print("")
                continue
            elif status == "Tie":
                print("Game over. It's a tie!")
                break
            else:
                print(status)
                continue
            """
        except:
            break
    # Close socket
    sock.close()

if __name__ == '__main__':
    main()
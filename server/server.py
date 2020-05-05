import socket
import pickle
from _thread import start_new_thread

import yaml

from models.game import Game
from models.player import Player
from models.move import Move
from models.game_state import GameState
from server_utils import (
    process_handshake,
    process_new_game,
    process_join_game,
    process_disconnect
)

# IP address of the server and the running port from a config file
config_file = "local_server.yaml"

with open(r"../configs/" + config_file) as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
    server = config["server"]
    port = config["port"]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Checking if port and server are accessible
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

# Setting number of available connections
s.listen(50)

print("Server started successfully ({})".format(config["name"]))
print("Waiting for a connection...")

# Setting up list of games
game_list = []
current_game = 0

# Setting up list of players
players = []


# Client communication thread
def threaded_client(conn, player):
    global current_game
    conn.send(pickle.dumps(player))
    reply = ""

    # Client listening loop
    while True:
        try:
            # Limit of bits that can be received per message
            data = pickle.loads(conn.recv(2048*2))

            if not data:
                print("Disconnected (id = {})".format(player.id))
                break

            # Processing player in menu screen
            elif player.state == "choosing":
                # Handshake: getting Hello message from client and sending game_list
                if data == "Hello":
                    reply = process_handshake(player, game_list)

                # New game: getting game objects and sending its id
                elif type(data) is Game:
                    current_game += 1
                    reply = process_new_game(player, data, current_game, game_list)

                # Join game: getting game id and sending it back if available to join
                elif type(data) == int:
                    reply = process_join_game(player, data, game_list)

                conn.sendall(pickle.dumps(reply))

            # Processing player while joined the game
            elif player.state == "joined":
                # Observing game list
                if type(data) == int:
                    reply = game_list
                    game = [game for game in game_list if game.id == data][0]
                    conn.sendall(pickle.dumps(reply))

                    # If all players joined than start the game
                    if game.max_players <= len(game.current_players):
                        player.state = "playing"

                        move = Move(None, None)
                        game_state = GameState(game.id, 0, 1, None, game.current_players[0], move)
                        conn.sendall(pickle.dumps(game_state))

            # Processing player while playing the game
            elif player.state == "playing":
                pass

        except (socket.error, EOFError) as e:
            break

    print("Lost connection (id = {})".format(player.id))
    process_disconnect(player, game_list)
    conn.close()


# Accepting new connections
current_player = 0
while True:
    conn, address = s.accept()
    print("Connected to: ", address)

    # Creating player from given id and appending to list of players
    player = Player(current_player)
    players.append(player)

    # Starting new thread for each client
    start_new_thread(threaded_client, (conn, player))
    current_player += 1



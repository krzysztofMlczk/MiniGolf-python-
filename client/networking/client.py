import sys
sys.path.append("..")

import yaml

from network import Network
from models.game import Game

# SERVER CONNECTION PIPELINE
config_file = "local_server.yaml"

with open(r"../configs/" + config_file) as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Creating connection to server
n = Network(config)
game_list = n.send("Hello")

# Printing player id
print("Your id: ", n.player.id)

# Printing available games
print("\nGame list: ")
for game in game_list:
    print(game)
print("Id: 0, New Game")
print("Id: -1, quit\n")

# Waiting for option input
option = int(input("Chosen option: "))

# If new game sending new game objects and setting state to joined
if option == 0:
    game_id = n.send(Game(0, 10, 2))

# If option is -1 than quitting
elif option == -1:
    print("Quit")
    exit()

# If joining game, sending game id to join
else:
    game_id = n.send(option)

# Waiting for players to join
print("In game: ", game_id)
print("Waiting for players...")
current = 1

while True:
    game_list = n.send(game_id)
    game = [game for game in game_list if game.id == game_id][0]

    if len(game.current_players) != current:
        current = len(game.current_players)
        print("Players: {}/{}".format(current, game.max_players))

    if len(game.current_players) >= game.max_players:
        break

print("Starting game")
init_state = n.listen()
print(init_state)

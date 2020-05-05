def process_handshake(player, game_list):
    print("New player connected (id = {})".format(player.id))

    # Returns list of current games
    return game_list


def process_new_game(player, data, current_game, game_list):
    print("Creating new game (id = {})".format(current_game))
    data.id = current_game
    data.current_players.append(player.id)
    game_list.append(data)
    player.state = "joined"

    # Returns game id
    return current_game


def process_join_game(player, data, game_list):
    print("Player {} joined game {}".format(player.id, data))
    game = [game for game in game_list if game.id == data][0]
    game.current_players.append(player.id)
    player.state = "joined"

    # Returns game id
    return data


def process_disconnect(player, game_list):
    # Deleting disconnected player from games and cleaning games with no players
    for i in range(len(game_list)):
        game = game_list[i]
        if player.id in game.current_players:
            game.current_players.remove(player.id)

        if not game.current_players:
            game_list.remove(game)
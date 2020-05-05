class Game:
    def __init__(self, id, levels, max_players):
        self.id = id
        self.levels = levels
        self.max_players = max_players
        self.current_players = []

    def __str__(self):
        return "Id: {}, Levels: {}, Max players: {}, Current players: {}".format(
            self.id, self.levels, self.max_players, self.current_players
        )
class GameState:
    def __init__(self, game_id, map_id, level, current, next, move):
        self.game_id = game_id
        self.map_id = map_id
        self.level = level
        self.current = current
        self.next = next
        self.move = move

    def __str__(self):
        return "Game id: {}, Map id: {}, Level: {}, Current: {}, Next: {}, Move: ({})".format(
            self.game_id, self.map_id, self.level, self.current, self.next, self.move
        )

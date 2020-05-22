class Player:
    """Player class holding player id, points and ball"""

    def __init__(self, id, color):
        self.id = id
        self.color = color
        self.ball = None
        self.points = {}

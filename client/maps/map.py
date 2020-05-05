from pymunk import Vec2d

from client.objects.wall import Wall
from client.objects.cup import Cup


class Map:
    def __init__(self, id, space):
        # TODO
        # Upload map from file by index, perhaps some loader required

        self.cup = Cup(Vec2d(700, 340), 14)
        self.obstacles = [
            Wall(space, (50, 800), (1230, 800), 6, 1.0),
            Wall(space, (50, 110), (1230, 110), 6, 1.0),
            Wall(space, (1230, 800), (1230, 110), 6, 1.0),
            Wall(space, (50, 110), (50, 800), 6, 1.0),
            Wall(space, (100, 300), (150, 240), 6, 1.0)
        ]

    def draw(self, screen):
        for o in self.obstacles:
            o.draw(screen)

        self.cup.draw(screen)

from client.objects.ObstacleBrickWallSegment import ObstacleBrickWallSegment
from client.objects.ObjectCup import ObjectCup
from client.objects.Ball import Ball
from client.objects.ObstacleRock import ObstacleRock
from client.objects.SurfaceGrass import SurfaceGrass


class Map:
    def __init__(self, id, cup):
        # TODO
        # Upload map from file by index, perhaps some loader required
        self.id = id
        self.cup = cup

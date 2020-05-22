import json
from client.objects.ObjectCup import ObjectCup
from client.objects.ObstacleBrickWallSegment import ObstacleBrickWallSegment
from client.objects.ObstacleRock import ObstacleRock
from client.objects.SurfaceGrass import SurfaceGrass
from client.objects.SurfaceIce import SurfaceIce
from client.objects.SurfaceDirt import SurfaceDirt
from client.objects.SurfaceLava import SurfaceLava
from client.objects.ObstacleTirangleBrick import ObstacleTriangleBrick


class Loader(object):
    def __init__(self, manager):
        self.obj_mgr = manager
        self.maps = []

    def add_map_file(self, filename):
        self.maps.append(self.map_from_file(filename))

    def next_map(self):
        """Returns map's id and cup"""
        if self.maps:
            level = self.maps.pop(0)
            return self.map_from_info(level)
        else:
            return None

    @staticmethod
    def map_info(string):
        """Changes string to map list"""
        print(json.loads(string))
        return json.loads(string)

    @staticmethod
    def map_from_file(filename):
        """Loads a map info from file"""
        file = open(filename, 'r')
        raw = file.read()
        file.close()
        return Loader.map_info(raw)

    def map_from_info(self, level):
        for bws in level['bws']:
            ObstacleBrickWallSegment(bws['pos'], bws['dim'], self.obj_mgr)
        for rock in level['rock']:
            ObstacleRock(rock['pos'], rock['dim'], self.obj_mgr)
        for dirt in level['dirt']:
            SurfaceDirt(dirt['pos'], dirt['dim'], self.obj_mgr)
        for ice in level['ice']:
            SurfaceIce(ice['pos'], ice['dim'], self.obj_mgr)
        for grass in level['grass']:
            SurfaceGrass(grass['pos'], grass['dim'], self.obj_mgr)
        for lava in level['lava']:
            SurfaceLava(lava['pos'], lava['dim'], self.obj_mgr)
        for triangle in level['triangle']:
            ObstacleTriangleBrick(triangle['pos'], triangle['dim'], self.obj_mgr)
        cup = ObjectCup(level['cup']['pos'], level['cup']['dim'], self.obj_mgr)
        id = level['id']
        return id, cup

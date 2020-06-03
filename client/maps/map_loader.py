import json

from client.objects.ObjectCup import ObjectCup
from client.objects.Obstacle import Obstacle
from client.objects.Surface import Surface


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
        for surface in level["surfaces"]:
            Surface.from_template(obj_mgr=self.obj_mgr, **surface)

        for obstacle in level["obstacles"]:
            Obstacle.from_template(obj_mgr=self.obj_mgr, **obstacle)

        cup = ObjectCup(self.obj_mgr, **level['cup'], )

        return level['id'], cup

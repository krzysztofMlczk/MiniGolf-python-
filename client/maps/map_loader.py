import json
from client.objects.ObjectCup import ObjectCup
from client.objects.Obstacle import Obstacle
from client.objects.Surface import Surface
from client.resources.ResourcesManager import ResourcesManager
import client.objects.SurfaceVelocities as SurfaceVelocities


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
            Obstacle(bws['pos'], bws['dim'], ResourcesManager.get_image('wall_brick'), 0.8, self.obj_mgr)
        for rock in level['rock']:
            Obstacle(rock['pos'], rock['dim'], ResourcesManager.get_image('obj_rock'), 0.5, self.obj_mgr)
        for dirt in level['dirt']:
            Surface(dirt['pos'], dirt['dim'], ResourcesManager.get_image('surf_dirt'), 4.0,
                    SurfaceVelocities.velocity_wobble, self.obj_mgr)
        for ice in level['ice']:
            Surface(ice['pos'], ice['dim'], ResourcesManager.get_image('surf_ice'), 1.0,
                    SurfaceVelocities.velocity_default, self.obj_mgr)
        for grass in level['grass']:
            Surface(grass['pos'], grass['dim'], ResourcesManager.get_image('surf_grass'), 3.0,
                    SurfaceVelocities.velocity_default, self.obj_mgr)
        for lava in level['lava']:
            Surface(lava['pos'], lava['dim'], ResourcesManager.get_image('surf_lava'), 5.0,
                    SurfaceVelocities.velocity_default, self.obj_mgr)
        for triangle in level['triangle']:
            Obstacle(triangle['pos'], triangle['dim'], ResourcesManager.get_image('wall_triangle_brick'), 0.5,
                     self.obj_mgr)
        cup = ObjectCup(level['cup']['pos'], level['cup']['dim'], self.obj_mgr)
        id = level['id']
        return id, cup

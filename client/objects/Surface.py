import yaml
import pygame

from client.objects.Object import Object
from client.resources.ResourcesManager import ResourcesManager
from client.objects import SurfaceVelocities

template_dir = "./client/objects/templates/"


class Surface(Object):
    def __init__(self, pos, dim, obj_mgr, name=None, id=-1, friction=4, velocity_func="default", **kwargs):
        self.position = pos
        self.friction = friction
        self.velocity_func = SurfaceVelocities.get_by_name(velocity_func)
        super().__init__(pos, dim, ResourcesManager.get_image(name), id, name=name, obj_mgr=obj_mgr)

    def get_rect(self):
        return pygame.Rect(self.position[0], self.position[1],
                           self.image.get_width(), self.image.get_height())

    def draw(self, display):
        display.blit(self.image, self.position)

    @classmethod
    def from_template(cls, name, pos, dim, obj_mgr, **kwargs):
        with open(template_dir + name + ".yaml") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        return Surface(pos, dim, obj_mgr, **config)


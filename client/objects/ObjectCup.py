import math

import pymunk

from client.objects.Object import Object
from client.resources.ResourcesManager import ResourcesManager


class ObjectCup(Object):
    def __init__(self, obj_mgr, pos=None, dim=None, id=-1, **kwargs):
        image = ResourcesManager.get_image('obj_hole')
        self.radius = dim[0] / 2
        super().__init__(pos, dim, image, id=id, name='cup', obj_mgr=obj_mgr)

    def prepare_body(self, position):
        body = pymunk.body.Body(1, pymunk.inf, body_type=pymunk.Body.STATIC)
        shape = pymunk.Circle(body, self.radius)
        shape.body.position = position

        # Collision type for cup objects is 2
        shape.collision_type = 2

        return shape

    def get_center(self):
        pos = self.get_position(pygame=True)
        return pos[0] - self.image.get_width() / 2, pos[1] - self.image.get_height() / 2

    def ball_in(self, pos):
        cup_pos = self.get_position()
        distance = math.sqrt(((pos[0] - cup_pos[0])**2) + ((pos[1] - cup_pos[1])**2))
        return distance < self.radius

    def draw(self, display):
        display.blit(self.image, self.get_center())

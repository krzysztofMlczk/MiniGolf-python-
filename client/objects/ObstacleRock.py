import pymunk
import pygame

from client.objects.Object import Object
from client.utils import flip_coords
from client.collision.CollisionManager import CollisionManager
from client.resources.ResourcesManager import ResourcesManager


class ObstacleRock(Object):
    def __init__(self, pos, dimension, obj_mgr, id=-1):
        self.offset = None
        super().__init__(pos, dimension, ResourcesManager.get_image('obj_rock'), id, obj_mgr=obj_mgr)

    def prepare_body(self, position):
        body = pymunk.body.Body(body_type=pymunk.Body.STATIC)
        shape, self.offset = CollisionManager.create_collision_shape(self.image, body)
        shape.elasticity = 0.5
        shape.body.position = position

        # Collision type for obstacle objects is 3
        shape.collision_type = 3

        return shape

    def draw(self, display):
        pos = (self.shape.bb.left - self.offset[0], self.shape.bb.top + self.offset[1])
        display.blit(self.image, flip_coords(pos))

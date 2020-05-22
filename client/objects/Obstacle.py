import pymunk

from client.objects.Object import Object
from client.collision.CollisionManager import CollisionManager
from client.utils import flip_coords

'''
    Collision types:
    1 - balls
    2 - cups
    3 - obstacles
'''


class Obstacle(Object):
    def __init__(self, pos, dimension, image, elasticity, obj_mgr, id=-1, name=''):
        self.offset = None
        self.elasticity = elasticity
        super().__init__(pos, dimension, image, id, name=name, obj_mgr=obj_mgr)

    def prepare_body(self, position):
        body = pymunk.body.Body(body_type=pymunk.Body.STATIC)
        shape, self.offset = CollisionManager.create_collision_shape(self.image, body)
        shape.elasticity = self.elasticity
        shape.body.position = position

        shape.collision_type = 3

        return shape

    def draw(self, display):
        pos = (self.shape.bb.left - self.offset[0], self.shape.bb.top + self.offset[1])
        display.blit(self.image, flip_coords(pos))

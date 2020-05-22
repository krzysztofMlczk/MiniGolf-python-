import pymunk

from client.objects.Object import Object
from client.utils import flip_coords
from client.collision.CollisionManager import CollisionManager
from client.resources.ResourcesManager import ResourcesManager


class ObstacleBrickWallSegment(Object):
    def __init__(self, pos, dimension, obj_mgr, id=-1):
        self.offset = None
        self.elasticity = 0.8
        super().__init__(pos, dimension, ResourcesManager.get_image('wall_brick'), id, obj_mgr=obj_mgr)

    def prepare_body(self, position):
        body = pymunk.body.Body(body_type=pymunk.Body.STATIC)
        shape, self.offset = CollisionManager.create_collision_shape(self.image, body)
        shape.elasticity = self.elasticity
        shape.body.position = position

        # Collision type for obstacle objects is 3
        shape.collision_type = 3

        return shape

    def draw(self, display):
        pos = (self.shape.bb.left, self.shape.bb.top)
        display.blit(self.image, flip_coords(pos))

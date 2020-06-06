import yaml
import pymunk
import pygame

from client.objects.Object import Object
from client.collision.CollisionManager import CollisionManager
from client.resources.ResourcesManager import ResourcesManager
from client.utils import flip_coords

'''
    Collision types:
    1 - balls
    2 - cups
    3 - obstacles
'''
template_dir = "./client/objects/templates/"


class Obstacle(Object):

    def __init__(self, pos, dim, obj_mgr, name=None, id=-1, elasticity=1.0, rotation=0, overlap=None, **kwargs):
        self.offset = None
        self.elasticity = elasticity

        if overlap is None:
            img = ResourcesManager.get_image(name)
        else:
            img = overlap

        super().__init__(pos, dim, img, id, name=name, obj_mgr=obj_mgr, rotation=rotation)

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

    @classmethod
    def from_template(cls, name, pos, dim, obj_mgr, vertical=1, horizontal=1, rotation=0, **kwargs):
        with open(template_dir + name + ".yaml") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        if vertical != 1 or horizontal != 1:
            img = pygame.Surface((horizontal * dim[0], vertical * dim[1]))
            texture = pygame.transform.scale(ResourcesManager.get_image(name), dim)

            for x in range(horizontal):
                for y in range(vertical):
                    img.blit(texture, (x * dim[0], y * dim[1]))

            Obstacle(pos, img.get_size(), obj_mgr, rotation=rotation, overlap=img, **config)
        else:
            Obstacle(pos, dim, obj_mgr, rotation=rotation, **config)

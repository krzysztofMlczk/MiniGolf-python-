import pygame

from client.utils import flip_coords


# Base class of all objects on the scene.
class Object(pygame.sprite.Sprite):
    def __init__(self, position, dimension, image, id=-1, name='', obj_mgr=None, obj_type='static'):
        super().__init__()

        self.image = pygame.transform.scale(image, dimension)
        self.id = id
        self.name = name
        self.shape = self.prepare_body(flip_coords(position))
        self.object_mgr = obj_mgr
        self.type = obj_type

        # Add newly created objects to the Object Manager, if not mentioned otherwise
        if obj_mgr is not None:
            obj_mgr.register_object(self)

    # For bodied objects only:
    def get_position(self, pygame=False):
        if pygame:
            return flip_coords(self.shape.body.position)
        else:
            return self.shape.body.position

    def prepare_body(self, position):
        return None

    def draw(self, display):
        pass

    def update(self):
        pass

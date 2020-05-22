import pygame

from client.objects.Object import Object


class Surface(Object):
    def __init__(self, position, dimension, image, friction, id=-1, obj_mgr=None):
        self.friction = friction
        self.position = position
        super().__init__(position, dimension, image, id=-1, obj_mgr=obj_mgr)

    def get_rect(self):
        return pygame.Rect(self.position[0], self.position[1],
                           self.image.get_width(), self.image.get_height())

    def change_velocity(self, vel):
        pass

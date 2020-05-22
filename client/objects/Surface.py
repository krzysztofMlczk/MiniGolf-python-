import pygame

from client.objects.Object import Object


class Surface(Object):
    def __init__(self, position, dimension, image, friction, velocity_func, obj_mgr=None, id=-1, name=''):
        self.friction = friction
        self.position = position
        self.velocity_func = velocity_func
        super().__init__(position, dimension, image, id=id, name=name, obj_mgr=obj_mgr)

    def get_rect(self):
        return pygame.Rect(self.position[0], self.position[1],
                           self.image.get_width(), self.image.get_height())

    def draw(self, display):
        display.blit(self.image, self.position)

import pygame

from client.gui.GUIElement import GUIElement


class Label(GUIElement):
    def __init__(self, name, dimension, position, image, obj_mgr, default_res=None):
        super().__init__(position, dimension, image, name, obj_mgr, default_res)

    def on_scr_resize(self, new_screen):
        new_size = new_screen.get_size()

        x_ratio = new_size[0] / self.old_scr_size[0]
        y_ratio = new_size[1] / self.old_scr_size[1]

        dimension = (round(self.image.get_width() * x_ratio), round(self.image.get_height() * y_ratio))
        self.position = (round(x_ratio * self.position[0]), round(y_ratio * self.position[1]))

        self.image = pygame.transform.scale(self.image_original, dimension)
        self.old_scr_size = new_size

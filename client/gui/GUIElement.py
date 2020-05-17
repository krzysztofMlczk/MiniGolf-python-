import pygame

from client.objects.ObjectManager import ObjectManager


# This class represents a simple GUI element
# like button, label etc.
class GUIElement(pygame.sprite.Sprite):
    def __init__(self, position, dimension, image, name, obj_mgr=None, default_res=None):
        super().__init__()
        self.position = position
        self.name = name
        self.image_original = image
        self.image = pygame.transform.scale(image, dimension)
        self.visible = True

        self.old_scr_size = default_res

        if obj_mgr is not None:
            obj_mgr.register_gui_elem(self)

    def set_image(self, image):
        self.image = image

    def set_visible(self, b):
        self.visible = b

    def get_visible(self):
        return self.visible

    def set_position(self, pos):
        super().position = pos

    def get_position(self):
        return self.position

    def set_size(self, dimension):
        self.image = pygame.transform.scale(self.image_original, dimension)

    def get_size(self):
        return self.image.get_width, self.image.get_height

    def draw(self, display):
        if self.old_scr_size is None:
            self.old_scr_size = display.get_size()

        if self.visible:
            display.blit(self.image, self.position)

    def update(self):
        pass

    def on_scr_resize(self, new_size):
        pass

    def get_rect(self):
        return pygame.rect.Rect(self.position[0], self.position[1], self.image.get_width(), self.image.get_height())

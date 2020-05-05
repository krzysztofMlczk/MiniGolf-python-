import pygame

from client.objects.ObjectManager import ObjectManager


class GUIElement(pygame.sprite.Sprite):
    def __init__(self, position, dimension, image, name, noregister=False):
        super().__init__()
        self.position = position
        self.name = name
        self.image = pygame.transform.scale(image, dimension)
        self.visible = True

        if not noregister:
            ObjectManager.register_gui_elem(self)

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
        self.image = pygame.transform.scale(self.image, dimension)

    def get_size(self):
        return self.image.get_width, self.image.get_height

    def update(self, display):
        if self.visible:
            display.blit(self.image, self.position)

    def get_rect(self):
        return pygame.rect.Rect(self.position[0], self.position[1], self.image.get_width(), self.image.get_height())

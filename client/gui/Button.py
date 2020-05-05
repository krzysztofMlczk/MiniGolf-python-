import pygame

from client.gui.GUIElement import GUIElement


class Button(GUIElement):
    def __init__(self, name, dimension, position, image, image_hover):
        super().__init__(position, dimension, image, name)
        self.image_default = self.image
        self.image_hover = pygame.transform.scale(image_hover, dimension)
        self.clicked = False

    def on_mouse_enter(self):
        self.image = self.image_hover

    def on_mouse_quit(self):
        if self.clicked:
            self.on_mouse_released()
        self.image = self.image_default

    def on_mouse_clicked(self):
        self.clicked = True
        self.position = (self.position[0] + 1, self.position[1] + 1)

    def on_mouse_released(self):
        if self.clicked:
            self.clicked = False
            self.position = (self.position[0] - 1, self.position[1] - 1)

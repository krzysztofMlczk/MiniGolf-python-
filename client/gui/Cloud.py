import pygame

from client.gui.GUIElement import GUIElement


class Cloud(GUIElement):
    def __init__(self, position, dimension, height_coefficient, width_coefficient, image, name, move_dir):
        super().__init__(position, dimension, image, name)
        self.height_coefficient = height_coefficient
        self.width_coefficient = width_coefficient
        self.move_dir = move_dir

    def update(self, display):
        if self.visible:
            (width, height) = display.get_size()
            left_cloud_border = width * self.width_coefficient
            right_cloud_border = width * self.width_coefficient
            y = height * self.height_coefficient
            # change coordinates
            if self.move_dir == "right":
                x = self.position[0] + 1
            else:
                x = self.position[0] - 1
            # deal with the left cloud
            if self.name == "left_cloud":
                if x < 0:
                    self.move_dir = "right"
                elif x > left_cloud_border and self.move_dir == "right":
                    self.move_dir = "left"
            # deal with the right cloud
            elif self.name == "right_cloud":
                if x + self.image.get_width() > width:
                    self.move_dir = "left"
                elif x < right_cloud_border and self.move_dir == "left":
                    self.move_dir = "right"
            self.position = (x, y)
            display.blit(self.image, self.position)

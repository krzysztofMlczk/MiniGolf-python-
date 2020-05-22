import pygame

from client.gui.GUIElement import GUIElement


class Cloud(GUIElement):
    def __init__(self, position, dimension, height_coefficient, width_coefficient, image, name, move_dir, obj_mgr,
                 default_res=None):
        super().__init__(position, dimension, image, name, obj_mgr, default_res)
        self.height_coefficient = height_coefficient
        self.width_coefficient = width_coefficient
        self.move_dir = move_dir
        self.step = 0.5
        self.pos_abs = position[0]

    def draw(self, display):
        if self.old_scr_size is None:
            self.old_scr_size = display.get_size()

        if self.visible:
            (width, height) = display.get_size()
            left_cloud_border = width * self.width_coefficient
            right_cloud_border = width * self.width_coefficient
            y = height * self.height_coefficient
            # change coordinates
            if self.move_dir == "right":
                self.pos_abs += self.step
                x = round(self.pos_abs)
            else:
                self.pos_abs -= self.step
                x = round(self.pos_abs)
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

    def on_scr_resize(self, new_screen):
        new_size = new_screen.get_size()

        x_ratio = new_size[0] / self.old_scr_size[0]
        y_ratio = new_size[1] / self.old_scr_size[1]

        self.step *= x_ratio

        dimension = (round(self.image.get_width() * x_ratio), round(self.image.get_height() * y_ratio))
        self.position = (round(x_ratio * self.position[0]), round(y_ratio * self.position[1]))

        self.image = pygame.transform.scale(self.image_original, dimension)
        self.pos_abs = self.position[0]

        self.old_scr_size = new_size

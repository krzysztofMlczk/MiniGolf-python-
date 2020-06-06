import pygame

from client.gui.GUIElement import GUIElement
from client.models.scene_init import SceneInit


class Button(GUIElement):
    def __init__(self, name, dimension, position, image, image_hover, obj_mgr, default_res=None):
        super().__init__(position, dimension, image, name, obj_mgr, default_res)

        self.image_default_original = image
        self.image_hover_original = image_hover

        self.image_default = pygame.transform.scale(self.image_default_original, dimension)
        self.image_hover = pygame.transform.scale(self.image_hover_original, dimension)

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

    def on_mouse_released(self, players=None, maps_to_play=None):
        if self.clicked:
            self.clicked = False
            self.position = (self.position[0] - 1, self.position[1] - 1)

            if self.name == "single":
                scene_init = SceneInit("SingleSetup", screen=self.get_current_screen())

            elif self.name == "multi":
                scene_init = SceneInit("MultiSetup", screen=self.get_current_screen())

            elif self.name == "players_up" or self.name == "maps_up":
                return 1

            elif self.name == "players_down" or self.name == "maps_down":
                return -1

            elif self.name == "play_btn":
                scene_init = SceneInit("Game", players=players, maps_to_play=maps_to_play)

            elif self.name == "cancel_btn":
                scene_init = SceneInit("Menu", screen=self.get_current_screen())

            elif self.name == "about":
                scene_init = SceneInit("About", screen=self.get_current_screen())

            elif self.name == "quit":
                scene_init = None
                exit(0)

            else:
                scene_init = None

            return scene_init

        return None

    def on_scr_resize(self, new_screen):

        # Getting new screen size
        new_size = new_screen.get_size()

        # Calculating ratio
        x_ratio = new_size[0] / self.old_scr_size[0]
        y_ratio = new_size[1] / self.old_scr_size[1]

        # Calculating new center
        center = (self.position[0] + self.image.get_width() // 2,
                  self.position[1] + self.image.get_height() // 2)

        center = (round(center[0] * x_ratio), round(center[1] * y_ratio))

        dimension = (round(self.image.get_width() * x_ratio), round(self.image.get_height() * y_ratio))
        self.position = (center[0] - dimension[0] // 2, center[1] - dimension[1] // 2)

        # Scaling images
        self.image_default = pygame.transform.scale(self.image_default_original, dimension)
        self.image_hover = pygame.transform.scale(self.image_hover_original, dimension)
        self.image = pygame.transform.scale(self.image_original, dimension)

        self.old_scr_size = new_size

    def get_current_screen(self):
        info = pygame.display.Info()
        return pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)

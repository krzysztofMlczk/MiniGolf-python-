import pygame

from client.objects.ObjectManager import ObjectManager
from client.gui.GUIManager import GUIManager


# This class represents a scene, by default
# each scene has its own ObjectManager which
# is storing all of the objects and gui elements
# present in that scene and is responsible for
# drawing and updating them.
class Scene:
    def __init__(self, space, fill_color=(0, 0, 0)):
        self.fill_color = fill_color
        self.display = pygame.Surface((1920, 1080), flags=pygame.SRCALPHA)
        self.object_mgr = ObjectManager(space, self.display)
        self.gui_mgr = GUIManager()

    def get_space(self):
        return self.object_mgr.space

    def draw(self, screen):
        pass

    def handle_event(self, event):
        pass

    def setup(self, screen=None, **kwargs):
        if screen:
            self.gui_mgr.resize_gui(screen)

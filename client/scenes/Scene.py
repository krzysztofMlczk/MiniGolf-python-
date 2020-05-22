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
        self.object_mgr = ObjectManager(space)
        self.gui_mgr = GUIManager()

    def get_space(self):
        return self.object_mgr.space

    def draw(self, screen):
        pass

    def handle_event(self, event):
        pass

    def setup(self, **kwargs):
        screen = None
        for key, value in kwargs.items():
            if key == "screen":
                screen = value

        if screen:
            self.gui_mgr.resize_gui(screen)

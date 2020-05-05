from client.gui.GUIElement import GUIElement


class Label(GUIElement):
    def __init__(self, name, dimension, position, image):
        super().__init__(position, dimension, image, name)


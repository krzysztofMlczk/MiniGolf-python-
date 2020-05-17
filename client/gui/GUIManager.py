

# Class responsible for holding the list of all GUI elements on the scene
# and updating them. Self registration is enabled by default, that means
# each newly created element is automatically being registered.
class GUIManager:
    def __init__(self):
        self.gui_elements = []

    def register_gui_elem(self, elem):
        self.gui_elements.append(elem)

    def destroy_gui_elem(self, elem):
        if elem not in self.gui_elements:
            return

        self.gui_elements.remove(elem)

    def update_gui(self):
        for elem in self.gui_elements:
            elem.update()

    def draw_gui(self, display):
        for elem in self.gui_elements:
            elem.draw(display)

    def resize_gui(self, display):
        for elem in self.gui_elements:
            elem.on_scr_resize(display)

    def move_to_front(self, elem):
        try:
            index = self.gui_elements.index(elem)
            self.gui_elements[index], self.gui_elements[-1] = self.gui_elements[-1], self.gui_elements[index]
        except ValueError:
            pass

    def move_to_back(self, elem):
        try:
            index = self.gui_elements.index(elem)
            self.gui_elements[index], self.gui_elements[0] = self.gui_elements[0], self.gui_elements[index]
        except ValueError:
            pass

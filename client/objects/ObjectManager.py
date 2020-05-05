

# Class responsible for holding the list of all objects on the scene
# and updating them. Self registration is enabled by default, that means
# each newly created objects is automatically being registered.
class ObjectManager:
    objects = []
    gui_elements = []

    @classmethod
    def register_object(cls, obj):
        cls.objects.append(obj)

    @classmethod
    def destroy_object(cls, obj):
        cls.objects.remove(obj)

    @classmethod
    def register_gui_elem(cls, elem):
        cls.gui_elements.append(elem)

    @classmethod
    def destroy_gui_elem(cls, elem):
        cls.gui_elements.remove(elem)

    @classmethod
    def update_objects(cls, display):
        for obj in cls.objects:
            obj.update(display)

    @classmethod
    def update_gui(cls, display):
        for elem in cls.gui_elements:
            elem.update(display)

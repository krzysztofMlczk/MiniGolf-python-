import pymunk
import pygame


# Class responsible for holding the list of all objects on the scene
# and updating them. Self registration is enabled by default, that means
# each newly created objects is automatically being registered.
class ObjectManager:
    def __init__(self, space, screen):
        self.objects = []
        self.space = space
        self.display = screen

    def register_object(self, obj):
        self.objects.append(obj)

        if obj.shape is not None:
            if obj.shape.body.body_type == pymunk.Body.STATIC:
                self.space.add(obj.shape)
            else:
                self.space.add(obj.shape, obj.shape.body)

    def destroy_object(self, obj):
        if obj not in self.objects:
            return

        self.objects.remove(obj)

        if obj.shape is not None:
            if obj.shape.body.body_type == pymunk.Body.STATIC:
                self.space.remove(obj.shape)
            else:
                self.space.remove(obj.shape, obj.shape.body)

    def destroy_all_objects(self):
        while self.objects:
            self.destroy_object(self.objects[0])

    def update_objects(self):
        for obj in self.objects:
            obj.update()

    def draw_objects(self):
        display = self.display.copy()

        for obj in self.objects:
            obj.draw(display)

        return display

    def draw_static_objects(self):
        display = self.display.copy()

        for obj in self.objects:
            if obj.type == 'static':
                obj.draw(display)

        return display

    def draw_dynamic_objects(self):
        display = self.display.copy()

        for obj in self.objects:
            if obj.type == 'dynamic':
                obj.draw(display)

        return display

    def blit_on_display(self, display):
        self.display = display

    def clear_display(self, fill_color=None):
        if fill_color:
            self.display.fill(fill_color)
        else:
            self.display.fill((0, 0, 0))

    def move_to_front(self, obj):
        try:
            index = self.objects.index(obj)
            self.objects[index], self.objects[-1] = self.objects[-1], self.objects[index]
        except ValueError:
            pass

    def move_to_back(self, obj):
        try:
            index = self.objects.index(obj)
            self.objects[index], self.objects[0] = self.objects[0], self.objects[index]
        except ValueError:
            pass

import pymunk


# Class responsible for holding the list of all objects on the scene
# and updating them. Self registration is enabled by default, that means
# each newly created objects is automatically being registered.
class ObjectManager:
    def __init__(self, space):
        self.objects = []
        self.space = space

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

    def draw_objects(self, display):
        for obj in self.objects:
            obj.draw(display)

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

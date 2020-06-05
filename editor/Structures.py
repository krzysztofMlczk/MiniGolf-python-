import pygame


class Object:
    def __init__(self, image, name, rot, t, horiz=1, vert=1):
        self.image = image
        self.name = name
        self.rotation = rot
        self.horizontal = horiz
        self.vertical = vert
        self.type = t

    def overlap_image(self):
        img = pygame.Surface((self.image.get_width() * self.horizontal,
                              self.image.get_height() * self.vertical))

        for y in range(self.vertical):
            for x in range(self.horizontal):
                img.blit(self.image, (x * self.image.get_width(), y * self.image.get_height()))

        return img


class Button:
    def __init__(self, image, pos):
        self.image = image
        self.pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], image.get_width(), image.get_height())

    def clicked(self, pos):
        return self.rect.collidepoint(*pos)


class ToolIcon:
    def __init__(self, obj, rect):
        self.object = obj
        self.rect = rect


class MapTile:
    def __init__(self, rect, obj):
        self.rect = rect

        self.objects = []
        if obj is not None:
            self.add_object(obj)

    def add_object(self, obj):
        for o in self.objects:
            if o.name == obj.name:
                return
        self.objects.append(obj)

    def remove_object(self, obj):
        for o in self.objects:
            if o.name == obj.name:
                self.objects.remove(o)

    def clear_objects(self):
        self.objects.clear()

    def has_object(self):
        return len(self.objects) > 0

    def rotate_object(self, obj, rot):
        for o in self.objects:
            if o.name == obj.name:
                o.rotation = (o.rotation + rot) % 360

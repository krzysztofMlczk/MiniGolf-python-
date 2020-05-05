import pygame

from client.objects.ObjectManager import ObjectManager


# Base class of all objects on the scene.
class Object(pygame.sprite.Sprite):
    def __init__(self, position, dimension, image, collision=True, noregister=False):
        super().__init__()

        self.image = pygame.transform.scale(image, dimension)
        self.rect = dimension
        self.position = position
        self.collision = collision

        if collision:
            self.mask = pygame.mask.from_surface(self.image)

        # Add newly created objects to the Object Manager, if not mentioned otherwise
        if not noregister:
            ObjectManager.register_object(self)

    def draw(self, screen):
        pass

    def update(self):
        pass

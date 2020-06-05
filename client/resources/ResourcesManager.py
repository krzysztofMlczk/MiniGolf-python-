import os

import pygame


# Here is a class which holds all the resources that we can use and refer to later.
class ResourcesManager:
    images = {}
    coll_masks = {}

    @classmethod
    def load_from_disk(cls):

        for root, dirnames, filenames in os.walk('./client/resources'):
            for filename in filenames:
                if filename.endswith(('.jpg', '.png', '.bmp', '.mp3')):
                    cls.images[os.path.splitext(filename)[0]] =\
                        pygame.image.load(os.path.join(root, filename)).convert_alpha()

    @classmethod
    def get_image(cls, name):
        if name in cls.images.keys():
            return cls.images[name]

        return None

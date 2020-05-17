from time import time

import pygame


class Particles:
    def __init__(self, position, dimension, image_set, frame_interval, obj_mgr=None, follow=None, id=-1):
        self.image_set = []
        self.id = id
        self.object_mgr = obj_mgr
        self.position = position
        self.follow = follow
        self.image_indicator = 0

        # For ObjectManager purposes:
        self.shape = None

        self._anim_time = time()
        self.frame_interval = frame_interval

        for img in image_set:
            self.image_set.append(pygame.transform.scale(img, dimension))

        # Add newly created object to the Object Manager, if not mentioned otherwise
        if obj_mgr is not None:
            obj_mgr.register_object(self)

    def draw(self, display):
        if self.follow is not None:
            pos = self.follow.get_position(pygame=True)
            dim = self.follow.image.get_size()
            self.position = (pos[0] - dim[0] // 2, pos[1] - dim[1] // 2)

        display.blit(self.image_set[self.image_indicator], self.position)

    def update(self):
        now = time()

        if now - self._anim_time > self.frame_interval:
            self.image_indicator += 1

            if self.image_indicator >= len(self.image_set):
                self.image_indicator = 0

            self._anim_time = now

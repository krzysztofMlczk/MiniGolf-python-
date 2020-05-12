import math

import pygame

from client.utils import flipy


class Cup:
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius

        self.color = (0, 0, 0)

    def ball_in(self, pos):
        distance = math.sqrt(((pos.x - self.position.x)**2) + ((pos.y - flipy(self.position.y))**2))
        return distance < self.radius

    def draw(self, screen):
        p = int(self.position.x), int(self.position.y)
        pygame.draw.circle(screen, self.color, p, int(self.radius))

import pygame
import pymunk

from client.utils import flipy


class Wall:
    def __init__(self, space, start, end, width, elasticity, color=(200, 190, 140)):
        self.width = width
        self.color = color

        # TODO
        # Generate body as image mask
        self.body = pymunk.Segment(space.static_body, start, end, width)
        self.body.elasticity = elasticity

        space.add(self.body)

    def draw(self, screen):
        # TODO
        # Draw picture instead of pygame shape
        pv1 = self.body.body.position + self.body.a.rotated(self.body.body.angle)
        pv2 = self.body.body.position + self.body.b.rotated(self.body.body.angle)

        p1 = pv1.x, flipy(pv1.y)
        p2 = pv2.x, flipy(pv2.y)

        pygame.draw.lines(screen, self.color, False, [p1, p2], self.width)

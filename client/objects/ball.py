import math

import pygame
import pymunk
from pymunk import Vec2d

from client.utils import flipy


class Ball:
    def __init__(self, scene, index, position, radius, color=(255, 255, 255)):
        self.body = pymunk.Body(1, pymunk.inf)
        self.body.velocity_func = self.friction_velocity
        self.body.position = position

        self.scene = scene
        self.index = index
        self.radius = radius
        self.color = color

        self.turn = False
        self.stroke = False
        self.moving = False

        # Setting up pymunk body
        shape = pymunk.Circle(self.body, self.radius)
        shape.color = self.color
        shape.elasticity = 1.0

        self.scene.space.add(self.body, shape)

    def friction_velocity(self, body, gravity, damping, dt, friction=0.001):
        pymunk.Body.update_velocity(body, gravity, damping, dt)
        body.velocity *= (1 - friction)

        eps = 5

        if math.fabs(body.velocity.x) < eps and math.fabs(body.velocity.y) < eps and body.velocity != Vec2d(0.0, 0.0):
            body.velocity = Vec2d(0.0, 0.0)
            self.moving = False

    def is_clicked(self, mouse_pos):
        if self.turn:
            distance = math.sqrt(((mouse_pos.x - self.body.position.x)**2) + ((mouse_pos.y - self.body.position.y)**2))
            return distance < self.radius

        else:
            return False

    def draw(self, screen):
        p = int(self.body.position.x), int(flipy(self.body.position.y))
        pygame.draw.circle(screen, self.color, p, int(self.radius))

    def update(self):
        pass

import math

import pygame
import pymunk
from pymunk import Vec2d

from client.enums.ball_state_enum import BallState
from client.utils import flipy, sign


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
        self.state = BallState.NOT_MOVING

        # Setting up pymunk body
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.color = self.color
        self.shape.elasticity = 1.0

        self.scene.space.add(self.body, self.shape)

    def friction_velocity(self, body, gravity, damping, dt, friction=2):
        """Custom velocity function for pymunk body"""
        if self.state is BallState.IN_CUP:
            body.velocity = Vec2d(0.0, 0.0)

        elif body.velocity != Vec2d(0.0, 0.0):
            pymunk.Body.update_velocity(body, gravity, damping, dt)

            # Calculating friction vector
            friction_vec = -friction * body.velocity / math.hypot(body.velocity.x, body.velocity.y)

            # Calculating new velocity with friction
            velocity = body.velocity + friction_vec

            # If friction changed sign than make velocity zero
            if sign(velocity.x) != sign(body.velocity.x):
                velocity.x = 0.0

            if sign(velocity.y) != sign(body.velocity.y):
                velocity.y = 0.0

            # Establish maximum velocity
            max_velocity = 800.0

            if math.fabs(velocity.x) > max_velocity:
                velocity.x = max_velocity * sign(velocity.x)

            if math.fabs(velocity.y) > max_velocity:
                velocity.y = max_velocity * sign(velocity.y)

            body.velocity = velocity

            if body.velocity == Vec2d(0.0, 0.0):
                if self.state is not BallState.CLICKED:
                    self.state = BallState.NOT_MOVING
            else:
                self.state = BallState.MOVING

    def is_clicked(self, mouse_pos):
        """Check if ball was clicked"""
        if self.state is not BallState.IN_CUP:
            distance = math.sqrt(((mouse_pos.x - self.body.position.x)**2) + ((mouse_pos.y - self.body.position.y)**2))
            return distance < self.radius

        return False

    def draw(self, screen):
        """Draw a ball onto the given screen"""
        if self.state is not BallState.IN_CUP:
            p = int(self.body.position.x), int(flipy(self.body.position.y))
            pygame.draw.circle(screen, self.color, p, int(self.radius))

    def update(self):
        pass

import math

import pymunk
from pymunk import Vec2d

from client.objects.Object import Object
from client.objects.Surface import Surface
from client.objects.particles.ParticlesFire import ParticlesFire
from client.resources.ResourcesManager import ResourcesManager
from client.enums.ball_state_enum import BallState
from client.utils import sign


class Ball(Object):
    def __init__(self, position, dimension, obj_mgr, color):
        image = ResourcesManager.get_image('obj_ball_' + color)
        self.radius = dimension[0] / 2

        super().__init__(position, dimension, image, obj_mgr=obj_mgr, name='ball', obj_type='dynamic')

        self.turn = False
        self.state = BallState.NOT_MOVING
        self.last_pos = self.get_position()

        self.particles_effect = None

    def friction_velocity(self, body, gravity, damping, dt, default_friction=6):
        """Custom velocity function for pymunk body"""
        if self.state is BallState.IN_CUP:
            body.velocity = Vec2d(0.0, 0.0)

        elif body.velocity != Vec2d(0.0, 0.0):
            pymunk.Body.update_velocity(body, gravity, damping, dt)

            surf = self.get_surface()

            if surf is not None and surf.name == 'lava' and self.particles_effect is None:
                self.particles_effect = ParticlesFire(None, (32, 32), follow=self, obj_mgr=self.object_mgr)

            if surf is not None:
                # Let the surface change the velocity:
                velocity = surf.velocity_func(body.velocity, surf.friction)
            else:
                # Calculating friction vector
                friction_vec = -default_friction * body.velocity / math.hypot(body.velocity.x, body.velocity.y)

                # Calculating new velocity with friction
                velocity = body.velocity + friction_vec

            # If friction changed sign than make velocity zero
            if sign(velocity.x) != sign(body.velocity.x):
                velocity.x = 0.0

            if sign(velocity.y) != sign(body.velocity.y):
                velocity.y = 0.0

            body.velocity = velocity

            if body.velocity == Vec2d(0.0, 0.0):
                if self.state is not BallState.CLICKED:
                    if self.get_surface() is not None and self.get_surface().name == 'lava':
                        self.shape.body.position = self.last_pos

                    self.state = BallState.NOT_MOVING
                    self.last_pos = self.get_position()
                    
                    self.object_mgr.destroy_object(self.particles_effect)
                    self.particles_effect = None
            else:
                self.state = BallState.MOVING

    def is_clicked(self, mouse_pos):
        """Check if ball was clicked"""
        if self.state is not BallState.IN_CUP:
            distance = math.sqrt(((mouse_pos[0] - self.shape.body.position[0])**2)
                                 + ((mouse_pos[1] - self.shape.body.position[1])**2))
            return distance < self.radius

        return False

    def get_center(self):
        pos = self.get_position(pygame=True)
        return pos[0] - self.image.get_width() / 2, pos[1] - self.image.get_height() / 2

    def prepare_body(self, position):
        body = pymunk.Body(1, pymunk.inf)
        body.velocity_func = self.friction_velocity
        body.position = position

        # Setting up pymunk body
        shape = pymunk.Circle(body, self.radius)
        shape.elasticity = 1.0

        # Collision type for ball objects is 1
        shape.collision_type = 1

        return shape

    def draw(self, display):
        """Draw a ball onto the given screen"""
        if self.state is not BallState.IN_CUP:
            display.blit(self.image, self.get_center())

    def update(self):
        pass

    def get_surface(self):
        for obj in self.object_mgr.objects:
            if isinstance(obj, Surface):
                if obj.get_rect().collidepoint(self.get_position(pygame=True)):
                    return obj
        return None

import pygame
import pymunk
from pymunk import Vec2d

from client.utils import flip_coords
from client.maps.Map import Map
from client.scenes.Scene import Scene
from client.enums.ball_state_enum import BallState


# This is the scene that represents each single level:
class GameScene(Scene):
    """Scene for drawing and handling game events"""
    def __init__(self):
        super().__init__(pymunk.Space())
        self.next = None
        self.map = None
        self.players = None

        # We need a custom collision handler for ball here:
        # self.object_mgr.space.add_collision_handler(1, 2).pre_solve = self.ball_in_cup

        self.trajectory = None
        self.next_turn = None

        # self.map.balls[0].turn = None

    def draw(self, screen):
        """Draw scene and change ball if required"""

        # Draw balls
        for ball in self.map.balls:
            ball.draw(screen)

        # Draw trajectory when aiming
        if self.trajectory:
            pygame.draw.lines(screen, (255, 0, 230), False, self.trajectory, 2)

        # Switch turn
        if self.balls_not_moving():
            if self.next_turn or self.current_ball().state is BallState.IN_CUP:
                self.next_ball()

        self.object_mgr.update_objects()
        self.object_mgr.draw_objects(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                # Find ball that was clicked if none than omit
                event_pos = flip_coords(event.pos)
                ball = self.clicked_ball(Vec2d(event_pos[0], event_pos[1]))

                if ball:
                    # If its ball's turn and all balls are still, let the ball be clicked to hit
                    if ball.turn and self.balls_not_moving():
                        pos = ball.shape.body.position
                        self.trajectory = [flip_coords(pos), flip_coords(pos)]
                        ball.state = BallState.CLICKED

        elif event.type == pygame.MOUSEBUTTONUP:
            # Get current ball
            ball = self.current_ball()

            if ball.state is BallState.CLICKED:
                self.trajectory = None

                if event.button == pygame.BUTTON_LEFT:
                    direction = 5*Vec2d(
                        ball.shape.body.position.x - flip_coords(event.pos)[0],
                        ball.shape.body.position.y - flip_coords(event.pos)[1]
                    )
                    ball.shape.body.apply_impulse_at_local_point(direction)
                    self.next_turn = True
                else:
                    ball.state = BallState.NOT_MOVING

        elif event.type == pygame.MOUSEMOTION:
            if self.trajectory:
                self.trajectory[1] = pygame.mouse.get_pos()

    def remove(self, ball):
        """Removing ball from space"""
        ball.state = BallState.IN_CUP
        self.object_mgr.destroy_object(ball)

    def clicked_ball(self, pos):
        """Get clicked ball, only if its turn"""
        for ball in self.map.balls:
            if ball.is_clicked(pos) and ball.turn:
                return ball

        return None

    def current_ball(self):
        """Get current ball to strike"""
        ball = [ball for ball in self.map.balls if ball.turn]
        return ball[0]

    def next_ball(self):
        """Change turn for next ball"""
        current_ball = self.current_ball()
        current_ball.turn = False

        # Choose next player
        tries = len(self.map.balls)
        next_id = (self.map.balls.index(current_ball) + 1) % len(self.map.balls)

        while self.map.balls[next_id].state is BallState.IN_CUP and tries > 0:
            next_id = (next_id + 1) % len(self.map.balls)
            tries -= 1

        if tries > 0:
            self.map.balls[next_id].turn = True
            self.next_turn = False
            print("Player {} to move".format(next_id))

        # If all players ended, load next map
        else:
            print("Next map")
            self.next_map()

    def next_map(self):
        """Switch to next map"""

        # Clean the map:
        self.object_mgr.destroy_all_objects()

        # Currently showing the same map again
        self.map = Map(self.players, self.object_mgr)

        # Resetting balls and adding them back to simulation space
        for i, ball in enumerate(self.map.balls):
            ball.state = BallState.NOT_MOVING
            ball.shape.body.position = Vec2d(300, 540 + 10 * i)
            ball.shape.body.velocity = Vec2d(0.0, 0.0)

        self.next_turn = False

        # Setting up first player
        self.map.balls[0].turn = True
        print("Player 0 to move")

    def balls_not_moving(self):
        """Check if all balls are still"""
        for ball in self.map.balls:
            if ball.state is BallState.MOVING or ball.state is BallState.CLICKED:
                return False

        return True

    def ball_in_cup(self, arbiter, space, data):
        for ball in self.map.balls:
            if self.map.cup.ball_in(ball.shape.body.position) and ball.state is not BallState.IN_CUP:
                print("Ball {} in a cup".format(ball.id))
                self.remove(ball)

        # We ignore the collision:
        return False

    def setup(self, players=None, **kwargs):
        self.next = None
        self.map = Map(players, self.object_mgr)
        self.players = players

        # We need a custom collision handler for ball here:
        self.object_mgr.space.add_collision_handler(1, 2).pre_solve = self.ball_in_cup

        self.trajectory = None
        self.next_turn = False

        self.map.balls[0].turn = True
        print("Player 0 to move")

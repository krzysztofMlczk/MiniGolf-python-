import pygame
import pymunk
from pymunk import Vec2d

from client.utils import flipy
from client.maps.map import Map
from client.objects.ball import Ball
from client.scenes.scene import Scene
from client.enums.ball_state_enum import BallState


class GameScene(Scene):
    """Scene for drawing and handling game events"""
    def __init__(self, player):
        self.space = pymunk.Space()
        self.color = (0, 50, 0)
        self.map = Map(1, self.space)
        self.balls = [
            Ball(self, i, Vec2d(300, 540 + 10*i), 10, color=color)
            for i, color in enumerate(player)
        ]

        self.trajectory = None
        self.next_turn = False

        self.balls[0].turn = True
        print("Player 0 to move")

    def draw(self, screen):
        """Draw scene and change ball if required"""

        # Draw map
        self.map.draw(screen)

        # Draw balls and check if in a cup
        for ball in self.balls:
            if self.map.cup.ball_in(ball.body.position) and ball.state is not BallState.IN_CUP:
                print("Ball {} in a cup".format(ball.index))
                self.remove(ball)

            ball.draw(screen)

        # Draw trajectory when aiming
        if self.trajectory:
            pygame.draw.lines(screen, (255, 0, 230), False, self.trajectory, 2)

        # Switch turn
        if self.balls_not_moving():
            if self.next_turn or self.current_ball().state is BallState.IN_CUP:
                self.next_ball()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                # Find ball that was clicked if none than omit
                ball = self.clicked_ball(Vec2d(event.pos[0], flipy(event.pos[1])))

                if ball:
                    # If its ball's turn and all balls are still, let the ball be clicked to hit
                    if ball.turn and self.balls_not_moving():
                        pos = ball.body.position
                        self.trajectory = [(pos.x, flipy(pos.y)), (pos.x, flipy(pos.y))]
                        ball.state = BallState.CLICKED

        elif event.type == pygame.MOUSEBUTTONUP:
            # Get current ball
            ball = self.current_ball()

            if ball.state is BallState.CLICKED:
                self.trajectory = None

                if event.button == pygame.BUTTON_LEFT:
                    direction = 5*Vec2d(
                        ball.body.position.x - event.pos[0],
                        ball.body.position.y - flipy(event.pos[1])
                    )
                    ball.body.apply_impulse_at_local_point(direction)
                    self.next_turn = True
                else:
                    ball.state = BallState.NOT_MOVING

        elif event.type == pygame.MOUSEMOTION:
            if self.trajectory:
                self.trajectory[1] = pygame.mouse.get_pos()

    def remove(self, ball):
        """Removing ball from space"""
        ball.state = BallState.IN_CUP
        self.space.remove(ball.shape, ball.body)

    def clicked_ball(self, pos):
        """Get clicked ball, only if its turn"""
        for ball in self.balls:
            if ball.is_clicked(pos) and ball.turn:
                return ball

        return None

    def current_ball(self):
        """Get current ball to strike"""
        ball = [ball for ball in self.balls if ball.turn]
        return ball[0]

    def next_ball(self):
        """Change turn for next ball"""
        current_ball = self.current_ball()
        current_ball.turn = False

        # Choose next player
        tries = len(self.balls)
        next_id = (self.balls.index(current_ball) + 1) % len(self.balls)

        while self.balls[next_id].state is BallState.IN_CUP and tries > 0:
            next_id = (next_id + 1) % len(self.balls)
            tries -= 1

        if tries > 0:
            self.balls[next_id].turn = True
            self.next_turn = False
            print("Player {} to move".format(next_id))

        # If all players ended, load next map
        else:
            print("Next map")
            self.next_map()

    def next_map(self):
        """Switch to next map"""

        # Currently showing the same map again
        self.map = Map(1, self.space)

        # Resetting balls and adding them back to simulation space
        for i, ball in enumerate(self.balls):
            ball.state = BallState.NOT_MOVING
            ball.body.position = Vec2d(300, 540 + 10 * i)
            ball.body.velocity = Vec2d(0.0, 0.0)
            self.space.add(ball.shape, ball.body)

        self.next_turn = False

        # Setting up first player
        self.balls[0].turn = True
        print("Player 0 to move")

    def balls_not_moving(self):
        """Check if all balls are still"""
        for ball in self.balls:
            if ball.state is BallState.MOVING or ball.state is BallState.CLICKED:
                return False

        return True

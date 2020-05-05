import pygame
import pymunk
from pymunk import Vec2d

from client.utils import flipy
from client.maps.map import Map
from client.objects.ball import Ball
from client.scenes.scene import Scene


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

        self.balls[0].turn = True
        print("Player 0 to move")

    def draw(self, screen):
        self.map.draw(screen)

        for ball in self.balls:
            ball.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                # Find ball that was clicked if none than omit
                ball = self.clicked_ball(Vec2d(event.pos[0], flipy(event.pos[1])))

                if ball:
                    if ball.turn and not ball.stroke and not ball.moving:
                        ball.stroke = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                # Get current ball if none than omit
                ball = self.current_ball()

                if ball:
                    ball.stroke = False
                    ball.moving = True
                    direction = 5*Vec2d(
                        ball.body.position.x - event.pos[0],
                        ball.body.position.y - flipy(event.pos[1])
                    )
                    ball.body.apply_impulse_at_local_point(direction)

    def clicked_ball(self, pos):
        for ball in self.balls:
            if ball.is_clicked(pos):
                return ball

        return None

    def current_ball(self):
        ball = [ball for ball in self.balls if ball.turn is True and ball.stroke is True]
        return None if len(ball) <= 0 else ball[0]

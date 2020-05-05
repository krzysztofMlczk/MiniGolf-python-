import math

import pygame
from pygame.locals import *

from client.gui.Button import Button
from client.objects.ObjectManager import ObjectManager
from client.objects.ObjectBall import Ball


# Class responsible for input handling.
class EventReceiver:
    start = (-1, -1)

    @classmethod
    def handle_events(cls):
        for event in pygame.event.get():
            cls.handle_gui_events(event)

            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    cls.clicked_ball(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == pygame.BUTTON_LEFT and cls.start != (-1, -1):
                    cls.released(event)
            elif event.type == VIDEORESIZE:
                pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        return True

    @classmethod
    def clicked_ball(cls, event):
        for obj in ObjectManager.objects:
            if isinstance(obj, Ball):
                x = obj.get_center()
                y = event.pos
                if math.sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2) < obj.radius:
                    cls.click(obj)

    @classmethod
    def click(cls, ball):
        cls.start = ball.get_position()
        cls.ball = ball

    @classmethod
    def released(cls, event):
        vec = (cls.start[0] - event.pos[0], cls.start[1] - event.pos[1])
        cls.ball.strike(vec)
        cls.start = (-1, -1)
        cls.ball = None

    # TODO
    # GUI event handlers to be added to main menu scene
    @classmethod
    def handle_gui_events(cls, event):
        for elem in ObjectManager.gui_elements:
            # Buttons:
            if isinstance(elem, Button):
                if elem.get_rect().collidepoint(pygame.mouse.get_pos()):
                    # Mouse click:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        elem.on_mouse_clicked()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        elem.on_mouse_released()
                    else:
                        elem.on_mouse_enter()
                else:
                    elem.on_mouse_quit()

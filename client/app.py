import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util

from client.scenes.game_scene import GameScene


class App:
    """Creating single window app with multiple scenes"""
    scenes = []
    current = None

    def __init__(self):

        # Setting up pygame
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 900))
        self.running = True

        # Setting up pymunk
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.dt = 1/50
        self.stepping = True

        # Setting up constant players
        players = [(255, 255, 255)]

        # Setting up scenes and choosing first
        App.scenes.append(GameScene(players))
        App.current = App.scenes[0]

    def run(self):
        """Main app loop"""
        while self.running:

            # Delegating event handling to current scene
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False

                App.current.handle_event(event)

            # Removing shapes from space
            for s in App.current.space.shapes:
                if s.body.position.y < -100:
                    App.current.space.remove(s)

            # Drawing updated scene
            self.draw()

            # Processing step in simulation
            if self.stepping:
                App.current.space.step(self.dt)

        pygame.quit()

    def draw(self):
        """Delegating updating a scene to a current scene"""
        self.screen.fill(App.current.color)

        # To turn on debug mode on pure simulation underneath
        # uncomment line below and comment one after
        # App.current.space.debug_draw(self.draw_options)

        App.current.draw(self.screen)
        pygame.display.flip()


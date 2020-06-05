import pygame
import pymunk
from pymunk import Vec2d

from client.models.scene_init import SceneInit
from client.utils import flip_coords
from client.maps.Map import Map
from client.scenes.Scene import Scene
from client.enums.ball_state_enum import BallState
from client.objects.Ball import Ball
from client.maps.map_loader import Loader
from client.maps.map_search import map_search
from client.resources.ResourcesManager import ResourcesManager


class GameScene(Scene):
    """Scene for drawing and handling game events"""

    def __init__(self):
        super().__init__(pymunk.Space())
        self.background_color = (0, 0, 0)
        self.scoreboards = dict()
        self.loader = Loader(self.object_mgr)
        self.next = None
        self.map = None
        self.players = None
        self.trajectory = None
        self.next_turn = None
        self.change_scene = None
        self.font = pygame.font.SysFont("monospace", 48)

    def draw(self, screen):
        """Draw scene and change ball if required"""

        # Switch turn
        if self.balls_not_moving():
            if self.next_turn or self.current_player().ball.state is BallState.IN_CUP:
                self.next_player()

        # Update map and draw it
        self.object_mgr.update_objects()

        screen.blit(self.object_mgr.draw_dynamic_objects(), (0, 0))

        # Draw trajectory when aiming
        if self.trajectory:
            pygame.draw.lines(screen, (255, 0, 230), False, self.trajectory, 2)

    def handle_event(self, event):
        """Handling specific scene events"""

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

            # Get current player
            player = self.current_player()

            if player.ball.state is BallState.CLICKED:
                self.trajectory = None

                if event.button == pygame.BUTTON_LEFT:

                    direction = 10*Vec2d(
                        player.ball.shape.body.position.x - flip_coords(event.pos)[0],
                        player.ball.shape.body.position.y - flip_coords(event.pos)[1]
                    )

                    player.ball.shape.body.apply_impulse_at_local_point(direction)
                    self.next_turn = True

                    # Adding points
                    if str(self.map.id) in player.points.keys():
                        player.points[str(self.map.id)] += 1
                    else:
                        player.points[str(self.map.id)] = 1
                    self.show_score()

                else:
                    player.ball.state = BallState.NOT_MOVING

        elif event.type == pygame.MOUSEMOTION and self.trajectory:
            self.trajectory[1] = pygame.mouse.get_pos()

    def remove(self, ball):
        """Removing ball from space"""
        ball.state = BallState.IN_CUP
        self.object_mgr.destroy_object(ball)

    def clicked_ball(self, pos):
        """Get clicked ball, only if its turn"""
        for player in self.players:
            if player.ball.is_clicked(pos) and player.ball.turn:
                return player.ball

        return None

    def current_player(self):
        """Get current player to strike"""
        player = [player for player in self.players if player.ball.turn]
        return player[0]

    def next_player(self):
        """Change turn for next player"""
        current_player = self.current_player()
        current_player.ball.turn = False

        # Choose next player
        tries = len(self.players)
        next_id = (self.players.index(current_player) + 1) % len(self.players)

        while self.players[next_id].ball.state is BallState.IN_CUP and tries > 0:
            next_id = (next_id + 1) % len(self.players)
            tries -= 1

        if tries > 0:
            self.players[next_id].ball.turn = True
            self.next_turn = False
            print("Player {} to move".format(next_id))
        # If all players ended, load next map
        else:
            print("Next map")
            self.next_map()
        self.show_score()

    def next_map(self):
        """Switch to next map"""

        # Clean the map:
        self.object_mgr.destroy_all_objects()

        # Currently showing the same map again
        # self.map = Map(self.players, self.object_mgr)
        next_map_details = self.loader.next_map()
        if next_map_details:
            self.map = Map(*next_map_details[0:2])
        else:
            self.change_scene = SceneInit("Score", players=self.players)
            return

        # Resetting balls and adding them back to simulation space
        for player in self.players:
            player.ball.state = BallState.NOT_MOVING
            player.ball.shape.body.position = Vec2d(next_map_details[2])
            player.ball.shape.body.velocity = Vec2d(0.0, 0.0)
            self.object_mgr.register_object(player.ball)
            print("Player {} points: {}".format(player.id, player.points))

        self.next_turn = False

        # Setting up first player
        self.players[0].ball.turn = True
        print("Player 0 to move")

        self.show_score()

        self.object_mgr.blit_on_display(self.object_mgr.draw_static_object())

    def balls_not_moving(self):
        """Check if all balls are still"""
        for player in self.players:
            if player.ball.state is BallState.MOVING or player.ball.state is BallState.CLICKED:
                return False

        return True

    def ball_in_cup(self, arbiter, space, data):
        for player in self.players:
            if self.map.cup.ball_in(player.ball.shape.body.position) and player.ball.state is not BallState.IN_CUP:
                print("Ball {} in a cup".format(player.id))
                self.remove(player.ball)

        # We ignore the collision:
        return False

    def setup(self, players=None, maps_to_play=None, **kwargs):
        self.players = players
        self.search_for_maps(maps_to_play)
        map_details = self.loader.next_map()
        self.map = Map(*map_details[0:2])

        for player in self.players:
            player.ball = Ball((map_details[2]), (32, 32), color=player.color, obj_mgr=self.object_mgr)

        # We need a custom collision handler for ball here:
        self.object_mgr.space.add_collision_handler(1, 2).pre_solve = self.ball_in_cup

        self.trajectory = None
        self.next_turn = False

        self.players[0].ball.turn = True
        print("Player 0 to move")
        self.show_score()
        self.object_mgr.blit_on_display(self.object_mgr.draw_static_object())

    def search_for_maps(self, count):
        levels = map_search('./client/levels')
        for lvl in levels:
            if 0 < count:
                self.loader.add_map_file(lvl)
                count -= 0

    def show_score(self):
        text = 'level: ' + str(self.map.id) + '     score:  '
        label = self.font.render(text, 1, (255, 255, 255), (0, 0, 0))
        self.object_mgr.display.blit(label, (96, 4))
        offset = 664
        for player in self.players:
            if player.ball.turn:
                pygame.draw.rect(self.object_mgr.display, (240, 50, 50), (offset-2, 2, 60, 60), 2)
            else:
                pygame.draw.rect(self.object_mgr.display, self.background_color, (offset-2, 2, 60, 60), 2)
            ball_img = ResourcesManager.get_image('obj_ball_' + player.color)
            ball_img = pygame.transform.scale(ball_img, (56, 56))
            self.object_mgr.display.blit(ball_img, (offset, 4))
            label = self.font.render(str(sum(v for k, v in player.points.items())), 1, (0, 0, 0))
            label = pygame.transform.scale(label, (48, 56))
            self.object_mgr.display.blit(label, (offset+4, 4))
            offset += 70

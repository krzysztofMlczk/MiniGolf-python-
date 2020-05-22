import pygame
import random

from client.gui.Label import Label
from client.models.scene_init import SceneInit
from client.scenes.Scene import Scene
from client.gui.Cloud import Cloud
from client.gui.Button import Button
from client.resources.ResourcesManager import ResourcesManager
from client.models.player import Player


class MultiSetupScene(Scene):
    """Scene for drawing scene for setting up multiplayer game"""

    available_colors = ["yellow", "orange", "blue", "pink", "white"]
    available_players_id = [0, 1, 2, 3, 4]

    def __init__(self, screen):
        super().__init__(None)
        self.change_scene = None
        self.setup_components()
        self.players_amount = 2
        self.maps_to_play = 1
        self.players = []
        # we have 2 players by default
        self.add_player()
        self.add_player()

        self.gui_mgr.resize_gui(screen)

    def setup_components(self):
        """Setting up and registering (happens automatically) components"""
        width, height = 1920, 1080

        # Setup up background, title and clouds
        background = Label(
            name="background",
            dimension=(width, height),
            position=(0, 0),
            image=ResourcesManager.get_image("background"),
            obj_mgr=self.gui_mgr,
            default_res=(width, height)
        )

        left_cloud = Cloud(
            position=(92, 175),
            dimension=(595, 259),
            height_coefficient=(176 / 1080),
            width_coefficient=(186 / 1920),
            image=ResourcesManager.get_image("left_cloud"),
            name="left_cloud",
            move_dir="right",
            obj_mgr=self.gui_mgr,
            default_res=(width, height)
        )

        right_cloud = Cloud(
            position=(1392, 66),
            dimension=(476, 207),
            height_coefficient=(66 / 1080),
            width_coefficient=(1052 / 1920),
            image=ResourcesManager.get_image("right_cloud"),
            name="right_cloud",
            move_dir="left",
            obj_mgr=self.gui_mgr,
            default_res=(width, height)
        )

        title = Label(
            name="title",
            dimension=(width, height),
            position=(0, 0),
            image=ResourcesManager.get_image("title"),
            obj_mgr=self.gui_mgr,
            default_res=(width, height)
        )

        # setup labels
        etiquette_size = (416, 100)
        numbers_size = (100, 100)

        # label which displays title "Players: "
        players_label = Label(
            name="players_label",
            dimension=etiquette_size,
            position=(702, 467),
            image=ResourcesManager.get_image("players_label"),
            obj_mgr=self.gui_mgr,
            default_res=(width, height)
        )

        # label which displays title "Maps: "
        maps_label = Label(
            name="maps_label",
            dimension=etiquette_size,
            position=(702, 617),
            image=ResourcesManager.get_image("maps_label"),
            obj_mgr=self.gui_mgr,
            default_res=(width, height)
        )

        # label which displays amount of players
        players_amount = Label(
            name="players_amount",
            dimension=numbers_size,
            position=(1118, 467),
            # we start off with 2 players and maksimum of 5 players
            image=ResourcesManager.get_image("amount_2"),
            obj_mgr=self.gui_mgr,
            default_res=(width, height)
        )

        # label which displays amount of maps to be played
        maps_amount = Label(
            name="maps_amount",
            dimension=numbers_size,
            position=(1118, 617),
            # we play 1 map by default on multiplayer mode
            image=ResourcesManager.get_image("amount_1"),
            obj_mgr=self.gui_mgr,
            default_res=(width, height)
        )

        # setup buttons
        up_down_btn_size = (50, 50)
        # buttons for players amount
        players_up = Button(
            name="players_up",
            dimension=up_down_btn_size,
            position=(1218, 467),
            image=ResourcesManager.get_image("btn_up"),
            image_hover=ResourcesManager.get_image("btn_up_hover"),
            obj_mgr=self.gui_mgr,
            default_res=(width, height)
        )

        players_down = Button(
            name="players_down",
            dimension=up_down_btn_size,
            position=(1218, 517),
            image=ResourcesManager.get_image("btn_down"),
            image_hover=ResourcesManager.get_image("btn_down_hover"),
            obj_mgr=self.gui_mgr,
            default_res=(width, height)
        )

        # buttons for maps amount
        maps_up = Button(
            name="maps_up",
            dimension=up_down_btn_size,
            position=(1218, 617),
            image=ResourcesManager.get_image("btn_up"),
            image_hover=ResourcesManager.get_image("btn_up_hover"),
            obj_mgr=self.gui_mgr,
            default_res=(width, height)
        )

        maps_down = Button(
            name="maps_down",
            dimension=up_down_btn_size,
            position=(1218, 667),
            image=ResourcesManager.get_image("btn_down"),
            image_hover=ResourcesManager.get_image("btn_down_hover"),
            obj_mgr=self.gui_mgr,
            default_res=(width, height)
        )
        # setup lower buttons
        lower_button_size = (268, 100)

        play_btn = Button(
            name="play_btn",
            dimension=lower_button_size,
            position=(1000, 767),
            image=ResourcesManager.get_image("btn_play"),
            image_hover=ResourcesManager.get_image("btn_play_hover"),
            obj_mgr=self.gui_mgr,
            default_res=(width, height)
        )

        cancel_btn = Button(
            name="cancel_btn",
            dimension=lower_button_size,
            position=(702, 767),
            image=ResourcesManager.get_image("btn_cancel"),
            image_hover=ResourcesManager.get_image("btn_cancel_hover"),
            obj_mgr=self.gui_mgr,
            default_res=(width, height)
        )

    def handle_event(self, event):
        for elem in self.gui_mgr.gui_elements:

            # Buttons:
            if isinstance(elem, Button):
                if elem.get_rect().collidepoint(pygame.mouse.get_pos()):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        elem.on_mouse_clicked()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        outcome = elem.on_mouse_released(self.players)
                        if isinstance(outcome, SceneInit):
                            self.change_scene = outcome
                        elif isinstance(outcome, int):
                            if elem.name == "players_up" and self.players_amount < 5:
                                self.players_amount += outcome
                                self.add_player()
                            elif elem.name == "players_down" and self.players_amount > 2:
                                self.players_amount += outcome
                                self.remove_player()
                            elif elem.name == "maps_up" and self.maps_to_play < 5:
                                self.maps_to_play += 1
                            elif elem.name == "maps_down" and self.maps_to_play > 1:
                                self.maps_to_play -= 1
                    else:
                        elem.on_mouse_enter()
                else:
                    elem.on_mouse_quit()

    def draw(self, screen):
        self.update_images()
        self.gui_mgr.update_gui()
        self.gui_mgr.draw_gui(screen)

    def add_player(self):
        player_id = self.available_players_id.pop(0)
        color = random.choice(self.available_colors)
        self.available_colors.remove(color)
        self.players.append(Player(player_id, color))

    def remove_player(self):
        # always remove latest added player
        to_remove = self.players.pop()
        self.available_players_id.append(to_remove.id)
        self.available_colors.append(to_remove.color)

    def update_images(self):
        """function to change numbers while clicking on up/down buttons"""
        for element in self.gui_mgr.gui_elements:
            if isinstance(element, Label):

                if element.name == "players_amount":
                    new_image = ResourcesManager.get_image("amount_" + str(self.players_amount))
                    element.set_image_original(new_image)
                    element.set_size(element.get_size())

                elif element.name == "maps_amount":
                    new_image = ResourcesManager.get_image("amount_" + str(self.maps_to_play))
                    element.set_image_original(new_image)
                    element.set_size(element.get_size())




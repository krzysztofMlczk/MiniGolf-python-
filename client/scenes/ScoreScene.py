import pygame

from client.gui.Button import Button
from client.scenes.Scene import Scene
from client.gui.Label import Label
from client.resources.ResourcesManager import ResourcesManager
from client.gui.Cloud import Cloud


class ScoreScene(Scene):
    def __init__(self, screen, players=None):
        super().__init__(None)
        self.change_scene = None
        self.setup_components()
        self.gui_mgr.resize_gui(screen)
        self.font = pygame.font.SysFont("Arial", 60)

    def setup_components(self):
        """Setting up and registering(happens automatically) components"""
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

        # setup score label
        score = Label(
            name="score",
            dimension=(500, 500),
            position=(750, 450),
            image=ResourcesManager.get_image("score_window"),
            obj_mgr=self.gui_mgr,
            default_res=(width, height)
        )

        # setup buttons
        cancel_btn = Button(
            name="cancel_btn",
            dimension=(134, 50),
            position=(933, 970),
            image=ResourcesManager.get_image("btn_cancel"),
            image_hover=ResourcesManager.get_image("btn_cancel_hover"),
            obj_mgr=self.gui_mgr,
            default_res=(width, height)
        )

    def setup(self, players=None, **kwargs):
        super().setup(**kwargs)
        self.set_scores(players)

    def handle_event(self, event):
        for elem in self.gui_mgr.gui_elements:

            # Buttons:
            if isinstance(elem, Button):
                if elem.get_rect().collidepoint(pygame.mouse.get_pos()):

                    # Mouse click:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        elem.on_mouse_clicked()
                    elif event.type == pygame.MOUSEBUTTONUP:
                        self.change_scene = elem.on_mouse_released()
                    else:
                        elem.on_mouse_enter()
                else:
                    elem.on_mouse_quit()

    def draw(self, screen):
        # self.gui_mgr.resize_gui(screen)
        self.gui_mgr.update_gui()
        self.gui_mgr.draw_gui(screen)

    def set_scores(self, players):
        colors = ["white", "blue", "orange", "pink", "yellow"]
        # color.index(color)

        starting_x = 750 + 129 - 12
        starting_y = 450 + 223 - 12
        x_shift = 65
        y_shift = 56
        for color in colors:
            player = self.find_player(color, players)
            score = {}
            if player:
                score = player.points

            for i in range(1, 6):
                if str(i) not in score.keys():
                    score[str(i)] = "-"

            score_items = sorted(score.items())

            for map_id, points in score_items:

                Label(
                    name="player_label",
                    dimension=(24, 24),
                    position=(starting_x + colors.index(color) * x_shift, starting_y + (int(map_id) - 1) * y_shift),
                    image=self.font.render(str(points), 1, (255, 255, 255)),
                    obj_mgr=self.gui_mgr,
                    default_res=(1920, 1080)
                )

    def find_player(self, color, players):
        for player in players:
            if player.color == color:
                return player
        return None

import pygame
from pygame.locals import *

from client.resources.ResourcesManager import ResourcesManager
from client.event.EventReceiver import EventReceiver
from client.objects.Object import ObjectManager
from client.gui.Button import Button
from client.gui.Label import Label
from client.gui.Cloud import Cloud

# Screen resolution
width, height = 1920, 1080

ResourcesManager.load_from_disk()

# Setting up background, title and clouds
background = Label(
    name="background",
    dimension=(width, height),
    position=(0, 0),
    image=ResourcesManager.get_image("background")
)

left_cloud = Cloud(
    position=(92, 175),
    dimension=(595, 259),
    height_coefficient=(176 / 1080),
    width_coefficient=(186 / 1920),
    image=ResourcesManager.get_image("left_cloud"),
    name="left_cloud",
    move_dir="right"
)

right_cloud = Cloud(
    position=(1392, 66),
    dimension=(476, 207),
    height_coefficient=(66 / 1080),
    width_coefficient=(1052 / 1920),
    image=ResourcesManager.get_image("right_cloud"),
    name="right_cloud",
    move_dir="left"
)

title = Label(
    name="title",
    dimension=(width, height),
    position=(0, 0),
    image=ResourcesManager.get_image("title")
)

# Setting up buttons
button_names = ["single", "multi", "options", "about"]
button_size = (416, 98)
offset = 30

for i, name in enumerate(button_names):
    Button(
        name, button_size,
        ((width - button_size[0])//2 + offset, height//2 + button_size[1]*(i-1) + offset),
        ResourcesManager.get_image(name),
        ResourcesManager.get_image(name + "_hover")
    )

# Setting up pygame
pygame.init()
# gameDisplay = pygame.display.set_mode((width, height), FULLSCREEN | HWSURFACE | DOUBLEBUF)
gameDisplay = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption('Mini Golf')

clock = pygame.time.Clock()
run = True

# Main menu event handler loop
while run:
    run = EventReceiver.handle_events()
    ObjectManager.update_objects(gameDisplay)
    ObjectManager.update_gui(gameDisplay)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()

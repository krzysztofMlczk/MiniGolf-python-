import pygame

pygame.init()

gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Mini Golf')

# Clock keeping track of time, to be used with FPS
clock = pygame.time.Clock()

# Crashed flag, telling us if game loop should end
crashed = False

# Game loop
while not crashed:

    # Loop over logged events, once that happened
    for event in pygame.event.get():
        # If quit window event happened than break the game loop
        if event.type == pygame.QUIT:
            crashed = True

        print(event)

    # Updating the entire surface of window.
    # Note that, calling update with no parameters is equal to calling flip.
    # Calling update with parameter lets updating specific areas of screen
    pygame.display.update()

    # How many frames per second are being run: 60 FPS
    clock.tick(60)

# End of pygame instance
pygame.quit()

# Exit python application
quit()

import pygame
from pygame.constants import QUIT

# Initialize pygame
pygame.init()

# Set the frames per second
FPS = pygame.time.Clock()

# Set the dimensions of the display window
HEIGHT = 800
WIDTH = 1200

# Define color constants
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

# Define the size of the player
PLAYER_SIZE = (50, 50)

# Create the main display window
main_display = pygame.display.set_mode((WIDTH, HEIGHT))

# Create the player surface
player = pygame.Surface(PLAYER_SIZE)
player.fill(COLOR_WHITE)
player_rect = player.get_rect()
player_rect.center = (WIDTH // 2, HEIGHT // 3)

# Set the player speed
player_speed = [1, 1]

# Variable to control the game loop
playing = True

while playing:
    # Limit the frames per second
    FPS.tick(320)

    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        
    # Clear the screen
    main_display.fill(COLOR_BLACK)

    # Reverse player direction if it reaches the screen boundaries
    if player_rect.bottom >= HEIGHT or player_rect.top <= 0:
        player_speed[1] = -player_speed[1]

    if player_rect.right >= WIDTH or player_rect.left <= 0:
        player_speed[0] = -player_speed[0]

    # Draw the player
    main_display.blit(player, player_rect)

    # Move the player
    player_rect = player_rect.move(player_speed)

    # Update the display
    pygame.display.flip()

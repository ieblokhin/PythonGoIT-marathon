import random                               # Import the random module
import pygame                               # Import the Pygame library
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT   # Import constants from Pygame

pygame.init()                               # Initialize Pygame

FPS = pygame.time.Clock()                   # Create a clock object to control the frame rate

HEIGHT = 800                                # Set the height of the game window
WIDTH = 1200                                # Set the width of the game window

COLOR_WHITE = (255, 255, 255)               # Define the white color using RGB values
COLOR_BLACK = (0, 0, 0)                     # Define the black color using RGB values
COLOR_BLUE = (0, 0, 255)                    # Define the blue color using RGB values
COLOR_GREEN = (0, 255, 0)                   # Define the green color using RGB values

main_display = pygame.display.set_mode((WIDTH, HEIGHT))    # Create the main game display window

player_size = (40, 40)                      # Define the size of the player object
player = pygame.Surface(player_size)        # Create the player surface with the specified size
player.fill(COLOR_WHITE)                    # Fill the player surface with white color
player_rect = player.get_rect()             # Get the rectangle representing the player surface

player_move_down = [0, 1]                   # Define the movement vector for moving the player down
player_move_up = [0, -1]                    # Define the movement vector for moving the player up
player_move_right = [1, 0]                  # Define the movement vector for moving the player right
player_move_left = [-1, 0]                  # Define the movement vector for moving the player left

def create_enemy():
    enemy_size = (30, 30)                    # Define the size of the enemy object
    enemy = pygame.Surface(enemy_size)       # Create the enemy surface with the specified size
    enemy.fill(COLOR_BLUE)                   # Fill the enemy surface with blue color
    enemy_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT), *enemy_size)   # Create a rectangle for the enemy with a random y-coordinate
    enemy_move = [random.randint(-6, -1), 0]  # Define the movement vector for the enemy
    return [enemy, enemy_rect, enemy_move]    # Return the enemy, its rectangle, and movement vector as a list

def create_bonus():
    bonus_size = (30, 30)                    # Define the size of the bonus object
    bonus = pygame.Surface(bonus_size)       # Create the bonus surface with the specified size
    bonus.fill(COLOR_GREEN)                  # Fill the bonus surface with green color
    bonus_rect = pygame.Rect(random.randint(0, WIDTH), 0, *bonus_size)       # Create a rectangle for the bonus with a random x-coordinate
    bonus_move = [0, random.randint(1, 5)]    # Define the movement vector for the bonus
    return [bonus, bonus_rect, bonus_move]    # Return the bonus, its rectangle, and movement vector as a list

CREATE_ENEMY = pygame.USEREVENT + 1          # Define a custom event for creating enemies
pygame.time.set_timer(CREATE_ENEMY, 1500)    # Set a timer to trigger the creation of enemies every 1500 milliseconds
CREATE_BONUS = pygame.USEREVENT + 2          # Define a custom event for creating bonuses
pygame.time.set_timer(CREATE_BONUS, 1500)    # Set a timer to trigger the creation of bonuses every 1500 milliseconds

enemies = []                                # Initialize an empty list to store the enemies
bonuses = []                                # Initialize an empty list to store the bonuses

playing = True                              # Set the playing flag to True to start the game loop

while playing:
    FPS.tick(160)                           # Limit the frame rate to 160 frames per second

    for event in pygame.event.get():        # Handle events
        if event.type == QUIT:               # If the user closes the window, set the playing flag to False to exit the loop
            playing = False
        if event.type == CREATE_ENEMY:       # If the CREATE_ENEMY event is triggered, create a new enemy and add it to the enemies list
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:       # If the CREATE_BONUS event is triggered, create a new bonus and add it to the bonuses list
            bonuses.append(create_bonus())

    main_display.fill(COLOR_BLACK)          # Clear the display by filling it with black color

    keys = pygame.key.get_pressed()         # Get the currently pressed keys

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:      # If the down arrow key is pressed and the player is not at the bottom of the screen, move the player down
        player_rect = player_rect.move(player_move_down)

    if keys[K_UP] and player_rect.top > 0:     # If the up arrow key is pressed and the player is not at the top of the screen, move the player up
        player_rect = player_rect.move(player_move_up)

    if keys[K_RIGHT] and player_rect.right < WIDTH:     # If the right arrow key is pressed and the player is not at the right edge of the screen, move the player right
        player_rect = player_rect.move(player_move_right)

    if keys[K_LEFT] and player_rect.left > 0:     # If the left arrow key is pressed and the player is not at the left edge of the screen, move the player left
        player_rect = player_rect.move(player_move_left)

    for enemy in enemies:                   # Update the position of each enemy and draw it on the main display surface
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

    for bonus in bonuses:                   # Update the position of each bonus and draw it on the main display surface
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])    

    main_display.blit(player, player_rect)   # Draw the player on the main display surface

    pygame.display.flip()                   # Update the contents of the entire display

    for enemy in enemies:                   # Remove enemies that have moved beyond the left edge of the screen
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:                   # Remove bonuses that have moved beyond the bottom of the screen
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))

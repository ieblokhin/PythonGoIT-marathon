import random                               # Import the random module
import os                                   # Import the os module for file path operations
import pygame                               # Import the Pygame library
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT   # Import constants from Pygame

pygame.init()                               # Initialize Pygame

FPS = pygame.time.Clock()                   # Create a clock object to control the frame rate

HEIGHT = 800                                # Set the height of the game window
WIDTH = 1200                                # Set the width of the game window
COLOR_GREEN = (0, 255, 0)                   # Define the green color using RGB values

FONT = pygame.font.SysFont('Verdana', 30)   # Create a font object for rendering text

main_display = pygame.display.set_mode((WIDTH, HEIGHT))    # Create the main game display window

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))    # Load and scale the background image
bg_x1 = 0                                   # Initialize the x-coordinate of the first background image
bg_x2 = bg.get_width()                      # Initialize the x-coordinate of the second background image
bg_move = 3                                 # Set the speed at which the background moves

IMAGE_PATH = "goose"                        # Define the path to the directory containing the player images
PLAYER_IMAGES = os.listdir(IMAGE_PATH)       # Get the list of player image files in the directory

player_size = (20, 20)                      # Define the size of the player object
player = pygame.image.load('player.png').convert_alpha()    # Load the player image with transparency
player_rect = player.get_rect(midleft=(0, HEIGHT // 2))     # Set the player's position to the center of the left side
player_move_down = [0, 4]                   # Define the movement vector for moving the player down
player_move_up = [0, -4]                    # Define the movement vector for moving the player up
player_move_right = [4, 0]                  # Define the movement vector for moving the player right
player_move_left = [-4, 0]                  # Define the movement vector for moving the player left

def create_enemy():
    enemy_size = (80, 40)                   # Define the size of the enemy object
    enemy = pygame.image.load('enemy.png').convert_alpha()    # Load the enemy image with transparency
    enemy = pygame.transform.scale(enemy, enemy_size)    # Scale the enemy image
    enemy_rect = pygame.Rect(WIDTH, random.randint(100, HEIGHT - 100), *enemy_size)    # Create a rectangle for the enemy with a random y-coordinate
    enemy_move = [random.randint(-8, -4), 0]  # Define the movement vector for the enemy
    return [enemy, enemy_rect, enemy_move]    # Return the enemy, its rectangle, and movement vector as a list

def create_bonus():
    bonus_size = (70, 80)                   # Define the size of the bonus object
    bonus = pygame.image.load('bonus.png').convert_alpha()    # Load the bonus image with transparency
    bonus = pygame.transform.scale(bonus, bonus_size)    # Scale the bonus image
    bonus_rect = pygame.Rect(random.randint(100, WIDTH - 100), 0, *bonus_size)    # Create a rectangle for the bonus with a random x-coordinate
    bonus_move = [0, random.randint(4, 8)]    # Define the movement vector for the bonus
    return [bonus, bonus_rect, bonus_move]    # Return the bonus, its rectangle, and movement vector as a list

CREATE_ENEMY = pygame.USEREVENT + 1          # Define a custom event for creating enemies
pygame.time.set_timer(CREATE_ENEMY, 1500)    # Set a timer to trigger the CREATE_ENEMY event every 1.5 seconds
CREATE_BONUS = pygame.USEREVENT + 2          # Define a custom event for creating bonuses
pygame.time.set_timer(CREATE_BONUS, 3000)    # Set a timer to trigger the CREATE_BONUS event every 3 seconds
CHANGE_IMAGE = pygame.USEREVENT + 3          # Define a custom event for changing the player's image
pygame.time.set_timer(CHANGE_IMAGE, 200)     # Set a timer to trigger the CHANGE_IMAGE event every 0.2 seconds

enemies = []                                # Initialize an empty list to store the enemies
bonuses = []                                # Initialize an empty list to store the bonuses
score = 0                                   # Initialize the score counter
image_index = 0                             # Initialize the index for player image selection

playing = True                              # Set the playing flag to True to start the game loop

while playing:
    FPS.tick(120)                           # Limit the frame rate to 120 frames per second

    for event in pygame.event.get():        # Handle events
        if event.type == QUIT:               # If the user closes the window, set the playing flag to False to exit the loop
            playing = False
        if event.type == CREATE_ENEMY:       # If the CREATE_ENEMY event is triggered, create a new enemy and add it to the enemies list
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:       # If the CREATE_BONUS event is triggered, create a new bonus and add it to the bonuses list
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:       # If the CHANGE_IMAGE event is triggered, change the player's image
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):   # If the index exceeds the number of images, reset it to 0
                image_index = 0
    
    bg_x1 -= bg_move                         # Update the background x-coordinates
    bg_x2 -= bg_move

    if bg_x1 < -bg.get_width():              # If the first background image moves off the screen, wrap it to the right side
        bg_x1 = bg.get_width()

    if bg_x2 < -bg.get_width():              # If the second background image moves off the screen, wrap it to the right side
        bg_x2 = bg.get_width()

    main_display.blit(bg, (bg_x1, 0))        # Draw the background images on the display surface
    main_display.blit(bg, (bg_x2, 0))

    keys = pygame.key.get_pressed()          # Get the currently pressed keys

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:      # If the down arrow key is pressed and the player is not at the bottom of the screen, move the player down
        player_rect = player_rect.move(player_move_down)

    if keys[K_UP] and player_rect.top > 0:     # If the up arrow key is pressed and the player is not at the top of the screen, move the player up
        player_rect = player_rect.move(player_move_up)

    if keys[K_RIGHT] and player_rect.right < WIDTH:     # If the right arrow key is pressed and the player is not at the right edge of the screen, move the player right
        player_rect = player_rect.move(player_move_right)

    if keys[K_LEFT] and player_rect.left > 0:    # If the left arrow key is pressed and the player is not at the left edge of the screen, move the player left
        player_rect = player_rect.move(player_move_left)

    
    for enemy in enemies:                   # Update and draw the enemies
        enemy[1] = enemy[1].move(enemy[2])   # Move the enemy according to its movement vector
        main_display.blit(enemy[0], enemy[1])    # Draw the enemy on the display surface

        if player_rect.colliderect(enemy[1]):     # If the player collides with an enemy, end the game
            playing = False

    for bonus in bonuses:                   # Update and draw the bonuses
        bonus[1] = bonus[1].move(bonus[2])   # Move the bonus according to its movement vector
        main_display.blit(bonus[0], bonus[1])    # Draw the bonus on the display surface

        if player_rect.colliderect(bonus[1]):     # If the player collides with a bonus, increase the score and remove the bonus from the list
            score += 1
            bonuses.pop(bonuses.index(bonus))
    
    main_display.blit(FONT.render(str(score), True, COLOR_GREEN), (WIDTH-50, 20))   # Render and draw the score text on the display surface
    main_display.blit(player, player_rect)     # Draw the player on the display surface

    pygame.display.flip()                      # Update the contents of the entire display

    for enemy in enemies:                       # Remove enemies that move off the left side of the screen
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:                       # Remove bonuses that move off the bottom of the screen
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))

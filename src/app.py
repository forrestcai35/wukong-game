import pygame
import sys
# Initialize Pygame
pygame.init()

# Screen Dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sun Wukong: The Monkey King's Journey")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Colors (temporary)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (34, 139, 34)

# Player attributes
player_width = 50
player_height = 60
player_x = 100
player_y = HEIGHT - player_height - 100  # Start above ground level
player_speed = 5
player_jump_speed = -15
gravity = 1
on_ground = False
y_velocity = 0

# Load player image or use a placeholder
# Replace with an actual Wukong sprite later
player_surf = pygame.Surface((player_width, player_height))
player_surf.fill(GREEN)

# Ground (temporary)
ground_height = 100
ground_rect = pygame.Rect(0, HEIGHT - ground_height, WIDTH, ground_height)

# Basic font for text
font = pygame.font.SysFont(None, 24)

# Game loop variables
running = True

while running:
    clock.tick(60)  # 60 FPS
    
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Key Presses
    keys = pygame.key.get_pressed()

    # Horizontal movement
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    # Jumping
    if keys[pygame.K_SPACE] and on_ground:
        y_velocity = player_jump_speed
        on_ground = False

    # Gravity
    y_velocity += gravity
    player_y += y_velocity

    # Collision with ground
    if player_y + player_height > HEIGHT - ground_height:
        player_y = HEIGHT - ground_height - player_height
        y_velocity = 0
        on_ground = True

    # Drawing
    screen.fill(WHITE)

    # Draw ground
    pygame.draw.rect(screen, BLACK, ground_rect)

    # Draw player
    screen.blit(player_surf, (player_x, player_y))

    # Temporary instructions text
    instructions_text = font.render("Use LEFT/RIGHT to move, SPACE to jump", True, BLACK)
    screen.blit(instructions_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
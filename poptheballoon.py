import pygame
import random
import sys

# Initialize Pygame
pygame.init()
balloons=[]

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Balloon properties
BALLOON_RADIUS = 30
BALLOON_SPEED = 3
BALLOON_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # Red, Green, Blue

# Game variables
timer = 7200  # 2 minutes
score = 0
miss_penalty = 1

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pop-The-Balloon")

# Function to spawn a balloon
def spawn_balloon():
    color = random.choice(BALLOON_COLORS)
    x = random.randint(BALLOON_RADIUS, SCREEN_WIDTH - BALLOON_RADIUS)
    y = SCREEN_HEIGHT + BALLOON_RADIUS
    return {'rect': pygame.Rect(x, y, BALLOON_RADIUS * 2, BALLOON_RADIUS * 2), 'color': color}

# Function to decrease the timer
def decrease_timer():
    global timer
    timer -= 1

# Function to check if the balloon is popped
def check_balloon_popped(balloon, pos):
    return balloon['rect'].collidepoint(pos)

# Main game loop
# Main game loop
clock = pygame.time.Clock()
running = True
spawn_timer = 0

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for balloon in balloons:
                if check_balloon_popped(balloon, pos):
                    score += 2
                    balloons.remove(balloon)
                    break
            else:
                score -= miss_penalty

    # Update spawn timer
    spawn_timer += 1

    # Spawn new balloons every 60 frames (1 second)
    if spawn_timer % 60 == 0:
        balloons.append(spawn_balloon())

    # Update balloons' positions
    for balloon in balloons:
        balloon['rect'].move_ip(0, -BALLOON_SPEED)

    # Remove balloons that have gone off-screen
    balloons = [balloon for balloon in balloons if balloon['rect'].bottom > 0]

    # Display balloons
    for balloon in balloons:
        pygame.draw.circle(screen, balloon['color'], balloon['rect'].center, BALLOON_RADIUS)

    # Display timer and score
    font = pygame.font.SysFont(None, 36)
    timer_text = font.render(f'Time: {timer // 60}:{timer % 60:0>2}', True, BLACK)
    score_text = font.render(f'Score: {score}', True, BLACK)
    screen.blit(timer_text, (10, 10))
    screen.blit(score_text, (10, 50))

    pygame.display.flip()

    # Decrease timer
    decrease_timer()

    # Check for game over
    if timer <= 0:
        running = False

    clock.tick(60)

# Game over
screen.fill(WHITE)
game_over_text = font.render("Game Over!", True, RED)
final_score_text = font.render(f"Final Score: {score}", True, BLACK)
screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
screen.blit(final_score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
pygame.display.flip()

pygame.time.delay(3000)  # Delay for 3 seconds before quitting
pygame.quit()

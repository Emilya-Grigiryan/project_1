import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GROUND_HEIGHT = 30
BALL_RADIUS = 30
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 70
GRAVITY = 0.5
OBSTACLE_SPEED = 12  # Increased obstacle speed
JUMP_VELOCITY = -12  # Increased jump velocity

def main():
    """Main function to run the ball game."""
    try:
        # Screen setup
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Ball Game")

        # Ball setup
        ball_x = 50
        ball_y = SCREEN_HEIGHT - GROUND_HEIGHT - BALL_RADIUS
        ball_vel_y = 0
        jumping = False

        # Obstacle setup
        obstacle = pygame.Rect(SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT - OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)

        # Clock
        clock = pygame.time.Clock()
        running = True
        score = 0

        # Font
        font = pygame.font.Font(None, 36)

        # Game loop
        game_over = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if not game_over:
                ball_y, ball_vel_y, jumping = handle_ball_movement(ball_y, ball_vel_y, jumping)

                obstacle.x -= OBSTACLE_SPEED
                if obstacle.x < 0:
                    obstacle.x = SCREEN_WIDTH
                    score += 1

                ball_rect = pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
                if ball_rect.colliderect(obstacle):
                    game_over = True

                draw_game(screen, font, ball_x, ball_y, obstacle, score)
            else:
                draw_game_over(screen, font, score)

            pygame.display.flip()
            clock.tick(30)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        pygame.quit()

def handle_ball_movement(ball_y, ball_vel_y, jumping):
    """Handles the ball movement including jumping and gravity."""
    keys = pygame.key.get_pressed()
    if not jumping and keys[pygame.K_SPACE]:
        ball_vel_y = JUMP_VELOCITY
        jumping = True

    ball_vel_y += GRAVITY
    ball_y += ball_vel_y

    if ball_y >= SCREEN_HEIGHT - GROUND_HEIGHT - BALL_RADIUS:
        ball_y = SCREEN_HEIGHT - GROUND_HEIGHT - BALL_RADIUS
        ball_vel_y = 0
        jumping = False

    return ball_y, ball_vel_y, jumping

def draw_game(screen, font, ball_x, ball_y, obstacle, score):
    """Draws the game elements on the screen."""
    screen.fill(WHITE)
    pygame.draw.circle(screen, BLUE, (ball_x, ball_y), BALL_RADIUS)
    pygame.draw.rect(screen, BLACK, obstacle)
    pygame.draw.rect(screen, BLACK, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))

    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

def draw_game_over(screen, font, score):
    """Draws the game over screen with the final score."""
    screen.fill(WHITE)
    game_over_text = font.render("Game Over", True, BLACK)
    final_score_text = font.render(f"Final Score: {score}", True, BLACK)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + game_over_text.get_height()))

if __name__ == "__main__":
    main()


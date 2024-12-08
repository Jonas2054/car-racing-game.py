import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CAR_WIDTH, CAR_HEIGHT = 50, 100
TRACK_WIDTH = 200
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Racing Game")

# Clock for FPS
clock = pygame.time.Clock()

# Car class
class Car:
    def __init__(self):
        self.x = WIDTH // 2 - CAR_WIDTH // 2
        self.y = HEIGHT - CAR_HEIGHT - 10
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.color = BLUE
        self.speed = 5
        self.velocity = 0
        self.angle = 0

    def draw(self, screen):
        car_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, car_rect)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        # Keep the car inside the screen
        self.x = max(0, min(self.x, WIDTH - self.width))
        self.y = max(0, min(self.y, HEIGHT - self.height))

# Track class
class Track:
    def __init__(self):
        self.track_color = (50, 50, 50)
        self.border_color = (200, 200, 200)

    def draw(self, screen):
        # Draw the track (a simple rectangle for the track)
        pygame.draw.rect(screen, self.track_color, (WIDTH // 2 - TRACK_WIDTH // 2, 0, TRACK_WIDTH, HEIGHT))
        # Draw the track borders
        pygame.draw.rect(screen, self.border_color, (WIDTH // 2 - TRACK_WIDTH // 2 - 10, 0, TRACK_WIDTH + 20, HEIGHT), 5)
        pygame.draw.rect(screen, self.border_color, (WIDTH // 2 + TRACK_WIDTH // 2 - 10, 0, TRACK_WIDTH + 20, HEIGHT), 5)

# Obstacle class
class Obstacle:
    def __init__(self):
        self.x = random.randint(WIDTH // 2 - TRACK_WIDTH // 2, WIDTH // 2 + TRACK_WIDTH // 2 - CAR_WIDTH)
        self.y = -CAR_HEIGHT
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.color = RED
        self.speed = 5

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = -CAR_HEIGHT
            self.x = random.randint(WIDTH // 2 - TRACK_WIDTH // 2, WIDTH // 2 + TRACK_WIDTH // 2 - CAR_WIDTH)

    def check_collision(self, car):
        # Check if the car collides with the obstacle
        car_rect = pygame.Rect(car.x, car.y, car.width, car.height)
        obstacle_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return car_rect.colliderect(obstacle_rect)

# Main game loop
def main():
    # Game initialization
    car = Car()
    track = Track()
    obstacles = [Obstacle() for _ in range(3)]  # 3 obstacles on the track

    score = 0
    game_over = False
    font = pygame.font.SysFont(None, 55)

    # Main game loop
    while not game_over:
        screen.fill(WHITE)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        # Draw the track
        track.draw(screen)

        # Move and draw the player's car
        car.move()
        car.draw(screen)

        # Move and draw obstacles
        for obstacle in obstacles:
            obstacle.move()
            obstacle.draw(screen)

            # Check for collisions
            if obstacle.check_collision(car):
                game_over = True

        # Display the score
        score += 1
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Game over condition
        if game_over:
            game_over_text = font.render("GAME OVER", True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - 150, HEIGHT // 2 - 50))

        # Update the screen
        pygame.display.update()
        
        # FPS
        clock.tick(FPS)

    # End the game
    pygame.quit()

if __name__ == "__main__":
    main()

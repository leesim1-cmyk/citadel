import pygame
import random
import sys

# Initialize pygame modules
pygame.init()

# Game Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
GRID_SIZE = 20
FPS = 7

# Colors (R, G, B)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 0, 255)
COLOR_RED = (255, 0, 0)
ROWS = int(SCREEN_HEIGHT / GRID_SIZE)
COLS = int(SCREEN_WIDTH / GRID_SIZE)
SQUARE_SIZE = 20

LIGHT_GREEN = (35, 204, 27) 
DARK_GREEN = (5, 102, 0)

# Setup Display Window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

def draw_checkerboard(surface):
    for row in range(ROWS):
        for col in range(COLS):
            # Alternating logic: if row + col is even, use light color; if odd, use dark
            if (row + col) % 2 == 0:
                color = LIGHT_GREEN
            else:
                color = DARK_GREEN
            
            # Calculate coordinates for each rectangle
            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE
            
            # Draw the square
            pygame.draw.rect(surface, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

class Snake:

    def __init__(self):
        # Start with a length of 3 blocks in the middle of the screen
        self.body = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                     (SCREEN_WIDTH // 2 - GRID_SIZE, SCREEN_HEIGHT // 2),
                     (SCREEN_WIDTH // 2 - (2 * GRID_SIZE), SCREEN_HEIGHT // 2)]
        self.direction = pygame.K_RIGHT
        self.alive = True

    def change_direction(self, new_dir):
        # Prevent the snake from reversing into itself directly
        opposite_dirs = {
            pygame.K_UP: pygame.K_DOWN,
            pygame.K_DOWN: pygame.K_UP,
            pygame.K_LEFT: pygame.K_RIGHT,
            pygame.K_RIGHT: pygame.K_LEFT,
        }
        if new_dir in opposite_dirs and new_dir != opposite_dirs.get(
                self.direction):
            self.direction = new_dir

    def move(self):
        if not self.alive:
            return

        head_x, head_y = self.body[0]

        # Calculate new head position based on direction
        if self.direction == pygame.K_UP:
            head_y -= GRID_SIZE
        elif self.direction == pygame.K_DOWN:
            head_y += GRID_SIZE
        elif self.direction == pygame.K_LEFT:
            head_x -= GRID_SIZE
        elif self.direction == pygame.K_RIGHT:
            head_x += GRID_SIZE

        new_head = (head_x, head_y)

        # Check wall collision bounds
        if (head_x < 0 or head_x >= SCREEN_WIDTH or head_y < 0
                or head_y >= SCREEN_HEIGHT):
            self.alive = False
            return

        # Check self-collision
        if new_head in self.body:
            self.alive = False
            return

        # Insert new head position
        self.body.insert(0, new_head)

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(
                surface, COLOR_GREEN,
                pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))


class Food:

    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        # Choose a random grid cell on the board
        x = (random.randint(0, (SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE) *
             GRID_SIZE)
        y = (random.randint(0, (SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE) *
             GRID_SIZE)
        self.position = (x, y)

    def draw(self, surface):
        pygame.draw.rect(
            surface, COLOR_RED,
            pygame.Rect(self.position[0], self.position[1], GRID_SIZE,
                        GRID_SIZE),
        )


def main():
    snake = Snake()
    food = Food()
    score = 0

    # Ensure food doesn't spawn on top of the starting snake position
    while food.position in snake.body:
        food.randomize_position()

    font = pygame.font.SysFont("Arial", 24)

    running = True
    while running:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in [
                        pygame.K_UP,
                        pygame.K_DOWN,
                        pygame.K_LEFT,
                        pygame.K_RIGHT,
                ]:
                    snake.change_direction(event.key)

        # 2. Update Game Logic
        snake.move()

        if not snake.alive:
            running = False
            print(f"Game Over! Your Final Score: {score}")
            break

        # Check if snake head shares a cell with the food
        if snake.body[0] == food.position:
            score += 1
            food.randomize_position()
            # Ensure food doesn't respawn on the snake's body
            while food.position in snake.body:
                food.randomize_position()
        else:
            # Pop the tail out to simulate movement if food wasn't eaten
            snake.body.pop()

        # 3. Rendering / Drawing
        
            

        screen.fill(COLOR_BLACK)
        draw_checkerboard(screen)
        snake.draw(screen)
        food.draw(screen)

        # Display the score
        score_surface = font.render(f"Score: {score}", True, COLOR_WHITE)
        screen.blit(score_surface, (10, 10))

        pygame.display.flip()

        # Tick rate sets game speed (frames per second)
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

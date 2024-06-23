import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mammoth Rampage: Stomping Out Climate Change")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# Mammoth class
class Mammoth(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.rect.clamp_ip(screen.get_rect())


# Car class
class Car(pygame.sprite.Sprite):
    def __init__(self, is_gas_guzzler):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(RED if is_gas_guzzler else GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 40)
        self.rect.y = -60
        self.speed = random.randint(1, 5)
        self.is_gas_guzzler = is_gas_guzzler

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


# Game variables
mammoth = Mammoth()
all_sprites = pygame.sprite.Group(mammoth)
cars = pygame.sprite.Group()
clock = pygame.time.Clock()
score = 0
font = pygame.font.Font(None, 36)

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move mammoth
    keys = pygame.key.get_pressed()
    mammoth.move(
        keys[pygame.K_RIGHT] - keys[pygame.K_LEFT],
        keys[pygame.K_DOWN] - keys[pygame.K_UP],
    )

    # Spawn cars
    if random.randint(1, 60) == 1:
        cars.add(Car(random.choice([True, False])))

    # Update
    cars.update()

    # Check collisions
    for car in pygame.sprite.spritecollide(mammoth, cars, True):
        if car.is_gas_guzzler:
            score += 10
        else:
            score -= 5

    # Draw
    screen.fill(WHITE)
    all_sprites.draw(screen)
    cars.draw(screen)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit game
pygame.quit()

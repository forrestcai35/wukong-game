import pygame, sys, random

pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
FPS = 60

# Colors
BG_COLOR = (135, 206, 250)  # Light sky blue

# Font
font = pygame.font.SysFont(None, 36)

class Player:
    def __init__(self, x, y, player_img):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.gravity = 0.5
        self.jump_strength = -10
        self.image = player_img
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, width, height):
        # Apply horizontal movement
        self.x += self.dx
        # Wrap horizontally
        if self.x < 0:
            self.x = width
        elif self.x > width:
            self.x = 0

        # Apply vertical movement
        self.y += self.dy
        self.dy += self.gravity

        self.rect.topleft = (self.x, self.y)

    def jump(self):
        self.dy = self.jump_strength

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Platform:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Journey To The West")
        self.clock = pygame.time.Clock()

        # Load images
        self.player_img = pygame.image.load("sprites/wukong.png").convert_alpha()
        self.player_img = pygame.transform.scale(self.player_img, (80, 80))
        self.platform_img = pygame.image.load("sprites/nimbus.png").convert_alpha()
        self.platform_img = pygame.transform.scale(self.platform_img, (100, 30))

        # Initialize player
        self.player = Player(WIDTH // 2, HEIGHT // 2, self.player_img)

        # Initialize platforms
        self.num_platforms = 10
        self.platforms = self._generate_initial_platforms()

        self.score = 0
        self.running = True

    def _generate_initial_platforms(self):
        platforms = []
        for i in range(self.num_platforms):
            x = random.randint(0, WIDTH - self.platform_img.get_width())
            y = HEIGHT - (i * 80) - 50
            platforms.append(Platform(x, y, self.platform_img))
        # Sort by y coordinate
        platforms.sort(key=lambda p: p.rect.y)
        return platforms

    def _create_platform(self, topmost_y):
        x = random.randint(0, WIDTH - self.platform_img.get_width())
        y = topmost_y - 80
        return Platform(x, y, self.platform_img)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.dx = -5
        elif keys[pygame.K_RIGHT]:
            self.player.dx = 5
        else:
            self.player.dx = 0

    def check_collisions(self):
        # Check for platform collision only if player is falling downwards
        if self.player.dy > 0:
            for p in self.platforms:
                if (self.player.rect.colliderect(p.rect) and
                        (self.player.y + self.player.rect.height - self.player.dy) < p.rect.y):
                    self.player.y = p.rect.y - self.player.rect.height
                    self.player.jump()  # Player jumps again on collision

    def scroll_world(self):
        # If player is higher than a quarter up the screen, move platforms down
        if self.player.y < HEIGHT // 4:
            diff = (HEIGHT // 4) - self.player.y
            self.player.y = HEIGHT // 4
            for p in self.platforms:
                p.rect.y += diff

            # Remove platforms that fall off the screen
            self.platforms = [p for p in self.platforms if p.rect.y <= HEIGHT]

            # Sort to find topmost platform and create new ones if needed
            self.platforms.sort(key=lambda p: p.rect.y)
            while len(self.platforms) < self.num_platforms:
                topmost_platform = self.platforms[0]
                new_p = self._create_platform(topmost_platform.rect.y)
                self.platforms.append(new_p)
                self.platforms.sort(key=lambda p: p.rect.y)
                self.score += 10

    def run(self):
        while self.running:
            self.clock.tick(FPS)

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Handle input
            self.handle_input()

            # Update player
            self.player.update(WIDTH, HEIGHT)

            # Check collisions
            self.check_collisions()

            # Scroll the world if player moves upward
            self.scroll_world()

            # Check game over condition
            if self.player.y > HEIGHT:
                self.running = False

            # Drawing
            self.screen.fill(BG_COLOR)
            # Draw platforms
            for p in self.platforms:
                p.draw(self.screen)
            # Draw player
            self.player.draw(self.screen)

            # Draw score
            score_text = font.render(f"Score: {self.score}", True, (0,0,0))
            self.screen.blit(score_text, (10, 10))

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()

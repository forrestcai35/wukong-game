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

class CollectibleTalisman:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class CollectibleFruit:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Journey To The West")
        self.clock = pygame.time.Clock()

        # Load images
        self.player_img = pygame.image.load("sprites/wukong.png").convert_alpha()
        self.player_img = pygame.transform.scale(self.player_img, (90, 90))
        self.platform_img = pygame.image.load("sprites/nimbus.png").convert_alpha()
        self.platform_img = pygame.transform.scale(self.platform_img, (100, 25))

        # Load collectible images
        self.talisman_img = pygame.image.load("sprites/talisman.png").convert_alpha()
        self.talisman_img = pygame.transform.scale(self.talisman_img, (50, 50))
        self.fruit_img = pygame.image.load("sprites/fruit.png").convert_alpha()
        self.fruit_img = pygame.transform.scale(self.fruit_img, (50, 50))

        # Initialize player
        self.player = Player(WIDTH // 2, HEIGHT // 2, self.player_img)

        # Initialize platforms
        self.num_platforms = 10
        self.platforms = self._generate_initial_platforms()

        # Lists for collectibles
        self.talismans = []
        self.fruits = []

        # Possibly place some initial collectibles
        self._place_initial_collectibles()

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

    def _place_initial_collectibles(self):
        # Randomly place a few collectibles on existing platforms
        for p in self.platforms:
            # With some probability, place a talisman or fruit
            if random.random() < 0.3:  # 30% chance to place a collectible
                if random.random() < 0.5:
                    # Place a talisman
                    tx = p.rect.centerx
                    ty = p.rect.y - 20  # just above the platform
                    self.talismans.append(CollectibleTalisman(tx, ty, self.talisman_img))
                else:
                    # Place a fruit
                    fx = p.rect.centerx
                    fy = p.rect.y - 20
                    self.fruits.append(CollectibleFruit(fx, fy, self.fruit_img))

    def _add_collectibles_on_new_platform(self, platform):
        # Chance to add collectibles to newly generated platforms
        if random.random() < 0.3:
            if random.random() < 0.5:
                # Add a talisman
                tx = platform.rect.centerx
                ty = platform.rect.y - 20
                self.talismans.append(CollectibleTalisman(tx, ty, self.talisman_img))
            else:
                # Add a fruit
                fx = platform.rect.centerx
                fy = platform.rect.y - 20
                self.fruits.append(CollectibleFruit(fx, fy, self.fruit_img))

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

        # Check collectible collisions
        # Talisman
        for t in self.talismans[:]:
            if self.player.rect.colliderect(t.rect):
                self.score += 20  # Award points for a talisman
                self.talismans.remove(t)

        # Fruit
        for f in self.fruits[:]:
            if self.player.rect.colliderect(f.rect):
                self.score += 15  # Award points for a fruit
                self.fruits.remove(f)

    def scroll_world(self):
        # If player is higher than a quarter up the screen, move platforms down
        if self.player.y < HEIGHT // 4:
            diff = (HEIGHT // 4) - self.player.y
            self.player.y = HEIGHT // 4
            for p in self.platforms:
                p.rect.y += diff
            for t in self.talismans:
                t.rect.y += diff
            for f in self.fruits:
                f.rect.y += diff

            # Remove platforms (and associated collectibles) that fall off the screen
            self.platforms = [p for p in self.platforms if p.rect.y <= HEIGHT]
            self.talismans = [t for t in self.talismans if t.rect.y <= HEIGHT]
            self.fruits = [f for f in self.fruits if f.rect.y <= HEIGHT]

            # Sort to find topmost platform and create new ones if needed
            self.platforms.sort(key=lambda p: p.rect.y)
            while len(self.platforms) < self.num_platforms:
                topmost_platform = self.platforms[0]
                new_p = self._create_platform(topmost_platform.rect.y)
                self.platforms.append(new_p)
                self.platforms.sort(key=lambda p: p.rect.y)
                self.score += 10

                # Add collectibles on new platform
                self._add_collectibles_on_new_platform(new_p)

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
            # Draw collectibles
            for t in self.talismans:
                t.draw(self.screen)
            for f in self.fruits:
                f.draw(self.screen)
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

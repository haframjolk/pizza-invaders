import pygame
import random
import os
import sys

"""
RAM
21.11.2018 - 5.12.2018
Lokaverkefni
"""

WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)

# Keybindings
LEFT = pygame.K_LEFT
RIGHT = pygame.K_RIGHT
FIRE = pygame.K_SPACE
QUIT = pygame.K_ESCAPE

# Config
PLAYER_SPEED = 6
BULLET_SPEED = 12
FONT_NAME = pygame.font.match_font("Arial")

# Directory containing game files
# Determine whether or not game has been frozen
is_frozen = getattr(sys, "frozen", False)
# If game is frozen
if is_frozen:
    # py2app
    if is_frozen == "macosx_app":
        game_dir = "."
    # PyInstaller
    else:
        game_dir = sys._MEIPASS
# Use script directory if being run as script
else:
    game_dir = os.path.dirname(__file__)

img_dir = os.path.join(game_dir, "img")
snd_dir = os.path.join(game_dir, "snd")

# Game init
pygame.init()
pygame.mixer.init()

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pizza Invaders")
clock = pygame.time.Clock()


def draw_text(surf, text, size, x, y):
    """Draw text on the screen"""
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
    """Sprite for player"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (61, 80))
        self.rect = self.image.get_rect()
        self.radius = 31  # Hitbox radius
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.bottom = HEIGHT
        self.x_speed = PLAYER_SPEED
        # Automatic fire (while holding FIRE button)
        self.fire_delay = 150  # Delay in ms to wait between shots
        self.last_fired = pygame.time.get_ticks()

    def update(self):
        # By default, player speed is 0
        self.x_speed = 0

        # Change speed based on user input
        keystate = pygame.key.get_pressed()
        if keystate[LEFT]:
            self.x_speed = -PLAYER_SPEED
        if keystate[RIGHT]:
            self.x_speed = PLAYER_SPEED
        if keystate[FIRE]:
            self.fire()

        # Move player horizontally according to speed
        self.rect.x += self.x_speed

        # Constrain player within screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def fire(self):
        # If fire_delay has passed since last shot, fire
        now = pygame.time.get_ticks()
        if now - self.last_fired > self.fire_delay:
            self.last_fired = now
            # Create a new bullet, add it to sprites and play fire sound
            bullet = Bullet(self.rect.centerx, self.rect.top)
            sprites.add(bullet)
            bullets.add(bullet)
            fire_sound.play()


class Mob(pygame.sprite.Sprite):
    """Enemies in the game"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Choose a random image for the mob
        self.image_orig = pygame.transform.scale(random.choice(mob_images), (28, 60))
        self.image = self.image_orig.copy()  # Copy image to improve performance of rotation
        self.rect = self.image.get_rect()
        # Mobs start at random positions off screen
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        # Mobs have differing speeds
        self.y_speed = random.randint(1, 8)
        self.x_speed = random.randint(-3, 3)
        # Mobs rotate at varying speeds
        self.rotation = 0
        self.rotation_speed = random.randint(-8, 8)
        self.last_rotated = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        # Rotate mob every 50 ticks
        if now - self.last_rotated > 50:
            self.last_rotated = now
            self.rotation = (self.rotation + self.rotation_speed) % 360
            # Create a new image based on the original using the new rotation value (degrees)
            new_image = pygame.transform.rotate(self.image_orig, self.rotation)
            # Update rect with rotation
            old_center = self.rect.center
            # Update mob
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        # Move mobs according to speed
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        # If enemy goes off the bottom or the sides, push it to the top
        if self.rect.top > HEIGHT + 10 or self.rect.left < -60 or self.rect.right > WIDTH + 60:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            # Mobs start at varying distances off-screen, with random vertical speeds
            self.rect.y = random.randint(-100, -40)
            self.y_speed = random.randint(1, 8)


class Bullet(pygame.sprite.Sprite):
    """Bullets shot by the player"""
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (15, 28))
        self.rect = self.image.get_rect()
        # x and y are the coordinates of the player, passed as arguments
        self.rect.bottom = y
        self.rect.centerx = x
        self.y_speed = -BULLET_SPEED

    def update(self):
        self.rect.y += self.y_speed
        # If bullet goes off screen, kill it
        if self.rect.bottom < 0:
            self.kill()


def show_game_over():
    """Game over screen, shown before game starts and after player dies"""
    # Stop playing music and clear screen
    screen.blit(background, background_rect)
    pygame.mixer.music.stop()
    # Draw text to screen
    # Game title
    draw_text(screen, "Pizza Invaders", 64, WIDTH / 2, HEIGHT / 5)
    # Controls
    draw_text(screen, "Move: Arrow keys", 22, WIDTH / 2, HEIGHT * 2 / 5)
    draw_text(screen, "Fire: Space", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Quit: Escape", 22, WIDTH / 2, HEIGHT * 3 / 5)
    # Instructions to start
    draw_text(screen, "Press any key to start!", 18, WIDTH / 2, HEIGHT * 3 / 4)
    # Flip display
    pygame.display.flip()

    # Wait for user input
    waiting = True
    key_pressed = False
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            # If user closes the window, quit the game
            if event.type == pygame.QUIT:
                sys.exit(0)  # Use sys.exit instead of pygame.quit to prevent errors on quit
                # pygame.quit()
            # If user presses any key, start game
            # Key must be pressed and then released to start game
            # This prevents KEYUP events from keys that were pressed during the previous game from starting a new one
            if event.type == pygame.KEYDOWN:
                # If user presses the QUIT key, quit the game
                if event.key == QUIT:
                    sys.exit(0)
                    # pygame.quit()
                key_pressed = True
            if event.type == pygame.KEYUP:
                if key_pressed:
                    waiting = False


# Load all graphics
# Background
background = pygame.image.load(os.path.join(img_dir, "background.jpg")).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()
# Player
player_img = pygame.image.load(os.path.join(img_dir, "player.png")).convert_alpha()
# Mobs
mob_list = ["mob.png", "mob1.png"]
mob_images = [pygame.image.load(os.path.join(img_dir, img_name)).convert_alpha() for img_name in mob_list]
# Bullet
bullet_img = pygame.image.load(os.path.join(img_dir, "bullet.png")).convert_alpha()

# Load all sounds
fire_sound = pygame.mixer.Sound(os.path.join(snd_dir, "fire.wav"))
expl_list = ["expl0.wav", "expl1.wav"]
expl_sounds = [pygame.mixer.Sound(os.path.join(snd_dir, snd_name)) for snd_name in expl_list]
# Background music
pygame.mixer.music.load(os.path.join(snd_dir, "background.ogg"))


# Game loop
game_over = True
running = True
while running:
    # Game over screen is shown on first run and after player dies
    if game_over:
        show_game_over()

        # When game over loop ends, start game
        game_over = False
        pygame.mixer.music.play(loops=-1)  # Loop background music infinitely
        # When user chooses to play, initialize game
        # Create sprites
        sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        # Create 8 mobs and add them to the sprite groups
        for _ in range(8):
            m = Mob()
            sprites.add(m)
            mobs.add(m)
        # Create bullet sprite group
        bullets = pygame.sprite.Group()
        # Add player to sprite group
        player = Player()
        sprites.add(player)

        # Initial score is 0
        score = 0

    # Game
    # Run game loop at specified speed
    clock.tick(FPS)
    # Process events
    for event in pygame.event.get():
        # Stop running game if user quits
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # End game (go to game over) if user hits the QUIT key
            if event.key == QUIT:
                game_over = True

    # Update
    sprites.update()

    # Check for bullet collisions with mobs
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)  # Kill both mob and bullet if they collide
    # If a mob is killed, add to score and spawn a new mob
    for hit in hits:
        score += 1  # 1 kill = 1 pt
        m = Mob()
        sprites.add(m)
        mobs.add(m)
        random.choice(expl_sounds).play()  # Play one of the explosion sounds

    # Check for mob collisions with player
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    # If player is hit by mob, player dies and game ends
    if hits:
        game_over = True

    # Render
    screen.blit(background, background_rect)
    sprites.draw(screen)
    # Draw score on top
    draw_text(screen, str(score), 24, WIDTH / 2, 10)
    # Flip display
    pygame.display.flip()

# When loop ends, quit game
sys.exit(0)
# pygame.quit()

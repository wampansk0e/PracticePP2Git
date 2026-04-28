import pygame, sys
from pygame.locals import *
import random, time
import os

# Initializing 
pygame.init()

# --- ASSETS FOLDER SETUP ---
BASE_PATH = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_PATH, "assets")

def get_asset(filename):
    """Utility to fetch files from the assets folder."""
    return os.path.join(ASSETS_DIR, filename)

# Setting up FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
RED   = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game Variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COIN_SCORE = 0 
N_COINS_FOR_SPEEDUP = 5 # Speed increases every N coins

# Fonts
font_small = pygame.font.SysFont("Verdana", 20)
game_over = pygame.font.SysFont("Verdana", 60).render("Game Over", True, BLACK)

# Background
background = pygame.image.load(get_asset("AnimatedStreet.png"))

DISPLAYSURF = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Racer - Weighted Coins Task")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load(get_asset("Enemy.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.bottom > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load(get_asset("Player.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    """Requirement 1: Randomly generating coins with different weights."""
    def __init__(self, enemy_group):
        super().__init__()
        self.enemy_group = enemy_group
        # Define weights and their corresponding images/values
        self.weights = {
            "silver": {"value": 1, "scale": (25, 25)},
            "gold":   {"value": 5, "scale": (35, 35)}
        }
        self.image_orig = pygame.image.load(get_asset("coin.png")) 
        self.rect = self.image_orig.get_rect()
        self.reset()

    def reset(self):
        # Weighted selection: Gold is rarer (20% chance)
        self.type = random.choices(["silver", "gold"], weights=[80, 20])[0]
        self.weight_value = self.weights[self.type]["value"]
        
        # Scale image based on weight
        new_size = self.weights[self.type]["scale"]
        self.image = pygame.transform.scale(self.image_orig, new_size)
        
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        
        # Ensure it doesn't spawn on top of the enemy
        while pygame.sprite.spritecollideany(self, self.enemy_group):
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            self.reset()

# --- SETUP ---
P1 = Player()
E1 = Enemy()
enemies = pygame.sprite.Group()
enemies.add(E1)

C1 = Coin(enemies)
coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))
    
    # Requirement 3: Comments added throughout code.
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    coin_text = font_small.render("Coins: " + str(COIN_SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 110, 10))

    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)
        
    # Handling Coin Collection
    if pygame.sprite.spritecollide(P1, coins, False):
        COIN_SCORE += C1.weight_value # Add the specific weight of the coin
        
        # Requirement 2: Increase speed when player earns N coins.
        if COIN_SCORE // N_COINS_FOR_SPEEDUP > (COIN_SCORE - C1.weight_value) // N_COINS_FOR_SPEEDUP:
            SPEED += 1 
            
        C1.reset()

    # Enemy Collision
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound(get_asset('crash.wav')).play()
        time.sleep(1)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()        
        
    pygame.display.update()
    FramePerSec.tick(FPS)
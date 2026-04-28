import pygame, sys
from pygame.locals import *
import random, time
import os
from UI import UIManager

pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Road Racer")
FramePerSec = pygame.time.Clock()

font_s = pygame.font.SysFont("Verdana", 18)
font_l = pygame.font.SysFont("Verdana", 35)
ui = UIManager(DISPLAYSURF, font_s, font_l)

def get_asset(filename):
    return os.path.join(os.path.dirname(__file__), "assets", filename)

LANES = [65, 200, 335]

# --- CLASSES ---
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(get_asset("Enemy.png"))
        self.rect = self.image.get_rect()
        self.reset()
    def reset(self):
        self.rect.center = (random.choice(LANES), random.randint(-600, -100))
    def move(self, speed):
        self.rect.move_ip(0, speed * 1.2)
        if self.rect.top > 600: self.reset()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(get_asset("Player.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (200, 520)
        self.move_speed = 5
    def move(self):
        pressed = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed[K_LEFT]: self.rect.move_ip(-self.move_speed, 0)
        if self.rect.right < SCREEN_WIDTH and pressed[K_RIGHT]: self.rect.move_ip(self.move_speed, 0)

class Barrier(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(get_asset("Barrier.png"))
        self.rect = self.image.get_rect()
        self.reset()
    def reset(self):
        self.rect.center = (random.choice(LANES), random.randint(-1200, -200))
    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > 600: self.reset()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        size = (40, 40)
        self.imgs = {
            "Nitro": pygame.transform.scale(pygame.image.load(get_asset("Nitro.png")), size),
            "Shield": pygame.transform.scale(pygame.image.load(get_asset("Shield.png")), size),
            "Reset": pygame.transform.scale(pygame.image.load(get_asset("Reset.png")), size)
        }
        self.reset()
    def reset(self):
        self.type = random.choice(list(self.imgs.keys()))
        self.image = self.imgs[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = (random.choice(LANES), random.randint(-1500, -800))
        self.spawn_time = pygame.time.get_ticks()
    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > 600 or (pygame.time.get_ticks() - self.spawn_time > 5000):
            self.reset()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load(get_asset("coin.png"))
        self.image = pygame.transform.scale(img, (30, 30))
        self.rect = self.image.get_rect()
        self.reset()
    def reset(self):
        self.rect.center = (random.choice(LANES), random.randint(-900, -100))
    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > 600: self.reset()

class Oil(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(get_asset("Oil.png"))
        self.rect = self.image.get_rect()
        self.reset()
    def reset(self):
        self.rect.center = (random.choice(LANES), random.randint(-2000, -500))
    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > 600: self.reset()

def run_game():
    USER_NAME = ui.get_username()
    
    # This block immediately applies the loaded preferences to the new game session
    diff_multipliers = {"Easy": 0.7, "Normal": 1.0, "Hard": 1.5}
    multiplier = diff_multipliers.get(ui.difficulty, 1.0)
    
    BASE_SPEED = 5 * multiplier
    SPEED = BASE_SPEED
    COIN_SCORE = 0
    TOTAL_DISTANCE = 0
    FINISH_LINE = 5000
    ACTIVE_POWERUP, HAS_SHIELD, POWER_TIMER = None, False, 0
    bg_y = 0
    
    # Initialize all sprites
    P1 = Player(); E1 = Enemy(); B1 = Barrier(); C1 = Coin(); PU1 = PowerUp(); O1 = Oil()

    hazards = pygame.sprite.Group(E1, B1)
    powerups = pygame.sprite.Group(PU1)
    coins = pygame.sprite.Group(C1)
    oil_group = pygame.sprite.Group(O1)
    # Add O1 to all_sprites so it is drawn and moved
    all_sprites = pygame.sprite.Group(O1, C1, PU1, B1, E1, P1)

    INC_SPEED = pygame.USEREVENT + 1
    pygame.time.set_timer(INC_SPEED, 1000)

    try: background = pygame.image.load(get_asset("AnimatedStreet.png"))
    except: background = pygame.Surface((400, 600)); background.fill((100,100,100))

    running = True
    while running:
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == INC_SPEED: SPEED += (0.05 * multiplier)
            if event.type == QUIT: pygame.quit(); sys.exit()

        bg_y += SPEED
        TOTAL_DISTANCE += SPEED / 10
        if bg_y >= SCREEN_HEIGHT: bg_y = 0
        DISPLAYSURF.blit(background, (0, bg_y))
        DISPLAYSURF.blit(background, (0, bg_y - SCREEN_HEIGHT))

        # Power-up Timer Logic
        if ACTIVE_POWERUP == "Nitro" and now > POWER_TIMER:
            ACTIVE_POWERUP = None; SPEED -= 5

        # Update and Draw Sprites
        for s in all_sprites:
            if s == P1: s.move()
            else: s.move(SPEED)
            DISPLAYSURF.blit(s.image, s.rect)

        # UI Scoreboard
        score = int((COIN_SCORE * 100) + TOTAL_DISTANCE)
        DISPLAYSURF.blit(font_s.render(f"Score: {score}", True, (0,0,0)), (10, 10))
        DISPLAYSURF.blit(font_s.render(f"Dist: {int(TOTAL_DISTANCE)}m", True, (0,0,0)), (10, 35))
        
        if HAS_SHIELD or ACTIVE_POWERUP:
            txt = ACTIVE_POWERUP if ACTIVE_POWERUP else "Shield Active"
            DISPLAYSURF.blit(font_s.render(txt, True, (0,0,200)), (10, 60))
        
        # 1. Oil Slick Collision (Slows player movement speed)
        if pygame.sprite.spritecollideany(P1, oil_group):
            P1.move_speed = 2 # Harder to steer
        else:
            P1.move_speed = 5

        # 2. Coin Collision (Increases game speed)
        if pygame.sprite.spritecollide(P1, coins, False):
            COIN_SCORE += 1
            SPEED += (0.4 * multiplier) 
            C1.reset()

        # 3. Power-Up Collision
        if pygame.sprite.spritecollide(P1, powerups, False):
            if not ACTIVE_POWERUP and not HAS_SHIELD:
                if PU1.type == "Nitro": 
                    ACTIVE_POWERUP = "Nitro"; SPEED += 5; POWER_TIMER = now + 5000
                elif PU1.type == "Shield": HAS_SHIELD = True
                elif PU1.type == "Reset": E1.reset(); B1.reset()
                PU1.reset()

        # 4. Hazard Collision
        hit = pygame.sprite.spritecollideany(P1, hazards)
        if hit or TOTAL_DISTANCE >= FINISH_LINE:
            if hit and HAS_SHIELD:
                HAS_SHIELD = False; hit.reset()
            else:
                if ui.sound_on:
                    try: pygame.mixer.Sound(get_asset("crash.wav")).play()
                    except: pass
                ui.save_score(USER_NAME, score, TOTAL_DISTANCE)
                ui.show_leaderboard()
                running = False

        pygame.display.update()
        FramePerSec.tick(60)

while True:
    choice = ui.main_menu()
    if choice == "play":
        run_game()
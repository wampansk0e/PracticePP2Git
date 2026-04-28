import pygame
import time
import random

# Initializing pygame
pygame.init()

# Colors
WHITE  = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK  = (0, 0, 0)
RED    = (213, 50, 80)
GOLD   = (255, 215, 0) 
GREEN  = (0, 255, 0)

# Screen Dimensions
WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20

dis = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Advanced Snake - Input Fix')

clock = pygame.time.Clock()
score_font = pygame.font.SysFont("verdana", 25)

def display_ui(score, level):
    value = score_font.render(f"Score: {score}  Level: {level}", True, YELLOW)
    dis.blit(value, [10, 10])

def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, GREEN, [x[0], x[1], BLOCK_SIZE, BLOCK_SIZE])

class Food:
    def __init__(self, snake_list):
        self.snake_list = snake_list
        self.spawn()

    def spawn(self):
        # Ensure food doesn't land on snake
        while True:
            self.x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 20.0) * 20.0
            self.y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 20.0) * 20.0
            if [self.x, self.y] not in self.snake_list:
                break
        
        # Random weights (Gold 20%, Silver 80%)
        self.type = random.choices(['silver', 'gold'], weights=[80, 20])[0]
        self.color = GOLD if self.type == 'gold' else RED
        self.weight = 3 if self.type == 'gold' else 1
        
        # Timer logic
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 5000 

    def draw(self):
        pygame.draw.rect(dis, self.color, [self.x, self.y, BLOCK_SIZE, BLOCK_SIZE])

    def check_timer(self):
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.spawn()

def gameLoop():
    game_over = False
    game_close = False

    x1, y1 = WIDTH / 2, HEIGHT / 2
    x1_change, y1_change = BLOCK_SIZE, 0 # Start moving Right
    
    # Input Fix
    current_dir = "RIGHT" 
    direction_queue = [] 

    snake_List = []
    Length_of_snake = 1
    score, level, speed = 0, 1, 10 
    
    target_food = Food(snake_List)

    while not game_over:
        while game_close:
            dis.fill(BLACK)
            msg = score_font.render("Game Over! C-Play Again or Q-Quit", True, RED)
            dis.blit(msg, [WIDTH / 6, HEIGHT / 3])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: game_over, game_close = True, False
                    if event.key == pygame.K_c: gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                last_intended = direction_queue[-1] if direction_queue else current_dir

                if event.key == pygame.K_UP and last_intended != "DOWN":
                    direction_queue.append("UP")
                elif event.key == pygame.K_DOWN and last_intended != "UP":
                    direction_queue.append("DOWN")
                elif event.key == pygame.K_LEFT and last_intended != "RIGHT":
                    direction_queue.append("LEFT")
                elif event.key == pygame.K_RIGHT and last_intended != "LEFT":
                    direction_queue.append("RIGHT")

        # Process the next move from the buffer
        if direction_queue:
            next_move = direction_queue.pop(0)
            current_dir = next_move
            if next_move == "LEFT": x1_change, y1_change = -BLOCK_SIZE, 0
            elif next_move == "RIGHT": x1_change, y1_change = BLOCK_SIZE, 0
            elif next_move == "UP": y1_change, x1_change = -BLOCK_SIZE, 0
            elif next_move == "DOWN": y1_change, x1_change = BLOCK_SIZE, 0

        # Border collision check
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        dis.fill(BLACK)
        
        target_food.check_timer()
        target_food.draw()
        
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake: del snake_List[0]

        # Self-collision check
        for x in snake_List[:-1]:
            if x == snake_Head: game_close = True

        draw_snake(snake_List)
        display_ui(score, level)
        pygame.display.update()

        # Speed/Level logic
        if x1 == target_food.x and y1 == target_food.y:
            score += target_food.weight
            Length_of_snake += 1
            if score // 5 >= level: 
                level += 1
                speed += 2 
            target_food.spawn()

        clock.tick(speed)

    pygame.quit()
    quit()

gameLoop()
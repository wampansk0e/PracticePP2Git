import pygame
import time
import random

# Initializing pygame
pygame.init()

# Define Colors (Using tuples for RGB values)
WHITE  = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK  = (0, 0, 0)
RED    = (213, 50, 80)
GREEN  = (0, 255, 0)

# Screen Dimensions
WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20 # Size of each snake segment and food item

dis = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game - Lab Task')

clock = pygame.time.Clock()

# Setting up Fonts
score_font = pygame.font.SysFont("verdana", 25)

def display_ui(score, level):
    """Requirement 5: Displays current score and level in the top-left corner."""
    value = score_font.render(f"Score: {score}  Level: {level}", True, YELLOW)
    dis.blit(value, [10, 10])

def draw_snake(snake_list):
    """Requirement 6: Draws the snake body segments."""
    for x in snake_list:
        pygame.draw.rect(dis, GREEN, [x[0], x[1], BLOCK_SIZE, BLOCK_SIZE])

def get_random_food_pos(snake_list):
    """Requirement 2: Generates food position ensuring it doesn't fall on snake."""
    while True:
        # Generate coordinates aligned to the grid (multiples of 20)
        foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 20.0) * 20.0
        foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 20.0) * 20.0
        
        # Check if the food position is currently occupied by the snake
        if [foodx, foody] not in snake_list:
            return foodx, foody

def gameLoop():
    game_over = False
    game_close = False

    # Snake starting position
    x1 = WIDTH / 2
    y1 = HEIGHT / 2
    
    # Movement variables
    x1_change = 0
    y1_change = 0
    
    # Direction Control
    current_dir = None
    direction_queue = [] # Buffers inputs to prevent accidental self-collisions

    snake_List = []
    Length_of_snake = 1
    
    # Game Stats
    score = 0
    level = 1
    speed = 10 # Initial Speed

    # Generate first food position
    foodx, foody = get_random_food_pos(snake_List)

    while not game_over:

        # Screen displayed after losing
        while game_close == True:
            dis.fill(BLACK)
            msg = score_font.render("Game Over! C-Play Again or Q-Quit", True, RED)
            dis.blit(msg, [WIDTH / 6, HEIGHT / 3])
            display_ui(score, level)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # --- INPUT HANDLING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                # Add inputs to a queue to process them sequentially
                if event.key == pygame.K_LEFT: direction_queue.append("LEFT")
                elif event.key == pygame.K_RIGHT: direction_queue.append("RIGHT")
                elif event.key == pygame.K_UP: direction_queue.append("UP")
                elif event.key == pygame.K_DOWN: direction_queue.append("DOWN")

        # Process the next valid movement from the queue
        if direction_queue:
            next_move = direction_queue.pop(0)
            # Logic check: Prevent 180-degree turns (e.g., can't go Left if moving Right)
            if next_move == "LEFT" and current_dir != "RIGHT":
                x1_change = -BLOCK_SIZE
                y1_change = 0
                current_dir = "LEFT"
            elif next_move == "RIGHT" and current_dir != "LEFT":
                x1_change = BLOCK_SIZE
                y1_change = 0
                current_dir = "RIGHT"
            elif next_move == "UP" and current_dir != "DOWN":
                y1_change = -BLOCK_SIZE
                x1_change = 0
                current_dir = "UP"
            elif next_move == "DOWN" and current_dir != "UP":
                y1_change = BLOCK_SIZE
                x1_change = 0
                current_dir = "DOWN"

        # Requirement 1: Checking for border (wall) collision
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True
        
        x1 += x1_change
        y1 += y1_change
        dis.fill(BLACK)
        
        # Draw Food
        pygame.draw.rect(dis, RED, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])
        
        # Manage Snake Body
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Check for self-collision (hitting your own body)
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        draw_snake(snake_List)
        display_ui(score, level) # Requirement 5

        pygame.display.update()

        # Check if snake consumes food
        if x1 == foodx and y1 == foody:
            foodx, foody = get_random_food_pos(snake_List) # Requirement 2
            Length_of_snake += 1
            score += 1
            
            # Requirement 3 & 4: Increase level and speed every 3 points
            if score % 3 == 0:
                level += 1
                speed += 2 

        # Control the game speed based on the current level
        clock.tick(speed)

    pygame.quit()
    quit()

# Execute the game
gameLoop()
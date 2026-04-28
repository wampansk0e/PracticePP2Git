import pygame
import random
import leaderboard

WIDTH, HEIGHT, BLOCK_SIZE = 600, 400, 20
BLACK, WHITE, YELLOW, RED = (0,0,0), (255,255,255), (255,255,102), (213,50,80)
GOLD, GREEN, DARK_RED = (255,215,0), (0,255,0), (139,0,0)
BLUE, CYAN, PURPLE, GRAY = (0,0,255), (0,255,255), (128,0,128), (100,100,100)

class Food:
    def __init__(self, snake, walls):
        self.snake, self.walls = snake, walls
        self.spawn()
    def spawn(self):
        while True:
            self.x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 20.0) * 20.0
            self.y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 20.0) * 20.0
            if [self.x, self.y] not in self.snake and [self.x, self.y] not in self.walls: break
        self.type = random.choices(['silver', 'gold', 'poison'], weights=[70, 20, 10])[0]
        self.color = DARK_RED if self.type == 'poison' else GOLD if self.type == 'gold' else RED
        self.weight = 3 if self.type == 'gold' else 0 if self.type == 'poison' else 1
        self.spawn_time, self.lifetime = pygame.time.get_ticks(), 5000 
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, [self.x, self.y, BLOCK_SIZE, BLOCK_SIZE])

class PowerUp:
    def __init__(self, snake, walls):
        self.snake, self.walls = snake, walls
        self.active = False
    def spawn(self):
        while True:
            self.x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 20.0) * 20.0
            self.y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 20.0) * 20.0
            if [self.x, self.y] not in self.snake and [self.x, self.y] not in self.walls: break
        self.type = random.choice(['speed', 'slow', 'shield'])
        self.color = BLUE if self.type == 'speed' else CYAN if self.type == 'slow' else PURPLE
        self.active, self.spawn_time = True, pygame.time.get_ticks()
    def update(self):
        if self.active and pygame.time.get_ticks() - self.spawn_time > 8000: self.active = False
    def draw(self, surface):
        if self.active: pygame.draw.rect(surface, self.color, [self.x, self.y, BLOCK_SIZE, BLOCK_SIZE])

class SnakeGame:
    def __init__(self, screen, username, prefs):
        self.screen, self.username, self.prefs = screen, username, prefs
        self.clock = pygame.time.Clock()
        self.pb = leaderboard.get_personal_best(username)
        self.ui_font = pygame.font.SysFont("verdana", 18)
        self.reset()

    def reset(self):
        self.x, self.y = WIDTH/2, HEIGHT/2
        self.dx, self.dy = BLOCK_SIZE, 0
        self.current_dir, self.queue = "RIGHT", []
        self.snake, self.length = [], 1
        self.score, self.level, self.base_speed = 0, 1, 10
        self.current_speed, self.power_timer, self.shield = 10, 0, False
        self.walls = []
        self.food = Food(self.snake, self.walls)
        self.p_up = PowerUp(self.snake, self.walls)

    def generate_walls(self):
        """Creates obstacles for Level 3+ and ensures snake isn't trapped."""
        self.walls = []
        if self.level >= 3:
            num_blocks = (self.level - 2) * 5
            while len(self.walls) < num_blocks:
                wx = round(random.randrange(0, WIDTH-BLOCK_SIZE)/20.0)*20.0
                wy = round(random.randrange(0, HEIGHT-BLOCK_SIZE)/20.0)*20.0
                # Give snake head a 3-block breathing room
                if abs(wx - self.x) > BLOCK_SIZE * 3 or abs(wy - self.y) > BLOCK_SIZE * 3:
                    if [wx, wy] not in self.walls: self.walls.append([wx, wy])

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            last = self.queue[-1] if self.queue else self.current_dir
            if event.key == pygame.K_UP and last != "DOWN": self.queue.append("UP")
            elif event.key == pygame.K_DOWN and last != "UP": self.queue.append("DOWN")
            elif event.key == pygame.K_LEFT and last != "RIGHT": self.queue.append("LEFT")
            elif event.key == pygame.K_RIGHT and last != "LEFT": self.queue.append("RIGHT")

    def update(self):
        if self.queue:
            self.current_dir = self.queue.pop(0)
            if self.current_dir == "UP": self.dx, self.dy = 0, -BLOCK_SIZE
            elif self.current_dir == "DOWN": self.dx, self.dy = 0, BLOCK_SIZE
            elif self.current_dir == "LEFT": self.dx, self.dy = -BLOCK_SIZE, 0
            elif self.current_dir == "RIGHT": self.dx, self.dy = BLOCK_SIZE, 0

        self.x += self.dx; self.y += self.dy

        # Power-up timer logic
        if self.power_timer > 0 and pygame.time.get_ticks() > self.power_timer:
            self.current_speed, self.power_timer = self.base_speed, 0

        # Collision Check
        hit_wall = [self.x, self.y] in self.walls
        out_bounds = (self.x < 0 or self.x >= WIDTH or self.y < 0 or self.y >= HEIGHT)
        hit_self = [self.x, self.y] in self.snake[:-1]

        if hit_wall or out_bounds or hit_self:
            if self.shield:
                self.shield = False; self.x -= self.dx; self.y -= self.dy
            else:
                leaderboard.save_game_result(self.username, self.score, self.level)
                return True
        
        self.snake.append([self.x, self.y])
        if len(self.snake) > self.length: del self.snake[0]

        # Pick up Food
        if self.x == self.food.x and self.y == self.food.y:
            if self.food.type == 'poison':
                self.length -= 2
                if self.length <= 1: 
                    leaderboard.save_game_result(self.username, self.score, self.level)
                    return True
                self.snake = self.snake[2:] if len(self.snake) > 2 else self.snake[1:]
            else:
                self.score += self.food.weight; self.length += 1
                if self.score // 5 >= self.level:
                    self.level += 1; self.base_speed += 2
                    self.generate_walls() # TRIGGER OBSTACLES
            self.food.spawn()
            if random.random() < 0.2: self.p_up.spawn()

        # Pick up Power-up
        if self.p_up.active and self.x == self.p_up.x and self.y == self.p_up.y:
            if self.p_up.type == 'speed': 
                self.current_speed, self.power_timer = self.base_speed + 5, pygame.time.get_ticks() + 5000
            elif self.p_up.type == 'slow':
                self.current_speed, self.power_timer = max(5, self.base_speed - 4), pygame.time.get_ticks() + 5000
            elif self.p_up.type == 'shield': self.shield = True
            self.p_up.active = False

        self.p_up.update()
        if pygame.time.get_ticks() - self.food.spawn_time > self.food.lifetime: self.food.spawn()
        return False

    def draw(self):
        self.screen.fill(BLACK)
        if self.prefs.get("grid_overlay"):
            for i in range(0, WIDTH, BLOCK_SIZE): pygame.draw.line(self.screen, (30,30,30), (i,0), (i,HEIGHT))
            for i in range(0, HEIGHT, BLOCK_SIZE): pygame.draw.line(self.screen, (30,30,30), (0,i), (WIDTH,i))
        
        for w in self.walls: pygame.draw.rect(self.screen, GRAY, [w[0], w[1], BLOCK_SIZE, BLOCK_SIZE])
        self.food.draw(self.screen)
        self.p_up.draw(self.screen)
        
        color = CYAN if self.shield else self.prefs.get("snake_color", GREEN)
        for s in self.snake: pygame.draw.rect(self.screen, color, [s[0], s[1], BLOCK_SIZE, BLOCK_SIZE])
        
        # Draw UI Text
        self.screen.blit(self.ui_font.render(f"Score: {self.score}", True, YELLOW), [10, 10])
        self.screen.blit(self.ui_font.render(f"Lvl: {self.level}", True, WHITE), [WIDTH - 80, 10])
        self.screen.blit(self.ui_font.render(f"Best: {self.pb}", True, GOLD), [10, 35])
        
        pygame.display.update()
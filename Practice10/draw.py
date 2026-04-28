import pygame

# Initialize Pygame
pygame.init()

# Define some basic colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def main():
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Paint Clone")
    clock = pygame.time.Clock()
    
    # Tool settings
    mode = 'rectangle'  # Options: 'rectangle', 'circle', 'eraser'
    color = RED         # Current drawing color
    drawing = False     # Tracks if mouse button is held down
    start_pos = None    # Where the mouse was first clicked
    
    # Surface to keep the actual drawings
    canvas = pygame.Surface((800, 600))
    canvas.fill(BLACK)
    
    while True:
        # 4. Color Selection Logic
        # Press R for Red, G for Green, B for Blue
        pressed = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            # Key mappings for tools
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: color = RED
                elif event.key == pygame.K_g: color = GREEN
                elif event.key == pygame.K_b: color = BLUE
                elif event.key == pygame.K_1: mode = 'rectangle'
                elif event.key == pygame.K_2: mode = 'circle'
                elif event.key == pygame.K_3: mode = 'eraser'
                elif event.key == pygame.K_ESCAPE: return

            # Mouse Logic
            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start_pos = event.pos
            
            if event.type == pygame.MOUSEBUTTONUP:
                if drawing and start_pos:
                    end_pos = event.pos
                    
                    # 1. Draw Rectangle
                    if mode == 'rectangle':
                        x = min(start_pos[0], end_pos[0])
                        y = min(start_pos[1], end_pos[1])
                        width = abs(start_pos[0] - end_pos[0])
                        height = abs(start_pos[1] - end_pos[1])
                        pygame.draw.rect(canvas, color, (x, y, width, height), 2)
                    
                    # 2. Draw Circle
                    elif mode == 'circle':
                        radius = int(((start_pos[0] - end_pos[0])**2 + (start_pos[1] - end_pos[1])**2)**0.5)
                        pygame.draw.circle(canvas, color, start_pos, radius, 2)
                
                drawing = False
                start_pos = None

            # 3. Eraser Logic
            if event.type == pygame.MOUSEMOTION and drawing:
                if mode == 'eraser':
                    # Erasing is essentially drawing in the background color (BLACK)
                    pygame.draw.circle(canvas, BLACK, event.pos, 20)

        # Rendering
        screen.fill(BLACK)
        screen.blit(canvas, (0, 0))
        
        # UI Hints
        font = pygame.font.SysFont("Arial", 18)
        hint = font.render(f"Mode: {mode.upper()} | Color keys: R, G, B | Tool keys: 1 (Rect), 2 (Circle), 3 (Eraser)", True, WHITE)
        screen.blit(hint, (10, 10))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
import pygame
import math

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def main():
    # Set up the display
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Paint - Final Lab Task")
    clock = pygame.time.Clock()
    font_ui = pygame.font.SysFont("Arial", 16)
    
    # State variables
    mode = 'rectangle' # Default tool
    color = RED        # Default color
    drawing = False
    start_pos = None
    
    # Persistent canvas to store drawings
    canvas = pygame.Surface((800, 600))
    canvas.fill(BLACK)
    
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            # Keyboard Logic: Tool and Color selection
            if event.type == pygame.KEYDOWN:
                # Color Selection
                if event.key == pygame.K_r: color = RED
                elif event.key == pygame.K_g: color = GREEN
                elif event.key == pygame.K_b: color = BLUE
                
                # Basic Tools
                elif event.key == pygame.K_1: mode = 'rectangle'
                elif event.key == pygame.K_2: mode = 'circle'
                elif event.key == pygame.K_3: mode = 'eraser'
                
                # Extra Shapes
                elif event.key == pygame.K_4: mode = 'square'
                elif event.key == pygame.K_5: mode = 'right_triangle'
                elif event.key == pygame.K_6: mode = 'equilateral_triangle'
                elif event.key == pygame.K_7: mode = 'rhombus'
                
                elif event.key == pygame.K_ESCAPE:
                    return

            # Mouse Logic for drawing shapes
            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start_pos = event.pos
            
            if event.type == pygame.MOUSEBUTTONUP:
                if drawing and start_pos:
                    end_pos = event.pos
                    dx = end_pos[0] - start_pos[0]
                    dy = end_pos[1] - start_pos[1]
                    
                    # 1. Rectangle
                    if mode == 'rectangle':
                        rect = pygame.Rect(min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]), abs(dx), abs(dy))
                        pygame.draw.rect(canvas, color, rect, 2)
                    
                    # 2. Circle
                    elif mode == 'circle':
                        radius = int(math.sqrt(dx**2 + dy**2))
                        pygame.draw.circle(canvas, color, start_pos, radius, 2)
                    
                    # 3. Square
                    elif mode == 'square':
                        side = max(abs(dx), abs(dy))
                        rect = pygame.Rect(start_pos[0], start_pos[1], side, side)
                        pygame.draw.rect(canvas, color, rect, 2)
                    
                    # 4. Right Triangle
                    elif mode == 'right_triangle':
                        points = [start_pos, (start_pos[0], end_pos[1]), end_pos]
                        pygame.draw.polygon(canvas, color, points, 2)
                        
                    # 5. Equilateral Triangle
                    elif mode == 'equilateral_triangle':
                        side = math.sqrt(dx**2 + dy**2)
                        height = (math.sqrt(3)/2) * side
                        p2 = (start_pos[0] + side, start_pos[1])
                        p3 = (start_pos[0] + side/2, start_pos[1] - height)
                        pygame.draw.polygon(canvas, color, [start_pos, p2, p3], 2)

                    # 6. Rhombus
                    elif mode == 'rhombus':
                        points = [
                            (start_pos[0] + dx/2, start_pos[1]), # Top
                            (start_pos[0] + dx, start_pos[1] + dy/2), # Right
                            (start_pos[0] + dx/2, start_pos[1] + dy), # Bottom
                            (start_pos[0], start_pos[1] + dy/2)  # Left
                        ]
                        pygame.draw.polygon(canvas, color, points, 2)
                
                drawing = False

            # 7. Eraser Logic
            if event.type == pygame.MOUSEMOTION and drawing:
                if mode == 'eraser':
                    pygame.draw.circle(canvas, BLACK, event.pos, 20)

        # Rendering
        screen.fill(BLACK)
        screen.blit(canvas, (0, 0))
        
        # UI Instruction Text
        instructions = [
            f"Active Mode: {mode.upper()}",
            "Colors: R (Red), G (Green), B (Blue)",
            "1: Rect, 2: Circle, 3: Eraser",
            "4: Square, 5: Right Tri, 6: Equi Tri, 7: Rhombus"
        ]
        for i, text in enumerate(instructions):
            text_surf = font_ui.render(text, True, WHITE)
            screen.blit(text_surf, (10, 10 + (i * 20)))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
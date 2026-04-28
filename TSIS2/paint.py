import pygame
from datetime import datetime
from tools import flood_fill, draw_rhombus, draw_right_triangle, draw_equilateral_triangle

# Initialize
pygame.init()
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
RED, GREEN, BLUE = (255, 0, 0), (0, 255, 0), (0, 0, 255)

def main():
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Paint v2.0")
    clock = pygame.time.Clock()
    font_ui = pygame.font.SysFont("Arial", 14)
    font_canvas = pygame.font.SysFont("Arial", 24) #

    # State
    mode, color, thickness = 'pencil', RED, 2 #
    drawing, canvas = False, pygame.Surface((800, 600))
    canvas.fill(BLACK)
    start_pos, last_pos = None, None
    text_buffer, is_typing, text_pos = "", False, None

    while True:
        ctrl = pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return

            # Text Tool Handling
            if is_typing and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    canvas.blit(font_canvas.render(text_buffer, True, color), text_pos)
                    is_typing = False
                elif event.key == pygame.K_ESCAPE: is_typing = False
                elif event.key == pygame.K_BACKSPACE: text_buffer = text_buffer[:-1]
                else: text_buffer += event.unicode
                continue

            if event.type == pygame.KEYDOWN:
                # 3.4 Save with datetime
                if event.key == pygame.K_s and ctrl:
                    name = f"paint_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    pygame.image.save(canvas, name)
                
                # Shortcuts
                elif event.key == pygame.K_1: thickness = 2
                elif event.key == pygame.K_2: thickness = 5
                elif event.key == pygame.K_3: thickness = 10
                elif event.key == pygame.K_r: color = RED
                elif event.key == pygame.K_g: color = GREEN
                elif event.key == pygame.K_b: color = BLUE
                elif event.key == pygame.K_p: mode = 'pencil'
                elif event.key == pygame.K_l: mode = 'line'
                elif event.key == pygame.K_f: mode = 'fill'
                elif event.key == pygame.K_t: mode = 'text'
                elif event.key == pygame.K_x: mode = 'eraser'
                elif event.key == pygame.K_q: mode = 'square'
                elif event.key == pygame.K_v: mode = 'triangle' # Right triangle
                elif event.key == pygame.K_e: mode = 'equi' # Equilateral
                elif event.key == pygame.K_h: mode = 'rhombus'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if mode == 'fill': flood_fill(canvas, event.pos[0], event.pos[1], color)
                elif mode == 'text': is_typing, text_pos, text_buffer = True, event.pos, ""
                else: drawing = True; start_pos = last_pos = event.pos
            
            if event.type == pygame.MOUSEMOTION and drawing:
                if mode == 'pencil': #
                    pygame.draw.line(canvas, color, last_pos, event.pos, thickness)
                    last_pos = event.pos
                elif mode == 'eraser':
                    pygame.draw.circle(canvas, BLACK, event.pos, thickness * 5)

            if event.type == pygame.MOUSEBUTTONUP and drawing:
                # Final shape rendering
                if mode == 'line': pygame.draw.line(canvas, color, start_pos, event.pos, thickness)
                elif mode == 'square':
                    s = max(abs(event.pos[0]-start_pos[0]), abs(event.pos[1]-start_pos[1]))
                    pygame.draw.rect(canvas, color, (start_pos[0], start_pos[1], s, s), thickness)
                elif mode == 'rhombus': draw_rhombus(canvas, color, start_pos, event.pos, thickness)
                elif mode == 'triangle': draw_right_triangle(canvas, color, start_pos, event.pos, thickness)
                elif mode == 'equi': draw_equilateral_triangle(canvas, color, start_pos, event.pos, thickness)
                drawing = False

        # Display
        screen.fill(BLACK)
        screen.blit(canvas, (0, 0))
        if is_typing: screen.blit(font_canvas.render(text_buffer + "|", True, color), text_pos)
        
        ui = [f"TOOL: {mode.upper()}", "P:Pencil L:Line F:Fill T:Text X:Eraser", "Q:Square V:Tri E:Equi H:Rhombus", "1,2,3:Size | R,G,B:Color | Ctrl+S:Save"]
        for i, text in enumerate(ui): screen.blit(font_ui.render(text, True, WHITE), (10, 10 + (i * 18)))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__": main()
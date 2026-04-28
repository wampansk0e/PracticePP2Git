import pygame
import math

def flood_fill(surface, x, y, new_color):
    """3.3 Fill Tool: Fills closed areas using Surface.get_at/set_at."""
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return
    stack, width, height = [(x, y)], *surface.get_size()
    while stack:
        curr_x, curr_y = stack.pop()
        if 0 <= curr_x < width and 0 <= curr_y < height:
            if surface.get_at((curr_x, curr_y)) == target_color:
                surface.set_at((curr_x, curr_y), new_color)
                stack.extend([(curr_x+1, curr_y), (curr_x-1, curr_y), (curr_x, curr_y+1), (curr_x, curr_y-1)])

def draw_rhombus(surface, color, start_pos, end_pos, thickness):
    """Draws a rhombus centered in the drag bounding box."""
    dx, dy = end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]
    points = [
        (start_pos[0] + dx / 2, start_pos[1]),
        (start_pos[0] + dx, start_pos[1] + dy / 2),
        (start_pos[0] + dx / 2, start_pos[1] + dy),
        (start_pos[0], start_pos[1] + dy / 2)
    ]
    pygame.draw.polygon(surface, color, points, thickness)

def draw_right_triangle(surface, color, start_pos, end_pos, thickness):
    """Draws a right triangle based on mouse drag."""
    points = [start_pos, (start_pos[0], end_pos[1]), end_pos]
    pygame.draw.polygon(surface, color, points, thickness)

def draw_equilateral_triangle(surface, color, start_pos, end_pos, thickness):
    """Draws an equilateral triangle using math for the height."""
    dx, dy = end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]
    side = math.sqrt(dx**2 + dy**2)
    height = (math.sqrt(3) / 2) * side
    points = [start_pos, (start_pos[0] + side, start_pos[1]), (start_pos[0] + side / 2, start_pos[1] - height)]
    pygame.draw.polygon(surface, color, points, thickness)
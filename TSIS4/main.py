import pygame
import sys
import leaderboard
import settings 
from game import SnakeGame, WIDTH, HEIGHT, BLACK, WHITE, GOLD, RED

pygame.init()
dis = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Advanced Lab')

font_big = pygame.font.SysFont("verdana", 25)
font_small = pygame.font.SysFont("verdana", 18)

user_prefs = settings.load_settings()

def settings_menu():
    global user_prefs
    while True:
        dis.fill(BLACK)
        dis.blit(font_big.render("SETTINGS", True, GOLD), [WIDTH/2.8, 50])
        
        grid_status = "ON" if user_prefs["grid_overlay"] else "OFF"
        dis.blit(font_small.render(f"1. Grid Overlay: {grid_status}", True, WHITE), [WIDTH/4, 150])
        dis.blit(font_small.render("Press B to Save & Back", True, RED), [WIDTH/4, 250])
        
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    user_prefs["grid_overlay"] = not user_prefs["grid_overlay"]
                if event.key == pygame.K_b:
                    settings.save_settings(user_prefs)
                    return

def main_menu():
    name = ""
    while True:
        dis.fill(BLACK)
        prompt = font_big.render("Enter Name: " + name + "_", True, WHITE)
        dis.blit(prompt, [WIDTH / 6, HEIGHT / 2.5])
        
        # Updated Navigation Hints for keys 1 and 2
        hints = [
            "Press ENTER to Start",
            "Press 1 for Settings",
            "Press 2 for Leaderboard"
        ]
        for i, text in enumerate(hints):
            hint_surf = font_small.render(text, True, GOLD)
            dis.blit(hint_surf, [WIDTH / 6, HEIGHT / 1.7 + (i * 30)])
            
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name:
                    return name
                elif event.key == pygame.K_1: # Key changed to 1
                    settings_menu()
                elif event.key == pygame.K_2: # Key changed to 2
                    leaderboard.show_leaderboard(dis)
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 12 and event.unicode.isalnum():
                        name += event.unicode

if __name__ == "__main__":
    while True:
        user = main_menu()
        game = SnakeGame(dis, user, user_prefs)
        
        over = False
        while not over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                game.handle_event(event)
            
            over = game.update()
            game.draw()
            game.clock.tick(game.current_speed)
        
        leaderboard.show_leaderboard(dis)
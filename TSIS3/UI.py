import pygame
import json
import os

class UIManager:
    def __init__(self, screen, font_small, font_large):
        self.screen = screen
        self.font_small = font_small
        self.font_large = font_large
        self.leaderboard_file = "leaderboard.json"
        self.settings_file = "settings.json"
        
        # Default Settings
        self.difficulty = "Normal" 
        self.sound_on = True
        
        # Load saved settings immediately at startup
        self.load_settings()
        
        self.colors = {
            "BLACK": (0, 0, 0), "WHITE": (255, 255, 255), 
            "BLUE": (0, 0, 200), "RED": (200, 0, 0), "GRAY": (220, 220, 220)
        }

    def load_settings(self):
        """Loads settings from settings.json if it exists."""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r") as f:
                    data = json.load(f)
                    self.difficulty = data.get("difficulty", "Normal")
                    self.sound_on = data.get("sound_on", True)
            except:
                pass # Fallback to defaults if file is corrupted

    def save_settings(self):
        """Saves current settings to settings.json."""
        data = {
            "difficulty": self.difficulty,
            "sound_on": self.sound_on
        }
        with open(self.settings_file, "w") as f:
            json.dump(data, f, indent=4)

    def draw_button(self, text, y_pos, width=220):
        rect = pygame.Rect((400 // 2 - width // 2), y_pos, width, 50)
        pygame.draw.rect(self.screen, self.colors["GRAY"], rect, border_radius=10)
        pygame.draw.rect(self.screen, self.colors["BLACK"], rect, 2, border_radius=10)
        surf = self.font_small.render(text, True, self.colors["BLACK"])
        self.screen.blit(surf, surf.get_rect(center=rect.center))
        return rect

    def main_menu(self):
        while True:
            self.screen.fill(self.colors["WHITE"])
            title = self.font_large.render("ROAD RACER", True, self.colors["BLUE"])
            self.screen.blit(title, title.get_rect(center=(200, 80)))

            btn_play = self.draw_button("PLAY", 180)
            btn_settings = self.draw_button("SETTINGS", 250)
            btn_lead = self.draw_button("LEADERBOARD", 320)
            btn_quit = self.draw_button("QUIT", 390)

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if btn_play.collidepoint(pos): return "play"
                    if btn_settings.collidepoint(pos): self.settings_menu()
                    if btn_lead.collidepoint(pos): self.show_leaderboard()
                    if btn_quit.collidepoint(pos): pygame.quit(); exit()

    def settings_menu(self):
        while True:
            self.screen.fill(self.colors["WHITE"])
            title = self.font_small.render("SETTINGS", True, self.colors["BLACK"])
            self.screen.blit(title, (150, 50))

            btn_diff = self.draw_button(f"Difficulty: {self.difficulty}", 150)
            btn_sound = self.draw_button(f"Sound: {'ON' if self.sound_on else 'OFF'}", 220)
            btn_back = self.draw_button("BACK", 400)

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if btn_diff.collidepoint(pos):
                        diffs = ["Easy", "Normal", "Hard"]
                        self.difficulty = diffs[(diffs.index(self.difficulty) + 1) % 3]
                        self.save_settings() # Save immediately after change
                    if btn_sound.collidepoint(pos):
                        self.sound_on = not self.sound_on
                        self.save_settings() # Save immediately after change
                    if btn_back.collidepoint(pos): return

    def get_username(self):
        name = ""
        while True:
            self.screen.fill(self.colors["WHITE"])
            prompt = self.font_small.render("ENTER NAME:", True, self.colors["BLACK"])
            name_surf = self.font_large.render(name, True, self.colors["BLUE"])
            self.screen.blit(prompt, (50, 200))
            self.screen.blit(name_surf, (50, 250))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(name) > 0: return name
                    elif event.key == pygame.K_BACKSPACE: name = name[:-1]
                    else: 
                        if len(name) < 10: name += event.unicode

    def save_score(self, name, score, distance):
        data = []
        if os.path.exists(self.leaderboard_file):
            with open(self.leaderboard_file, "r") as f:
                try: data = json.load(f)
                except: data = []
        data.append({"name": name, "score": int(score), "distance": int(distance)})
        data = sorted(data, key=lambda x: x['score'], reverse=True)[:10]
        with open(self.leaderboard_file, "w") as f:
            json.dump(data, f, indent=4)

    def show_leaderboard(self):
        while True:
            self.screen.fill(self.colors["WHITE"])
            title = self.font_small.render("TOP 10 SCORES", True, self.colors["RED"])
            self.screen.blit(title, (30, 30))
            if os.path.exists(self.leaderboard_file):
                with open(self.leaderboard_file, "r") as f:
                    try:
                        data = json.load(f)
                        for i, entry in enumerate(data):
                            txt = f"{i+1}. {entry['name']} - {entry['score']} pts"
                            self.screen.blit(self.font_small.render(txt, True, (0,0,0)), (30, 70 + (i*30)))
                    except: pass
            btn_back = self.draw_button("BACK", 500)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_back.collidepoint(pygame.mouse.get_pos()): return
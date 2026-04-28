import pygame
import os


class MusicPlayer:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        # Screen
        self.WIDTH, self.HEIGHT = 1000, 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Music Player")

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (50, 100, 255)
        self.GREEN = (50, 200, 50)
        self.RED = (220, 50, 50)

        # Fonts
        self.title_font = pygame.font.SysFont("Arial", 40)
        self.info_font = pygame.font.SysFont("Arial", 28)
        self.small_font = pygame.font.SysFont("Arial", 22)

        # Playlist
        self.music_folder = "music"
        self.playlist = self.load_playlist()

        self.current_track_index = 0
        self.is_playing = False

        # Track length
        self.track_length = 0

        if self.playlist:
            self.load_track(self.current_track_index)

    def load_playlist(self):
        tracks = []

        if os.path.exists(self.music_folder):
            for file in os.listdir(self.music_folder):
                if file.endswith(".mp3") or file.endswith(".wav"):
                    tracks.append(os.path.join(self.music_folder, file))

        tracks.sort()
        return tracks

    def load_track(self, index):
        if not self.playlist:
            return

        pygame.mixer.music.load(self.playlist[index])

        # Get track length
        sound = pygame.mixer.Sound(self.playlist[index])
        self.track_length = sound.get_length()

    def play_music(self):
        if self.playlist:
            pygame.mixer.music.play()
            self.is_playing = True

    def stop_music(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        if not self.playlist:
            return

        self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
        self.load_track(self.current_track_index)
        self.play_music()

    def previous_track(self):
        if not self.playlist:
            return

        self.current_track_index = (self.current_track_index - 1) % len(self.playlist)
        self.load_track(self.current_track_index)
        self.play_music()

    def draw_progress_bar(self):
        if not self.is_playing:
            progress = 0
        else:
            current_time = pygame.mixer.music.get_pos() / 1000
            progress = min(current_time / self.track_length, 1) if self.track_length > 0 else 0

        bar_x = 150
        bar_y = 400
        bar_width = 600
        bar_height = 20

        pygame.draw.rect(self.screen, self.BLACK, (bar_x, bar_y, bar_width, bar_height), 2)
        pygame.draw.rect(
            self.screen,
            self.GREEN,
            (bar_x, bar_y, bar_width * progress, bar_height)
        )

        # Time display
        current_seconds = int(pygame.mixer.music.get_pos() / 1000) if self.is_playing else 0
        total_seconds = int(self.track_length)

        time_text = f"{current_seconds}s / {total_seconds}s"
        time_surface = self.small_font.render(time_text, True, self.BLACK)
        self.screen.blit(time_surface, (bar_x, bar_y + 30))

    def draw_ui(self):
        self.screen.fill(self.WHITE)

        # Title
        title = self.title_font.render("Music Player", True, self.BLUE)
        self.screen.blit(title, (330, 40))

        # Current track
        if self.playlist:
            track_name = os.path.basename(self.playlist[self.current_track_index])
        else:
            track_name = "No music files found"

        track_text = self.info_font.render(f"Current Track: {track_name}", True, self.BLACK)
        self.screen.blit(track_text, (100, 150))

        # Status
        status = "Playing" if self.is_playing else "Stopped"
        status_color = self.GREEN if self.is_playing else self.RED

        status_text = self.info_font.render(f"Status: {status}", True, status_color)
        self.screen.blit(status_text, (100, 220))

        # Controls
        controls = [
            "P = Play",
            "S = Stop",
            "N = Next",
            "B = Previous",
            "Q = Quit"
        ]

        y = 500
        for control in controls:
            control_text = self.small_font.render(control, True, self.BLACK)
            self.screen.blit(control_text, (100, y))
            y += 30

        # Progress bar
        self.draw_progress_bar()

        pygame.display.flip()

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.play_music()

                    elif event.key == pygame.K_s:
                        self.stop_music()

                    elif event.key == pygame.K_n:
                        self.next_track()

                    elif event.key == pygame.K_b:
                        self.previous_track()

                    elif event.key == pygame.K_q:
                        running = False

            self.draw_ui()
            clock.tick(30)

        pygame.quit()
import pygame
import math
import datetime
import os


class MickeyClock:
    def __init__(self):
        pygame.init()

        # Screen
        self.WIDTH, self.HEIGHT = 800, 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Mickey's Clock")

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        # Center
        self.CENTER = (self.WIDTH // 2, self.HEIGHT // 2)

        # Clock settings
        self.CLOCK_RADIUS = 250
        self.SECOND_HAND_LENGTH = 120
        self.MINUTE_HAND_LENGTH = 150

        # Font
        self.font = pygame.font.SysFont("Arial", 60)

        # Load hand image
        image_path = os.path.join("images", "mickey_hand.png")
        self.left_hand_original = pygame.image.load(image_path).convert_alpha()

        # Keep aspect ratio
        original_width = self.left_hand_original.get_width()
        original_height = self.left_hand_original.get_height()

        desired_height = 180
        scale_ratio = desired_height / original_height
        new_width = int(original_width * scale_ratio)

        self.left_hand_original = pygame.transform.scale(
            self.left_hand_original,
            (new_width, desired_height)
        )

        # Right hand
        self.right_hand_original = pygame.transform.flip(
            self.left_hand_original, True, False
        )

    def get_angle(self, value):
        return value * 6

    def rotate_hand(self, image, angle, length):
        rotated = pygame.transform.rotate(image, -angle)

        rad = math.radians(angle - 90)

        x = self.CENTER[0] + math.cos(rad) * length
        y = self.CENTER[1] + math.sin(rad) * length

        rect = rotated.get_rect(center=(x, y))
        self.screen.blit(rotated, rect)

    def draw_clock_face(self):
        self.screen.fill(self.WHITE)

        # Outer circle
        pygame.draw.circle(
            self.screen,
            self.BLACK,
            self.CENTER,
            self.CLOCK_RADIUS,
            4
        )

        # Tick marks
        for i in range(60):
            angle = math.radians(i * 6 - 90)

            outer_x = self.CENTER[0] + math.cos(angle) * self.CLOCK_RADIUS
            outer_y = self.CENTER[1] + math.sin(angle) * self.CLOCK_RADIUS

            inner_length = self.CLOCK_RADIUS - (25 if i % 5 == 0 else 10)

            inner_x = self.CENTER[0] + math.cos(angle) * inner_length
            inner_y = self.CENTER[1] + math.sin(angle) * inner_length

            pygame.draw.line(
                self.screen,
                self.BLACK,
                (inner_x, inner_y),
                (outer_x, outer_y),
                3 if i % 5 == 0 else 1
            )

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            now = datetime.datetime.now()

            minutes = now.minute
            seconds = now.second

            minute_angle = self.get_angle(minutes)
            second_angle = self.get_angle(seconds)

            # Draw clock
            self.draw_clock_face()

            # Left hand = seconds
            self.rotate_hand(
                self.left_hand_original,
                second_angle,
                self.SECOND_HAND_LENGTH
            )

            # Right hand = minutes
            self.rotate_hand(
                self.right_hand_original,
                minute_angle,
                self.MINUTE_HAND_LENGTH
            )

            # Center point
            pygame.draw.circle(
                self.screen,
                self.BLACK,
                self.CENTER,
                8
            )

            # Digital time
            time_text = f"{minutes:02}:{seconds:02}"
            text_surface = self.font.render(
                time_text,
                True,
                self.BLACK
            )

            text_rect = text_surface.get_rect(
                center=(self.WIDTH // 2, self.HEIGHT - 70)
            )

            self.screen.blit(text_surface, text_rect)

            pygame.display.flip()

            # Real-time update
            clock.tick(1)

        pygame.quit()
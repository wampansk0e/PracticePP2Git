import pygame
import sys
from ball import Ball

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball Game")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)

my_ball = Ball(WIDTH, HEIGHT)

def main():
    while True:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

       
        keys = pygame.key.get_pressed()
        
        speed = 3 
        
        if keys[pygame.K_UP]:
            my_ball.move(0, -speed)
        if keys[pygame.K_DOWN]:
            my_ball.move(0, speed)
        if keys[pygame.K_LEFT]:
            my_ball.move(-speed, 0)
        if keys[pygame.K_RIGHT]:
            my_ball.move(speed, 0)

        # 3. Drawing
        my_ball.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
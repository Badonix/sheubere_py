import pygame
import sys


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("FUCKING GAME")
        self.WIDTH = 700
        self.HEIGHT = 1080
        self.Y_OFFSET = 100
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.img = pygame.image.load("data/images/clouds/cloud_1.png")
        self.img.set_colorkey((0, 0, 0))
        self.movement = [False, False]
        self.start_pos = [
            self.screen.get_width() / 2 - self.img.get_width() / 2,
            self.screen.get_height() - self.Y_OFFSET,
        ]
        self.collision_area = pygame.Rect(
            self.start_pos[0] - 100, self.start_pos[1] - self.Y_OFFSET, 50, 300
        )
        self.img_pos = self.start_pos

    def run(self):
        while True:
            self.screen.fill((14, 219, 248))
            img_r = pygame.Rect(
                self.img_pos[0],
                self.img_pos[1],
                self.img.get_width(),
                self.img.get_height(),
            )
            # Checking collisions
            if img_r.colliderect(self.collision_area):
                pygame.draw.rect(self.screen, (0, 100, 255), self.collision_area)
            else:
                pygame.draw.rect(self.screen, (0, 50, 155), self.collision_area)

            # This is some GENIUS shit to move Left or Right based on keys (booleans are casted to ints and...)
            self.img_pos[0] += (self.movement[1] - self.movement[0]) * 5
            self.screen.blit(self.img, self.img_pos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
            pygame.display.update()
            self.clock.tick(60)


Game().run()

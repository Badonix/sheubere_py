import pygame
import random
import math


class TrashEnemy:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def move(self, height, screen_width, offset_y=0):

        self.rect.y += 2
        if offset_y < 0:
            self.rect.y -= offset_y

        if self.rect.y > height:
            self.rect.y = random.randint(-100, 0)
            self.rect.x = random.randint(0, screen_width - self.rect.width)

    def draw(self, screen, image):
        screen.blit(image, self.rect)

    def update_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)

    @staticmethod
    def check_distance(rect1, rect2, threshold):
        distance = math.sqrt((rect1.x - rect2.x) ** 2 +
                             (rect1.y - rect2.y) ** 2)
        return distance > threshold

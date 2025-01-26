
import pygame
import random


class Wave:
    def __init__(self, screen_width, image, height=200, pull_force=0.4, speed=1):
        self.width = screen_width
        self.height = height
        self.color = (0, 255, 255)
        self.pull_force = pull_force
        self.speed = speed
        self.active = False
        self.movement = [0, 0]
        self.image_left = image
        self.image_right = pygame.transform.flip(image, True, False)

    def activate(self):
        if self.active:
            return
        self.active = True
        self.y_position = -self.height
        self.direction = random.choice([-1, 1])

    def deactivate(self):
        self.active = False

    def update(self, screen, player, offset_y=0):
        if not self.active:
            return

        # Move the wave down
        self.y_position += self.speed

        if offset_y < 0:
            self.y_position -= offset_y * 0.7

        wave_rect = pygame.Rect(0, self.y_position, self.width, self.height)
        player_rect = player.get_rect()

        if wave_rect.colliderect(player_rect):
            player.is_in_wave = True
            player.velocity_x += self.direction * self.pull_force
            max_speed = 5
            player.velocity_x = max(-max_speed,
                                    min(player.velocity_x, max_speed))
        else:
            self.movement[0] = False
            self.movement[1] = False
            player.is_in_wave = False

        if self.y_position > screen.get_height() + self.height:
            self.deactivate()

    def draw(self, screen):
        """Draws the wave on the screen."""
        if self.active:
            if self.direction == -1:
                screen.blit(self.image_right, (0, self.y_position))
            else:
                screen.blit(self.image_left, (0, self.y_position))

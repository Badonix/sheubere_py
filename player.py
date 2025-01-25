import pygame


class Player:
    def __init__(self, image, width, height, max_speed=10, acceleration=0.5):
        self.image = image
        self.velocity_x = 0
        self.acceleration_x = acceleration
        self.acceleration_y = acceleration
        self.gravity = 0.3
        self.max_speed_x = max_speed
        self.max_speed_y = 1
        self.max_acceleration_y = 2.5
        self.min_acceleration_y = -5
        self.movement = [False, False]
        self.velocity_y = 1
        self.position = [
            width / 2 - image.get_width() / 2,
            height - 200,
        ]

    def handle_input(self, event):
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

    def update(self, screen_width, screen_height):
        if self.movement[0]:
            self.velocity_x -= self.acceleration_x
        if self.movement[1]:
            self.velocity_x += self.acceleration_x
        if not any(self.movement):
            self.velocity_x *= 0.9

        self.velocity_x = max(-self.max_speed_x, min(self.max_speed_x, self.velocity_x))
        self.velocity_y = max(self.max_speed_y, min(self.max_speed_y, self.velocity_y))

        self.velocity_y += self.acceleration_y
        self.position[0] += self.velocity_x
        self.position[1] += self.velocity_y

        self.position[0] = max(
            0, min(screen_width - self.image.get_width(), self.position[0])
        )
        self.position[1] = max(
            0, min(screen_height - self.image.get_height(), self.position[1])
        )

    def draw(self, screen):
        screen.blit(self.image, self.position)

    def get_rect(self):
        return pygame.Rect(
            self.position[0],
            self.position[1],
            self.image.get_width(),
            self.image.get_height(),
        )

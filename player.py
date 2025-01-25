import pygame


class Player:
    def __init__(self, image, start_pos, max_speed=10, acceleration=0.5):
        self.image = image
        self.image.set_colorkey((0, 0, 0))
        self.position = start_pos
        self.velocity_x = 0
        self.acceleration_x = acceleration
        self.acceleration_y = acceleration
        self.gravity = 0.1
        self.max_speed_x = max_speed
        self.max_speed_y = 3
        self.movement = [False, False]  # Left, Right
        self.velocity_y = 1

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
        if self.movement[0]:  # Moving left
            self.velocity_x -= self.acceleration_x
        if self.movement[1]:  # Moving right
            self.velocity_x += self.acceleration_x
        if not any(self.movement):
            self.velocity_x *= 0.9

        self.velocity_y += self.acceleration_y
        self.velocity_x = max(-self.max_speed_x, min(self.max_speed_x, self.velocity_x))
        self.velocity_y = max(-self.max_speed_y, min(self.max_speed_y, self.velocity_y))

        # Update player position
        self.position[0] += self.velocity_x
        self.position[1] += self.velocity_y
        print(self.acceleration_y, self.velocity_y)

        # Keep player within screen bounds
        self.position[0] = max(
            0, min(screen_width - self.image.get_width(), self.position[0])
        )
        self.position[1] = max(
            0, min(screen_height - self.image.get_height(), self.position[1])
        )

    def check_collision(self, enemies):
        player_rect = self.get_rect()
        for enemy in enemies:
            if player_rect.colliderect(enemy.get_rect()):
                return True
        return False

    def draw(self, screen):
        screen.blit(self.image, self.position)

    def get_rect(self):
        return pygame.Rect(
            self.position[0],
            self.position[1],
            self.image.get_width(),
            self.image.get_height(),
        )

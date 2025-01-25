import pygame
import sys
import random
from trash_enemy import TrashEnemy


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sheubere")
        self.WIDTH = 700
        self.HEIGHT = 1080
        self.Y_OFFSET = 100
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.img = pygame.image.load("data/images/player/player.png")
        self.img = pygame.transform.scale(self.img, (80, 80))
        self.img.set_colorkey((0, 0, 0))

        self.player_rect = pygame.Rect(
            self.WIDTH // 2 - 40, self.HEIGHT - self.Y_OFFSET, 80, 80
        )
        self.movement = [False, False]
        self.max_object = 10
        self.min_distance = 100  # Minimum distance between objects

        self.enemies = self.generate_objects(5)
        self.trashes = self.generate_objects(5)

        self.enemy_spawn_timer = 0
        self.trash_spawn_timer = 0

    def generate_objects(self, count):
        """Generate objects ensuring they are not close to each other."""
        objects = []
        for _ in range(count):
            while True:
                new_object = TrashEnemy(
                    random.randint(0, self.WIDTH - 50),
                    random.randint(-300, 0),
                    50,
                    50,
                )
                if all(
                    TrashEnemy.check_distance(
                        new_object.rect, obj.rect, self.min_distance)
                    for obj in objects
                ):
                    objects.append(new_object)
                    break
        return objects

    def run(self):
        while True:
            self.screen.fill((14, 219, 248))

            # Draw and move player
            self.player_rect.x += (self.movement[1] - self.movement[0]) * 5
            self.player_rect.x = max(
                0, min(self.WIDTH - self.player_rect.width, self.player_rect.x)
            )
            self.screen.blit(self.img, self.player_rect)

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

            # Update and draw enemies
            for i, enemy in enumerate(self.enemies):
                enemy.move(self.HEIGHT, self.WIDTH)
                enemyImgStr = f"enemy_{'1' if i % 3 else '2'}.png"
                image = pygame.image.load(f"data/images/enemies/{enemyImgStr}")
                image = pygame.transform.scale(
                    image, (enemy.rect.width, enemy.rect.height)
                )

                enemy.draw(self.screen, image)

                # Check collision with player
                if enemy.check_collision(self.player_rect):
                    print("Game Over!")

            # Spawn new enemies up to the maximum count
            self.enemy_spawn_timer += 1
            if self.enemy_spawn_timer > 120 and len(self.enemies) < self.max_object:
                while True:
                    new_enemy = TrashEnemy(
                        random.randint(0, self.WIDTH - 50),
                        random.randint(-300, 0),
                        50,
                        50,
                    )
                    if all(
                        TrashEnemy.check_distance(
                            new_enemy.rect, enemy.rect, self.min_distance)
                        for enemy in self.enemies
                    ):
                        self.enemies.append(new_enemy)
                        break
                self.enemy_spawn_timer = 0

            # Update and draw trashes
            for i, trash in enumerate(self.trashes):
                trash.move(self.HEIGHT, self.WIDTH)
                trashImgStr = f"trash{'1' if i % 3 else '3'}.png"
                image = pygame.image.load(f"data/images/trash/{trashImgStr}")
                image = pygame.transform.scale(
                    image, (trash.rect.width, trash.rect.height)
                )

                trash.draw(self.screen, image)

                # Check collision with player
                if trash.check_collision(self.player_rect):
                    print("Collect trash")

            # Spawn new trashes up to the maximum count
            self.trash_spawn_timer += 1
            if self.trash_spawn_timer > 120 and len(self.trashes) < self.max_object:
                while True:
                    new_trash = TrashEnemy(
                        random.randint(0, self.WIDTH - 50),
                        random.randint(-300, 0),
                        50,
                        50,
                    )
                    if all(
                        TrashEnemy.check_distance(
                            new_trash.rect, trash.rect, self.min_distance)
                        for trash in self.trashes
                    ):
                        self.trashes.append(new_trash)
                        break
                self.trash_spawn_timer = 0

            pygame.display.update()
            self.clock.tick(60)


Game().run()

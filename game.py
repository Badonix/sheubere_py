import pygame
import sys
import random
import math


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sheubere")
        self.WIDTH = 700
        self.HEIGHT = 1080
        self.Y_OFFSET = 100
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.img = pygame.image.load("data/images/clouds/cloud_1.png")
        self.img.set_colorkey((0, 0, 0))
        self.enemy_img = pygame.image.load(
            "data/images/entities/enemy/idle/00.png")
        self.enemy_img = pygame.transform.scale(self.enemy_img, (50, 50))
        self.movement = [False, False]
        self.start_pos = [
            self.screen.get_width() / 2 - self.img.get_width() / 2,
            self.screen.get_height() - self.Y_OFFSET,
        ]
        self.collision_area = pygame.Rect(
            self.start_pos[0] - 100, self.start_pos[1] - self.Y_OFFSET, 50, 300
        )
        self.img_pos = self.start_pos

        self.enemy = [
            {
                "rect": pygame.Rect(
                    random.randint(0, self.WIDTH -
                                   self.enemy_img.get_width() - 5),
                    random.randint(-300, 0),
                    50,
                    50
                ),
                "direction": random.choice([-1, 1]),
                "space_sensitive": random.choices([True, False], weights=[3, 7])[0],
                "move_count": 0  # Count of moves when spacebar is pressed
            }

            for _ in range(5)
        ]
        self.spawn_timer = 0
        self.max_enemy = 10
        self.isEnemyChange = False

    def collision(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) < 27

    def drawEnemy(self, enemy, i):
        enemyImgStr = f"enemy_{'1' if i % 3 else '2'}.png"
        enemyImg = pygame.image.load(f"data/images/enemies/{enemyImgStr}")
        enemyImg = pygame.transform.scale(enemyImg, (50, 50))
        self.screen.blit(enemyImg, (enemy["rect"].x, enemy["rect"].y))

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
                pygame.draw.rect(self.screen, (0, 100, 255),
                                 self.collision_area)
            else:
                pygame.draw.rect(self.screen, (0, 50, 155),
                                 self.collision_area)

            # Movement logic for the player
            self.img_pos[0] += (self.movement[1] - self.movement[0]) * 5
            self.screen.blit(self.img, self.img_pos)

            if self.img_pos[0] < 12:
                self.img_pos[0] = 12
            if self.img_pos[0] > self.WIDTH - self.img.get_width() - 5:
                self.img_pos[0] = self.WIDTH - self.img.get_width() - 5

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_SPACE:
                        self.isEnemyChange = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_SPACE:
                        self.isEnemyChange = False

            for i, enemy in enumerate(self.enemy):
                self.drawEnemy(enemy, i)

                if self.collision(enemy["rect"].x, enemy["rect"].y, self.img_pos[0], self.img_pos[1]):
                    print("game over simon")

                if enemy["rect"].y > self.HEIGHT:
                    enemy["rect"].y = random.randint(-100, 0)
                    enemy["rect"].x = random.randint(0, self.WIDTH - 50)
                    enemy["move_count"] = 0  # Reset move count

                enemy["rect"].y += 1

                if self.isEnemyChange and enemy["space_sensitive"]:
                    if enemy["move_count"] < 50:  # Limit moves to 50
                        if enemy["rect"].x <= 0:
                            enemy["direction"] = 1
                        elif enemy["rect"].x >= self.WIDTH - enemy["rect"].width:
                            enemy["direction"] = -1

                        enemy["rect"].x += enemy["direction"] * 2
                        enemy["move_count"] += 1  # Increment move count

            # Spawn new enemies up to the maximum count
            self.spawn_timer += 1
            if self.spawn_timer > 120 and len(self.enemy) < self.max_enemy:
                self.enemy.append(
                    {
                        "rect": pygame.Rect(
                            random.randint(0, self.WIDTH - 50),
                            random.randint(-300, 0),
                            50,
                            50
                        ),
                        "direction": 1,
                        "space_sensitive": random.choice([True, False]),
                        "move_count": 0  # New enemies start with 0 moves
                    }
                )
                self.spawn_timer = 0

            pygame.display.update()
            self.clock.tick(60)


Game().run()

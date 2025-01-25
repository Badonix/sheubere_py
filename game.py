from data.scripts.utils import load_image, generate_objects
from player import Player
from blow_listener import blow_listener
import pygame
import sys
import random
import math
from button import Button
import threading

import random

from trash_enemy import TrashEnemy


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Sheubere")

        pygame.display.set_caption("Endless Runner")

        self.WIDTH = 700
        self.HEIGHT = 1080
        self.BUBBLE_WIDTH = 100
        self.BUBBLE_HEIGHT = 100
        self.PLANT_WIDTH = 100
        self.PLANT_HEIGHT = 200
        self.MIN_DISTANCE = 100
        self.Y_OFFSET = 100
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.scroll_speed = 5
        self.max_object = 2
        self.render_offset = 0

        self.enemies = generate_objects(2, self.WIDTH, self.MIN_DISTANCE)
        self.trashes = generate_objects(2, self.WIDTH, self.MIN_DISTANCE)

        self.enemy_spawn_timer = 0
        self.trash_spawn_timer = 0
        self.player_rect = pygame.Rect(
            self.WIDTH // 2 - 40, self.HEIGHT - self.Y_OFFSET, 80, 80
        )

        # ASSETS
        self.assets = {
            "player": load_image("main_bubble.png").convert_alpha(),
            "background": load_image("background_image.png"),
            "plant": load_image("plant.gif"),
            "background_bubbles": load_image("background_bubble.gif"),
        }

        self.assets["background"] = pygame.transform.scale(
            self.assets["background"], (self.WIDTH + 2, self.HEIGHT)
        )
        self.assets["player"] = pygame.transform.scale(
            self.assets["player"], (self.BUBBLE_WIDTH, self.BUBBLE_HEIGHT)
        )
        self.assets["plant"] = pygame.transform.scale(
            self.assets["plant"], (self.PLANT_WIDTH, self.PLANT_HEIGHT)
        )
        self.assets["background_bubbles"].set_alpha(100)

        # Entities
        self.player = Player(self.assets["player"], self.WIDTH, self.HEIGHT)

        # DO NOT TOUCH
        threading.Thread(target=blow_listener, args=(
            self.player,), daemon=True).start()

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

    def drawButton(self, text, image):
        return Button(image, (self.WIDTH / 2, self.HEIGHT / 2), text, 'sans-serif', (255, 255, 255), (250, 250, 250))

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

            # This is some GENIUS shit to move Left or Right based on keys (booleans are casted to ints and...)
            self.img_pos[0] += (self.movement[1] - self.movement[0]) * 5
            self.screen.blit(self.img, self.img_pos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.player.handle_input(event)

            self.screen.blit(
                self.assets["plant"],
                (0, self.HEIGHT - self.assets["plant"].get_height()),
            )
            self.screen.blit(
                self.assets["plant"],
                (
                    self.WIDTH - self.assets["plant"].get_width(),
                    self.HEIGHT - self.assets["plant"].get_height(),
                ),
            )
            self.screen.blit(
                self.assets["background_bubbles"],
                (self.WIDTH -
                 self.assets["background_bubbles"].get_width(), 50),
            )
            self.screen.blit(
                self.assets["background_bubbles"],
                (10, 50),
            )

            # Update and draw enemies
            for i, enemy in enumerate(self.enemies):
                enemy.move(self.HEIGHT, self.WIDTH, self.render_offset)
                enemyImgStr = f"enemy{'1' if i % 3 else '2'}.gif"
                image = pygame.image.load(f"data/images/{enemyImgStr}")
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
                            new_enemy.rect, enemy.rect, self.MIN_DISTANCE
                        )
                        for enemy in self.enemies
                    ):
                        self.enemies.append(new_enemy)
                        break
                self.enemy_spawn_timer = 0

            # Update and draw trashes
            for i, trash in enumerate(self.trashes):
                trash.move(self.HEIGHT, self.WIDTH, self.render_offset)
                trashImgStr = f"trash{'1' if i % 3 else '3'}.png"
                image = pygame.image.load(f"data/images/{trashImgStr}")
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
                            new_trash.rect, trash.rect, self.MIN_DISTANCE
                        )
                        for trash in self.trashes
                    ):
                        self.trashes.append(new_trash)
                        break
                self.trash_spawn_timer = 0
            self.player.update(self.WIDTH, self.HEIGHT)
            self.player.draw(self.screen)
            pygame.display.update()
            self.clock.tick(60)


# Run the game
if __name__ == "__main__":
    Game().run()

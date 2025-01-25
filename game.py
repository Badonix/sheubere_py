from data.scripts.utils import load_image, generate_objects
from player import Player
from blow_listener import blow_listener
import pygame
import sys
import threading

import random

from trash_enemy import TrashEnemy


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Endless Runner")

        self.isRunning = True
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
        self.max_enemy_object = 2
        self.max_trash_object = 2
        self.render_offset = 0

        self.score_font = pygame.font.SysFont('sans-serif', 32)
        self.score = 0

        self.game_over_font = pygame.font.SysFont('sans-serif', 32)
        self.game_over_message = self.game_over_font.render(
            "Game Over", True, (255, 0, 0))

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

    def run(self):
        last_enemy_update_score = 0
        last_trash_update_score = 0

        while self.isRunning:

            self.player_rect = self.player.get_rect()
            self.screen.blit(self.assets["background"], (-2, 0))
            self.render_offset = self.player.get_vy()

            score_text = self.score_font.render(
                f"Score: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))
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
            if self.enemy_spawn_timer > 120 and len(self.enemies) < self.max_enemy_object:

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
                    trash.update_position(random.randint(
                        0, self.WIDTH - 50), random.randint(-300, 0))
                    self.score += 1

            # Spawn new trashes up to the maximum count
            self.trash_spawn_timer += 1
            if self.trash_spawn_timer > 120 and len(self.trashes) < self.max_trash_object:
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

            if self.score >= last_enemy_update_score + 5 and self.score % 5 == 0:
                self.max_enemy_object += 1
                last_enemy_update_score = self.score

            if self.score >= last_trash_update_score + 10 and self.score % 10 == 0:
                self.max_trash_object += 1
                last_trash_update_score = self.score

            self.player.update(self.WIDTH, self.HEIGHT)
            self.player.draw(self.screen)

            pygame.display.update()
            self.clock.tick(60)


# Run the game
if __name__ == "__main__":
    Game().run()

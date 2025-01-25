from data.scripts.utils import (
    is_name_taken,
    load_image,
    generate_objects,
    save_player_name_to_file,
    save_player_to_server,
    update_score_on_server,
)
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

        self.WIDTH = 700
        self.HEIGHT = 1080
        self.BUBBLE_WIDTH = 100
        self.BUBBLE_HEIGHT = 100
        self.PLANT_WIDTH = 100
        self.PLANT_HEIGHT = 200
        self.MIN_DISTANCE = 100
        self.TRASH_SIZE = 50
        self.FISH_SIZE = 80
        self.Y_OFFSET = 100
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.scroll_speed = 5
        self.max_enemy_object = 2
        self.max_trash_object = 2
        self.render_offset = 0

        self.status = "menu"

        self.enemies = generate_objects(
            2, self.WIDTH, self.MIN_DISTANCE, self.FISH_SIZE
        )
        self.trashes = generate_objects(
            2, self.WIDTH, self.MIN_DISTANCE, self.TRASH_SIZE
        )

        self.enemy_spawn_timer = 0
        self.trash_spawn_timer = 0
        self.player_rect = pygame.Rect(
            self.WIDTH // 2 - 40, self.HEIGHT - self.Y_OFFSET, 80, 80
        )

        # ASSETS
        self.assets = {
            "player": load_image("main_bubble.png").convert_alpha(),
            "background": load_image("background_image.png"),
            "game_over_background": load_image("gameover_background.png"),
            "plant": load_image("plant.gif"),
            "start_bubble": load_image("start_bubble.png"),
            "restart": pygame.transform.scale(load_image("restart.png"), (250, 100)),
            "quit": pygame.transform.scale(load_image("quit.png"), (250, 100)),
            "play": pygame.transform.scale(load_image("start.png"), (250, 100)),
            "background_bubbles": load_image("background_bubble.gif"),
        }

        self.assets["background"] = pygame.transform.scale(
            self.assets["background"], (self.WIDTH + 2, self.HEIGHT)
        )
        self.assets["game_over_background"] = pygame.transform.scale(
            self.assets["game_over_background"], (self.WIDTH + 2, self.HEIGHT)
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
        self.restart_button = pygame.Rect(220, 400, 250, 100)
        self.quit_button = pygame.Rect(220, 550, 250, 100)

        # Input
        self.player_name = ""
        self.input_active = not bool(self.player_name)
        self.input_box = pygame.Rect(
            self.WIDTH // 2 - 150, self.HEIGHT // 2 - 50, 300, 50
        )
        self.start_button = pygame.Rect(220, 600, 250, 100)

        self.score = 0

        # TEXTS
        pygame.font.init()

        self.TITLE_FONT = pygame.freetype.Font(
            "data/fonts/ComicNeue-Bold.ttf", 80)
        self.GAME_FONT = pygame.freetype.Font(
            "data/fonts/ComicNeue-Bold.ttf", 50)
        self.NAME_FONT = pygame.freetype.Font(
            "data/fonts/ComicNeue-Bold.ttf", 30)
        self.ERROR_FONT = pygame.freetype.Font(
            "data/fonts/ComicNeue-Bold.ttf", 25)
        self.SCORE_FONT = pygame.freetype.Font(
            "data/fonts/ComicNeue-Bold.ttf", 30)

        self.message = ""
        self.message_color = (255, 0, 0)

        self.last_enemy_update_score = 0
        self.last_trash_update_score = 0

        # DO NOT TOUCH
        threading.Thread(target=blow_listener, args=(
            self.player,), daemon=True).start()

    def reset(self):

        self.enemies = generate_objects(
            2, self.WIDTH, self.MIN_DISTANCE, self.FISH_SIZE
        )
        self.trashes = generate_objects(
            2, self.WIDTH, self.MIN_DISTANCE, self.TRASH_SIZE
        )
        self.score = 0

        self.last_enemy_update_score = 0
        self.last_trash_update_score = 0

        self.player.restart()

    def run(self):
        while True:
            if self.status == "menu":
                self.screen.blit(self.assets["game_over_background"], (-2, 0))
                self.screen.blit(
                    pygame.transform.scale_by(
                        self.assets["start_bubble"], 0.15),
                    (
                        self.WIDTH / 2
                        - self.assets["start_bubble"].get_width() * 0.15 / 2,
                        250,
                    ),
                )
                self.TITLE_FONT.render_to(
                    self.screen,
                    (150, 100),
                    "SHEUBERE",
                    (255, 255, 255),
                )
                self.NAME_FONT.render_to(
                    self.screen,
                    (self.WIDTH // 2 - 150, self.HEIGHT // 2 - 85),
                    "Enter your name",
                    (255, 255, 255),
                )
                if (
                    self.score >= self.last_enemy_update_score + 5
                    and self.score % 5 == 0
                ):
                    self.max_enemy_object += 1
                    self.last_enemy_update_score = self.score
                if (
                    self.score >= self.last_trash_update_score + 10
                    and self.score % 10 == 0
                ):
                    self.max_trash_object += 1
                    self.last_trash_update_score = self.score

                pygame.draw.rect(self.screen, (255, 255, 255),
                                 self.input_box, 2)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.start_button.collidepoint(event.pos):
                            self.status = "playing"
                    if self.input_active and event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if self.player_name:
                                if is_name_taken(self.player_name):
                                    self.message = "Name is already taken!"
                                    self.message_color = (255, 0, 0)
                                else:
                                    self.message = "Name is available!"
                                    self.message_color = (0, 255, 0)
                                    save_player_name_to_file(self.player_name)
                                    save_player_to_server(
                                        {"name": self.player_name, "score": 0}
                                    )
                                    self.input_active = False
                            else:
                                self.message = "Name cannot be empty!"
                                self.message_color = (255, 0, 0)
                            pass
                        elif event.key == pygame.K_BACKSPACE:
                            self.player_name = self.player_name[:-1]
                        else:
                            if len(self.player_name) <= 15:
                                self.player_name += event.unicode

                    if not self.input_active and event.type == pygame.MOUSEBUTTONDOWN:
                        pass
                if self.message == "Name is available!":
                    self.status = "playing"
                if len(self.message) > 0:
                    self.ERROR_FONT.render_to(
                        self.screen,
                        (self.WIDTH // 2 - 120, self.HEIGHT // 2 + 10),
                        self.message,
                        self.message_color,
                    )

                self.NAME_FONT.render_to(
                    self.screen,
                    (self.WIDTH // 2 - 130, self.HEIGHT // 2 - 35),
                    self.player_name,
                    (255, 255, 255),
                )
                self.screen.blit(self.assets["play"], (220, 600))
                pygame.display.update()
                self.clock.tick(60)

            elif self.status == "gameover":
                self.screen.blit(self.assets["game_over_background"], (-2, 0))
                self.GAME_FONT.render_to(
                    self.screen, (220, 150), "Game Over", (255, 255, 255)
                )
                self.GAME_FONT.render_to(
                    self.screen,
                    (190, 250),
                    f"Your score: {self.score}",
                    (255, 255, 255),
                )
                self.screen.blit(self.assets["restart"], (220, 400))
                self.screen.blit(self.assets["quit"], (220, 550))
                pygame.display.update()
                self.clock.tick(60)

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.restart_button.collidepoint(event.pos):
                            self.reset()
                            self.status = "playing"
                        elif self.quit_button.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()

            elif self.status == "playing":
                self.player_rect = self.player.get_rect()
                self.screen.blit(self.assets["background"], (-2, 0))
                self.render_offset = self.player.get_vy()
                if (
                    self.score >= self.last_enemy_update_score + 5
                    and self.score % 5 == 0
                ):
                    self.max_enemy_object += 1
                    self.last_enemy_update_score = self.score
                if (
                    self.score >= self.last_trash_update_score + 10
                    and self.score % 10 == 0
                ):
                    self.max_trash_object += 1
                    self.last_trash_update_score = self.score

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    self.player.handle_input(event)

                self.SCORE_FONT.render_to(
                    self.screen,
                    (10, 10),
                    f"Score: {self.score}",
                    (255, 255, 255),
                )
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
                    enemyImgStr = f"enemy{'1' if i % 3 else '2'}.png"
                    image = pygame.image.load(f"data/images/{enemyImgStr}")
                    image = pygame.transform.scale(
                        image, (enemy.rect.width, enemy.rect.height)
                    )

                    enemy.draw(self.screen, image)

                    # Check collision with player
                    if enemy.check_collision(self.player_rect):
                        print(self.score)
                        update_score_on_server(self.player_name, self.score)
                        self.status = "gameover"

                # Spawn new enemies up to the maximum count
                self.enemy_spawn_timer += 1
                if (
                    self.enemy_spawn_timer > 120
                    and len(self.enemies) < self.max_enemy_object
                ):
                    while True:
                        new_enemy = TrashEnemy(
                            random.randint(0, self.WIDTH - 50),
                            random.randint(-300, 0),
                            self.FISH_SIZE,
                            self.FISH_SIZE,
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
                        trash.update_position(
                            random.randint(0, self.WIDTH -
                                           50), random.randint(-300, 0)
                        )
                        self.score += 1
                        print("Collect trash")

                # Spawn new trashes up to the maximum count
                self.trash_spawn_timer += 1
                if (
                    self.trash_spawn_timer > 120
                    and len(self.trashes) < self.max_trash_object
                ):
                    while True:
                        new_trash = TrashEnemy(
                            random.randint(0, self.WIDTH - 50),
                            random.randint(-300, 0),
                            self.TRASH_SIZE,
                            self.TRASH_SIZE,
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

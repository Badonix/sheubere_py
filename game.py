from data.scripts.utils import (
    Animation,
    is_name_taken,
    load_image,
    generate_objects,
    load_images,
    save_player_name_to_file,
    save_player_to_server,
    update_score_on_server,
)
from player import Player
from blow_listener import blow_listener
import pygame
import sys
import webbrowser
import threading

import random

from trash_enemy import TrashEnemy
from waves import Wave
from sounds import Sounds

BACKGROUND_VOLUME = 0.3

pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
pygame.mixer.music.load("data/sounds/background.mp3")
pygame.mixer.music.set_volume(BACKGROUND_VOLUME)
pygame.mixer.music.play(loops=-1)


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Sheubere")

        self.sounds = Sounds()

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
            2, self.WIDTH, self.MIN_DISTANCE, self.FISH_SIZE, "enemy"
        )
        self.trashes = generate_objects(
            2, self.WIDTH, self.MIN_DISTANCE, self.TRASH_SIZE, "trash"
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
            "background_bubbles_anim": Animation(load_images("bubbles/")),
            "wave": load_image("wave.png"),
            "leaderboard": pygame.transform.scale(
                load_image("leaderboard.png"), (250, 100)
            ),
            "plant_anim": Animation(load_images("plant/")),
        }

        self.wave = Wave(self.WIDTH, self.assets["wave"])
        self.assets["wave"].set_alpha(100)

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

        # Entities
        self.player = Player(self.assets["player"], self.WIDTH, self.HEIGHT)
        self.restart_button = pygame.Rect(220, 400, 250, 100)
        self.quit_button = pygame.Rect(220, 550, 250, 100)
        self.leaderboard_button = pygame.Rect(220, 700, 250, 100)

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
            2, self.WIDTH, self.MIN_DISTANCE, self.FISH_SIZE, "enemy"
        )
        self.trashes = generate_objects(
            2, self.WIDTH, self.MIN_DISTANCE, self.TRASH_SIZE, "trash"
        )
        self.score = 0
        self.player.movement = [0, 0]
        self.wave.deactivate()

        self.last_enemy_update_score = 0
        self.last_trash_update_score = 0

        pygame.mixer.music.set_volume(BACKGROUND_VOLUME)

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
                    (self.WIDTH // 2 - 112, self.HEIGHT // 2 - 85),
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
                    if event.type == pygame.MOUSEBUTTONDOWN and self.player_name != "":
                        if self.start_button.collidepoint(event.pos):
                            self.sounds.click_sound()
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
                                        {"name": self.player_name,
                                            "score": self.score}
                                    )

                                    self.sounds.click_sound()
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
                if len(self.message) > 0 and self.message != "Name is available!":
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
                    (220, 250),
                    f"Recycled: {self.score}",
                    (255, 255, 255),
                )

                self.screen.blit(self.assets["restart"], (220, 400))
                self.screen.blit(self.assets["quit"], (220, 550))
                self.screen.blit(self.assets["leaderboard"], (220, 700))
                pygame.display.update()
                self.clock.tick(60)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.leaderboard_button.collidepoint(event.pos):
                            webbrowser.open("http://localhost:5173")
                        elif self.restart_button.collidepoint(event.pos):
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

                if random.random() < 0.1:  # Adjust probability for wave appearance
                    self.wave.activate()
                self.wave.update(self.screen, self.player, self.render_offset)
                self.wave.draw(self.screen)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    self.player.handle_input(event)
                if (
                    self.player.get_rect().right < 0
                    or self.player.get_rect().left > self.WIDTH
                ):
                    self.status = "gameover"

                self.SCORE_FONT.render_to(
                    self.screen,
                    (10, 10),
                    f"Recycled: {self.score}",
                    (255, 255, 255),
                )

                self.assets["plant_anim"].update()
                current_plant_frame = self.assets["plant_anim"].img()
                self.screen.blit(
                    pygame.transform.scale_by(current_plant_frame, 0.4),
                    (0, self.HEIGHT - current_plant_frame.get_height() * 0.4),
                )
                self.screen.blit(
                    pygame.transform.scale_by(current_plant_frame, 0.4),
                    (
                        self.WIDTH - current_plant_frame.get_width() * 0.4,
                        self.HEIGHT - current_plant_frame.get_height() * 0.4,
                    ),
                )

                self.assets["background_bubbles_anim"].update()
                current_bubble_frame = self.assets["background_bubbles_anim"].img(
                )
                self.screen.blit(
                    current_bubble_frame,
                    (self.WIDTH - current_bubble_frame.get_width(), 50),
                )
                self.screen.blit(current_bubble_frame, (10, 50))

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
                        self.sounds.pop_sound()
                        pygame.mixer.music.set_volume(0.1)
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
                            random.randint(2, 4),
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
                        self.sounds.play_collect()
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
                            random.randint(1, 3),
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

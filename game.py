from data.scripts.utils import load_image
from player import Player
from blow_listener import blow_listener
import pygame
import sys
import threading


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
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.scroll_speed = 5

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
        threading.Thread(target=blow_listener, args=(self.player,), daemon=True).start()

    def run(self):
        while True:
            self.screen.blit(self.assets["background"], (-2, 0))
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
                (self.WIDTH - self.assets["background_bubbles"].get_width(), 50),
            )
            self.screen.blit(
                self.assets["background_bubbles"],
                (10, 50),
            )
            self.player.update(self.WIDTH, self.HEIGHT)
            self.player.draw(self.screen)
            pygame.display.update()
            self.clock.tick(60)


# Run the game
if __name__ == "__main__":
    Game().run()

from data.scripts.utils import load_image
from player import Player
import pygame
import sys


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Endless Runner")

        self.WIDTH = 700
        self.HEIGHT = 1080
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.scroll_speed = 5

        # Assets
        self.assets = {
            "player": load_image("tiles/large_decor/1.png"),
            "enemy": load_image("entities/enemy/idle/00.png"),
        }

        # Initialize player
        start_pos = [
            self.WIDTH / 2 - self.assets["player"].get_width() / 2,
            self.HEIGHT - 200,
        ]
        self.player = Player(self.assets["player"], start_pos)

    def run(self):
        while True:
            self.screen.fill((14, 219, 248))

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.player.handle_input(event)

            # Update and draw player
            self.player.update(self.WIDTH)
            self.player.draw(self.screen)

            # Update display and tick
            pygame.display.update()
            self.clock.tick(60)


# Run the game
if __name__ == "__main__":
    Game().run()

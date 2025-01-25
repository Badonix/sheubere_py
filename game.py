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
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.scroll_speed = 5

        self.assets = {
            "player": load_image("tiles/large_decor/1.png"),
            "enemy": load_image("entities/enemy/idle/00.png"),
        }

        start_pos = [
            self.WIDTH / 2 - self.assets["player"].get_width() / 2,
            self.HEIGHT - 200,
        ]
        self.player = Player(self.assets["player"], start_pos)
        threading.Thread(target=blow_listener, args=(self.player,), daemon=True).start()

    def run(self):
        while True:
            self.screen.fill((14, 219, 248))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.player.handle_input(event)
            self.player.update(self.WIDTH, self.HEIGHT)
            self.player.draw(self.screen)
            pygame.display.update()
            self.clock.tick(60)


# Run the game
if __name__ == "__main__":
    Game().run()

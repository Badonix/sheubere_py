import pygame


class Sounds:

    BACKGROUND_MUSIC_VOLUME = 0.5
    SOUND_BUFFER_SIZE = 2048

    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16,
                          channels=2, buffer=self.SOUND_BUFFER_SIZE)

        # Load sounds
        self.sounds = {
            "collect": pygame.mixer.Sound('data/sounds/collect.mp3'),
            "click": pygame.mixer.Sound('data/sounds/click_bubble_sound.mp3'),
            "pop": pygame.mixer.Sound('data/sounds/bubble_pop_sound.mp3'),
        }

    def play_collect(self):
        channel = pygame.mixer.Channel(2)
        channel.play(self.sounds["collect"])
        channel.set_volume(3)

    def click_sound(self):
        channel = pygame.mixer.Channel(3)
        channel.play(self.sounds["click"])

    def pop_sound(self):
        channel = pygame.mixer.Channel(4)
        channel.play(self.sounds["pop"])

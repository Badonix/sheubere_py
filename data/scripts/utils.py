import pygame
import random
from trash_enemy import TrashEnemy

BASE_IMG_PATH = "data/images/"


def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    return img


def generate_objects(count, width, min_distance):
    """Generate objects ensuring they are not close to each other."""
    objects = []
    for _ in range(count):
        while True:
            new_object = TrashEnemy(
                random.randint(0, width - 50),
                random.randint(-300, 0),
                50,
                50,
            )
            if all(
                TrashEnemy.check_distance(new_object.rect, obj.rect, min_distance)
                for obj in objects
            ):
                objects.append(new_object)
                break
    return objects

import pygame
import os
import json
import requests
import random
from trash_enemy import TrashEnemy

BASE_IMG_PATH = "data/images/"

API_URL = "http://localhost:3000"
SAVE_FILE = "player_name.json"


def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    return img


def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + "/" + img_name))
    return images


def generate_objects(count, width, min_distance, obj_size, type):
    """Generate objects ensuring they are not close to each other."""
    objects = []
    for _ in range(count):
        while True:
            speed = 2
            if type == "trash":
                speed = random.randint(1, 3)
            elif type == "enemy":
                speed = random.randint(2, 4)

            new_object = TrashEnemy(
                random.randint(0, width - 50),
                random.randint(-300, 0),
                obj_size,
                obj_size,
                speed,
            )
            if all(
                TrashEnemy.check_distance(new_object.rect, obj.rect, min_distance)
                for obj in objects
            ):
                objects.append(new_object)
                break
    return objects


def save_player_name_to_file(name):
    with open(SAVE_FILE, "w") as f:
        json.dump({"name": name}, f)


# Load player name from local JSON file
def load_player_name_from_file():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f).get("name", "")
    return ""


# Check if the name is taken via API
def is_name_taken(name):
    try:
        response = requests.get(f"{API_URL}/check_name", params={"name": name})
        if response.status_code == 200:
            return response.json().get("taken", False)
    except requests.RequestException as e:
        print(f"Error contacting the API: {e}")
    return False


# Save player data to the server
def save_player_to_server(player_data):
    try:
        response = requests.post(f"{API_URL}/save_user", json=player_data)
        if response.status_code == 200:
            return response.json().get("success", False)
    except requests.RequestException as e:
        print(f"Error contacting the API: {e}")
    return False


# Update player score on the server
def update_score_on_server(name, score_change):
    try:
        response = requests.post(
            f"{API_URL}/update_score", json={"name": name, "score": score_change}
        )
        if response.status_code == 200:
            return response.json().get("success", False)
    except requests.RequestException as e:
        print(f"Error contacting the API: {e}")
    return False


class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def img(self):
        return self.images[int(self.frame / self.img_duration)]

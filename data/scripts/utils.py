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


def generate_objects(count, width, min_distance, obj_size):
    """Generate objects ensuring they are not close to each other."""
    objects = []
    for _ in range(count):
        while True:
            new_object = TrashEnemy(
                random.randint(0, width - 50),
                random.randint(-300, 0),
                obj_size,
                obj_size,
            )
            if all(
                TrashEnemy.check_distance(
                    new_object.rect, obj.rect, min_distance)
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
            f"{API_URL}/update_score", json={"name": name, "scoreChange": score_change}
        )
        if response.status_code == 200:
            return response.json().get("success", False)
    except requests.RequestException as e:
        print(f"Error contacting the API: {e}")
    return False

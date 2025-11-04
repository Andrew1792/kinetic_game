import pygame
import json
from src.player import Player
from src.level_objects import Platform
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class LevelLoader:

    def __init__(self, player, all_sprites_group, platforms_group, enemies_group):

        self.player = player
        self.all_sprites = all_sprites_group
        self.platforms = platforms_group
        self.enemies = enemies_group

    def load(self, file_path):

        # Clear existing level-specific sprites
        self.all_sprites.empty()
        self.platforms.empty()
        self.enemies.empty()
        
        # --- Always add a floor and ceiling ---
        floor = Platform(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20)
        ceiling = Platform(0, 0, SCREEN_WIDTH, 20)
        self.platforms.add(floor, ceiling)
        self.all_sprites.add(floor, ceiling)

        # --- Load level-specific data from JSON ---
        try:
            with open(f'levels/{file_path}', 'r') as f:
                level_data = json.load(f)

        except FileNotFoundError:
            print(f"Error: Level file not found at {file_path}")
            return None
        
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON in {file_path}")
            return None

        background_color = level_data.get("background_color", "#000000")

        # Load platforms from JSON
        platform_list = level_data.get("platforms", [])
        for plat_data in platform_list:
            platform = Platform(
                plat_data["x"], 
                plat_data["y"], 
                plat_data["width"], 
                plat_data["height"]
            )
            self.platforms.add(platform)
            self.all_sprites.add(platform)
        
        # Reset the player at the start position
        player_data = level_data.get("player_start")
        if not player_data:
            self.player.reset(100, 100)
        else:
            self.player.reset(start_x=player_data["x"], start_y=player_data["y"])
        
        # Add the player to the sprite group
        self.all_sprites.add(self.player)
        
        return background_color
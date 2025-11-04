# src/level_objects.py
import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        
        # The visual
        self.image = pygame.Surface((width, height))
        self.image.fill(pygame.Color("white ")) # Or any color
        
        # The hitbox
        self.rect = self.image.get_rect(topleft=(x, y))
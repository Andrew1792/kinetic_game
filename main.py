import pygame
import sys
from config import *
from src.player import Player
from src.level_loader import LevelLoader 

class Game:
  def __init__(self):
    pygame.init()
    self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    self.clock = pygame.time.Clock()

    # Store a default background color
    self.background_fill = BLACK 

    # --- Create groups and loader FIRST ---
    self.platforms = pygame.sprite.Group()
    self.enemies = pygame.sprite.Group()
    self.all_sprites = pygame.sprite.Group()
    
    # 1. Create the single Player object
    self.player = Player()
    
    # 2. Pass the player INTO the loader
    self.loader = LevelLoader(self.player, self.all_sprites, self.platforms, self.enemies)

    self.setup_game()

  def setup_game(self):
    # --- Use the loader to set up the level ---
    # The loader no longer returns the player, just the background color
    bg_color = self.loader.load("test_level.json")
    self.background_fill = bg_color

    # We check for None on the background color to see if loading failed
    if bg_color is None:
        print("Error: Failed to load level. Exiting.")
        pygame.quit()
        sys.exit()

  def run(self):
    while True:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
        
        # Pass key presses to the player
        self.player.handle_event(event)


      # Update the player (and pass collision groups)
      self.player.update(self.platforms, self.enemies)
      # Update all enemies (if you add any)
      self.enemies.update() 

      # --- Drawing ---
      # Now use the color we saved from the level!
      self.screen.fill(self.background_fill)
      self.all_sprites.draw(self.screen)
      
      pygame.display.flip()
      self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
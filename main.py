import pygame
import sys
from config import *
from src.player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.setup_game()

    def setup_game(self):
        self.player = Player()
        self.all_sprites = pygame.sprite.GroupSingle(self.player)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.player.handle_event(event)

            self.all_sprites.update()
            self.screen.fill(BLACK)
            self.all_sprites.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
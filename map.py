from config import *
import pygame
class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        image_brick = pygame.image.load("images/brick.webp")
        self.image = pygame.transform.scale(image_brick, (self.width, self.height))

        # Ustaw pozycję bloku
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
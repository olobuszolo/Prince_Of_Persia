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

        image_brick = pygame.image.load("resources/images/map_images/bricks.png")
        self.image = pygame.transform.scale(image_brick, (self.width, self.height))

        # Ustaw pozycję bloku
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)


class Door(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.doors
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = 3 * TILESIZE 
        self.height = 4 * TILESIZE

        image_brick = pygame.image.load("resources/images/map_images/door_stairs.png")
        self.image = pygame.transform.scale(image_brick, (self.width, self.height))

        # Ustaw pozycję bloku
        self.rect = self.image.get_rect()
        # self.rect.topleft = (self.x, self.y)
        self.rect.bottomleft = (self.x - 32, self.y + 32)

class Fake(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.fakes
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        image_brick = pygame.image.load("resources/images/map_images/bricks.png")
        self.image = pygame.transform.scale(image_brick, (self.width, self.height))

        # Ustaw pozycję bloku
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)


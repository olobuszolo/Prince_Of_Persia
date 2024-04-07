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
        
        self.is_open = False

        self.image_brick_close = pygame.image.load("resources/images/map_images/door_stairs.png")
        self.image_brick_open = pygame.image.load("resources/images/map_images/door_stairs_open.png")
        self.image = pygame.transform.scale(self.image_brick_close, (self.width, self.height))

        # Ustaw pozycję bloku
        self.rect = self.image.get_rect()
        # self.rect.topleft = (self.x, self.y)
        self.rect.bottomleft = (self.x - 32, self.y + 32)
        
    def update(self):
        if self.game.player.get_next_level_pred():
            if not self.is_open:
                self.image = pygame.transform.scale(self.image_brick_open, (self.width, self.height))
                self.is_open = True
        else:
            if self.is_open:
                self.image = pygame.transform.scale(self.image_brick_close, (self.width, self.height))
                self.is_open = False
            

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


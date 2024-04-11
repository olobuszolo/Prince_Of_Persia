from typing import Any
from config import *
import pygame
import math
class Block(pygame.sprite.Sprite): #B
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks, self.game.collisions
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        image_brick = pygame.image.load("resources/images/map_images/bricks.png")
        self.image = pygame.transform.scale(image_brick, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)


class Door(pygame.sprite.Sprite): #D
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
       

class FallingLeft(pygame.sprite.Sprite): #falling bricks
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.fakes
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = 0.5 * TILESIZE

        self.images = [
            pygame.image.load("resources/images/map_images/fake.png"),
            pygame.image.load("resources/images/map_images/fake1.png"),
            pygame.image.load("resources/images/map_images/fake2.png")
        ]
        self.image_index = 0

        self.image = pygame.transform.scale(self.images[self.image_index], (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

        self.collided = False
        self.next_image_time = pygame.time.get_ticks()
        self.fall_speed = 0
        self.last_change_time = 0

    def activate(self):
        player_y = self.game.player.rect.y
        player_x = self.game.player.rect.x
        if (player_y > self.rect.y + 2*TILESIZE) and (player_x + 2*TILESIZE> self.rect.x):
            self.fall_speed = FALL_SPEED

    def update(self):
        self.activate()

        if not self.collided:
            self.rect.y += self.fall_speed

        collisions = pygame.sprite.spritecollide(self, self.game.all_sprites, False)
        for sprite in collisions:
            if sprite != self:  # Ignoruj kolizję ze sobą samym
                self.collided = True
                break

        if self.collided:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_change_time >= CHANGE_INTERVAL:
                self.image_index += 1
                if self.image_index < len(self.images):
                    self.image = pygame.transform.scale(self.images[self.image_index], (self.width, self.height))
                else:
                    self.kill()
                self.last_change_time = current_time    

class FallingRight(FallingLeft):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

    def activate(self):
            player_y = self.game.player.rect.y
            player_x = self.game.player.rect.x
            if (player_y > self.rect.y + 2*TILESIZE) and (player_x < self.rect.x + 2*TILESIZE):
                self.fall_speed = FALL_SPEED

class Trap(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.fakes
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.images = [
            pygame.image.load("resources/images/map_images/bricks.png"),
        ]
        self.image_index = 0 
        self.image = pygame.transform.scale(self.images[self.image_index], (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

class Spikes(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.spikes
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE * 1.3

        self.image_spike = pygame.image.load("resources/images/map_images/spikes.png")
        self.image = pygame.transform.scale(self.image_spike, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.changing_speed = CHANGE_INTERVAL
        self.last_change_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()

        period = 1000 
        amplitude = TILESIZE / 4
        pulsation = amplitude * math.sin(2 * math.pi * current_time / period)
        
        self.rect.y = self.y + pulsation

class SemiDoors(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.semidoors
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * (TILESIZE) + 31
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE * 2
        self.image_spike = pygame.image.load("resources/images/map_images/halfdoors.png")
        self.image = pygame.transform.scale(self.image_spike, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

class Protection(Block): #makes it impossible to return to lower level
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        self.x = x * TILESIZE - 31
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        image_brick = pygame.image.load("resources/images/map_images/halfdoors.png")
        self.image = pygame.transform.scale(image_brick, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
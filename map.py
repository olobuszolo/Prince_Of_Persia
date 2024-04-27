from typing import Any
from config import *
import pygame
import math
import time

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

        image_brick = pygame.image.load("resources/images/map_images/newbrick.png")
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
        self.damage = True
        self.damage_kill = 32

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
            if sprite != self:
                self.collided = True
                self.damage = False
                break

        if self.collided:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_change_time >= CHANGE_INTERVAL/3:
                self.image_index += 1
                if self.image_index < len(self.images):
                    self.image = pygame.transform.scale(self.images[self.image_index], (self.width, self.height))
                    self.damage = False

                else:
                    self.kill()
                self.last_change_time = current_time   

        collisions = pygame.sprite.spritecollide(self, self.game.all_sprites, False)
        for object in collisions:
            if object != self:
                if not isinstance(object, Block):
                    self.game.player.get_damage(self.damage_kill)
                    self.damage_kill = 0 

class FallingRight(FallingLeft):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

    def activate(self):
            player_y = self.game.player.rect.y
            player_x = self.game.player.rect.x
            if (player_y > self.rect.y + 2*TILESIZE) and (player_x < self.rect.x + 4*TILESIZE):
                self.fall_speed = FALL_SPEED

class FallingLeftBottomUp(FallingLeft):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
    def activate(self):
        player_y = self.game.player.rect.y
        player_x = self.game.player.rect.x
        if ((player_x + 2*TILESIZE> self.rect.x) and (player_y - self.rect.y < 4*TILESIZE)):
            self.fall_speed = FALL_SPEED
    

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
        self.damage = 32
        self.damage_time = 0
        self.inside = False


    def update(self):
        current_time = pygame.time.get_ticks()
        if self.damage == 0:
            if current_time - self.damage_time > 2000:
                self.damage = 32

        period = 1000 
        amplitude = TILESIZE / 4
        pulsation = amplitude * math.sin(2 * math.pi * current_time / period)
        
        self.rect.y = self.y + pulsation

        collisions = pygame.sprite.spritecollide(self, self.game.players, False)
        for object in collisions:
            if object != self:
                if not isinstance(object, Block):
                    if self.damage_time + 2000 < current_time:
                        self.game.player.get_damage(32)
                        self.damage = 0
                        self.damage_time = pygame.time.get_ticks()


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

class NewTrap(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.traps
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.images = [
            pygame.image.load("resources/images/map_images/newbrick.png"),
            pygame.image.load("resources/images/map_images/empty.png")
        ]
        self.image_index = 0

        self.image = pygame.transform.scale(self.images[self.image_index], (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.dissapear_time = 0
        self.blocked = False

    def update(self):
        curr_time = pygame.time.get_ticks()
        if curr_time >= self.dissapear_time + 200:
            self.image_index = 0
            self.blocked = True
            self.image = pygame.transform.scale(self.images[self.image_index], (self.width, self.height))

        collisions = pygame.sprite.spritecollide(self, self.game.all_sprites, False)
        for object in collisions:
            if object != self: 
                self.collision_time = pygame.time.get_ticks()
                self.image_index = 1
                self.image = pygame.transform.scale(self.images[self.image_index], (self.width, self.height))
                self.game.player.trap_status = False

class Lift(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.lift
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE + 15
        self.width = TILESIZE
        self.height = 0.5 * TILESIZE

        self.start_x = x*TILESIZE
        self.start_y = y*TILESIZE

        lift_image = pygame.image.load("resources/images/map_images/fake.png")
        self.image = pygame.transform.scale(lift_image, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

        self.collided = False
        self.next_image_time = pygame.time.get_ticks()
        self.fall_speed = FALL_SPEED 

    def update(self):
        if not self.collided:
            self.rect.y -= self.fall_speed

        collisions = pygame.sprite.spritecollide(self, self.game.blocks, False)

        for sprite in collisions:
            if sprite != self:
                self.collided = True
                break
        if self.collided:
            self.fall_speed = -self.fall_speed 
            self.rect.y = self.rect.y 
            self.collided = False
            if self.game.player.is_on_lift:
                self.game.player.rect.x = self.rect.x - 32
                self.game.player.rect.y = self.rect.y + 4
                self.game.player.is_on_lift = False
        

class UpperPress(Lift):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.groups = self.game.all_sprites, self.game.upper_press
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.start_y = self.y = y * TILESIZE + 15
        self.fall_speed = - FALL_SPEED * 0.5


    def update(self):
        if not self.collided:
            self.rect.y -= self.fall_speed

        collisions = pygame.sprite.spritecollide(self, self.game.blocks, False)

        lift_collision = pygame.sprite.spritecollide(self, self.game.down_press, False)

        for sprite in collisions:
            if sprite != self:
                self.collided = True
                break
        if self.collided:
            self.fall_speed = -self.fall_speed 
            self.rect.y = self.rect.y 
            self.collided = False
        if self.rect.y == self.start_y:
            self.fall_speed = - self.fall_speed

        for sprite in lift_collision:
            if sprite != self:
                self.fall_speed = - self.fall_speed


class DownPress(pygame.sprite.Sprite):  #X
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER + 1
        self.groups = self.game.all_sprites, self.game.down_press
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE + 15
        self.width = TILESIZE
        self.height = 0.5 * TILESIZE

        self.start_y = y * TILESIZE + 15

        lift_image = pygame.image.load("resources/images/map_images/fake.png")
        self.image = pygame.transform.scale(lift_image, (self.width, self.height))

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

        self.collided = False
        self.next_image_time = pygame.time.get_ticks()
        self.fall_speed = FALL_SPEED * 0.5

    def update(self):
        if not self.collided:
            self.rect.y -= self.fall_speed

        collisions = pygame.sprite.spritecollide(self, self.game.upper_press, False)

        for sprite in collisions:
            if sprite != self:
                self.collided = True
                break
        if self.collided:
            self.fall_speed = -self.fall_speed
            self.rect.y -= self.fall_speed 

            self.collided = False
        if self.rect.y >= self.start_y + 32:
            self.fall_speed = -self.fall_speed
            self.rect.y -= self.fall_speed 

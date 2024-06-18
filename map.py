from config import *
import pygame
import math

class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks, self.game.collisions
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = BRICK_IMAGE

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

class MovingBlock(Block):
    """
    This is implementation of press.
    """
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.height = 4 * TILESIZE
        self.width = 2 * TILESIZE
        self.image = PRESS_IMAGE
        self.killing_y = self.y + TILESIZE + 1
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        
        self.direction = 1  
        self.movement_distance = 0
        self.max_distance = 4 * TILESIZE
        self.fall_speed = FALL_SPEED // 2

        self.groups = self.game.all_sprites, self.game.blocks, self.game.collisions, self.game.movingblocks
        pygame.sprite.Sprite.__init__(self, self.groups)

    def update(self):
        self.y += self.direction * self.fall_speed
        self.rect.y = self.y
        self.movement_distance += abs(self.direction * self.fall_speed)

        player_collision = pygame.sprite.spritecollide(self, self.game.players, False)
        if player_collision:
            if self.y in (self.killing_y - 1, self.killing_y + 1):
                self.game.player.press_flag = True

        if self.movement_distance >= self.max_distance:
            self.direction *= -1  
            self.movement_distance = 0

class Gate(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.gate, self.game.collisions
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = BRICK_IMAGE

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

        self.image_brick_close = DOORS_IMAGE_CLOSE
        self.image_brick_open = DOORS_IMAGE_OPEN
        self.image = self.image_brick_close

        self.rect = self.image.get_rect()
        self.rect.bottomleft = (self.x - 32, self.y + 32)
        
    def update(self):
        if self.game.player.get_next_level_pred():
            if not self.is_open:
                self.image = self.image_brick_open
                self.is_open = True
        else:
            if self.is_open:
                self.image = self.image_brick_close
                self.is_open = False

class FallingLeft(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.fakes,self.game.protections
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = 0.5 * TILESIZE

        self.images = FALLING_IMAGES
        self.image_index = 0
        self.image = self.images[self.image_index]


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
        if (player_y > self.rect.y + 2 * TILESIZE) and (player_x + 2 * TILESIZE > self.rect.x):
            self.fall_speed = FALL_SPEED // 2

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
                    self.image = self.images[self.image_index]
                    self.damage = False

                else:
                    self.kill()
                self.last_change_time = current_time   

        collisions = pygame.sprite.spritecollide(self, self.game.players, False)
        if self.damage_kill and collisions:
            self.game.player.get_damage(self.damage_kill)
            self.damage_kill = 0 

class FallingRight(FallingLeft):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

    def activate(self):
            player_y = self.game.player.rect.y
            player_x = self.game.player.rect.x
            if (player_y > self.rect.y + 2 * TILESIZE) and (player_x < self.rect.x + 4 * TILESIZE):
                self.fall_speed = FALL_SPEED

class FallingLeftBottomUp(FallingLeft):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
    def activate(self):
        player_y = self.game.player.rect.y
        player_x = self.game.player.rect.x
        if ((player_x + 2 * TILESIZE > self.rect.x) and (player_y - self.rect.y < 4 * TILESIZE)):
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

        self.image = SPIKES_IMAGE

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

        period = 1000 * 2
        amplitude = TILESIZE / 4
        pulsation = amplitude * math.sin(2 * math.pi * current_time / period)
        
        self.rect.y = self.y + pulsation

        collisions = pygame.sprite.spritecollide(self, self.game.players, False)
        if collisions and self.damage_time + 2000 < current_time:
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
        self.image = EMPTY_IMAGE

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

class Protection(Block):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)

        self.x = x * TILESIZE - 31
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = EMPTY_IMAGE

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

        self.images = [BRICK_IMAGE, EMPTY_IMAGE]
        self.image_index = 0

        self.image = self.images[self.image_index]

        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.dissapear_time = 0
        self.blocked = False

    def update(self):
        curr_time = pygame.time.get_ticks()
        if curr_time >= self.dissapear_time + 200:
            self.image_index = 0
            self.blocked = True
            self.image = self.images[self.image_index]

        collisions = pygame.sprite.spritecollide(self, self.game.players, False)
        if collisions:
            self.collision_time = pygame.time.get_ticks()
            self.image_index = 1
            self.image = self.images[self.image_index]
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

        self.image = FALLING_IMAGES[0]

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

class Fakes(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.fakes
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = EMPTY_IMAGE
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

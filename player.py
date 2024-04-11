import pygame
from config import *
import math
import random

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()
        
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width,height])
        sprite.blit(self.sheet, (0,0), (x,y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite

'''
To move use left and right.
To jump us up. After reaching the door
use down to enter next level.
'''

class Player(pygame.sprite.Sprite):
    def  __init__(self,game,x,y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE # * 2
        self.width = TILESIZE
        self.height = TILESIZE # * 2
        
        self.x_change = 0
        self.y_change = 0
        
        self.is_jump = False
        self.jump_count = PLAYER_JUMP_HEIGHT
        
        self.enter_next_level = False
        self.enter_next_semi_level = False
        self.is_on_trap = False
        
        self.fall = False
        
        self.facing = 'right'
        self.animation_loop = 1
        
        self.image = self.game.character_spritesheet.get_sprite(0,0, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def animate(self):
        # down_animations = [self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height),
        #                    self.game.character_spritesheet.get_sprite(35, 2, self.width, self.height),
        #                    self.game.character_spritesheet.get_sprite(68, 2, self.width, self.height)]

        # up_animations = [self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height),
        #                  self.game.character_spritesheet.get_sprite(35, 34, self.width, self.height),
        #                  self.game.character_spritesheet.get_sprite(68, 34, self.width, self.height)]

        left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)]

        right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)]
        
        # if self.facing == "down":
        #     if self.y_change == 0:
        #         self.image = self.game.character_spritesheet.get_sprite(3, 2, self.width, self.height)
        #     else:
        #         self.image = down_animations[math.floor(self.animation_loop)]
        #         self.animation_loop += 0.1
        #         if self.animation_loop >= 3:
        #             self.animation_loop = 1
                    
        # if self.facing == "up":
        #     if self.y_change == 0:
        #         self.image = self.game.character_spritesheet.get_sprite(3, 34, self.width, self.height)
        #     else:
        #         self.image = up_animations[math.floor(self.animation_loop)]
        #         self.animation_loop += 0.1
        #         if self.animation_loop >= 3:
        #             self.animation_loop = 1
        
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
                        
    def update(self):
        self.movement()
        self.animate()
           
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')

        self.x_change = 0
        self.y_change = 0

        if self.get_next_semi_level_pred():
            self.game.change_level = True
        
    def movement(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            self.x_change -= PLAYER_SPEED
            self.facing = 'left'
            
        if keys[pygame.K_RIGHT]:
            self.x_change += PLAYER_SPEED
            self.facing = 'right'
            
        if not self.is_jump:
            if keys[pygame.K_UP]:
                self.is_jump = True
            else:
                self.y_change += PLAYER_FALL_SPEED
                
        else:
            self.y_change -= (self.jump_count * abs(self.jump_count)) * 0.4
            if self.jump_count >= -10:
                self.jump_count -= 1
    
    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.collisions, False)
            hits_protections = pygame.sprite.spritecollide(self, self.game.protections, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
            if hits_protections:
                if self.x_change > 0:
                    self.rect.x = hits_protections[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits_protections[0].rect.right
                    
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    self.jump_count = PLAYER_JUMP_HEIGHT
                    self.is_jump = False
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    if self.is_jump:
                        self.jump_count = -1
                    
        hits = pygame.sprite.spritecollide(self, self.game.doors, False)
        hits_semi = pygame.sprite.spritecollide(self, self.game.semidoors, False)
        trap_stands = pygame.sprite.spritecollide(self, self.game.traps, False)
        if trap_stands:
            self.is_on_trap = True
        else:
            self.is_on_trap = False

        if hits:
            self.enter_next_level = True
        elif hits_semi:
            self.enter_next_semi_level = True
        else:
            self.enter_next_level = False
            self.enter_next_semi_level = False
            
        hits_traps = pygame.sprite.spritecollide(self, self.game.fakes, False)
        if hits_traps:
            self.game.map_update()

            
    def get_next_level_pred(self):
        return self.enter_next_level

    def get_next_semi_level_pred(self):
        return self.enter_next_semi_level
    
    def get_trap_status_pred(self):
        return self.is_on_trap
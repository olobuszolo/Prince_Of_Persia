import pygame
from config import *
import math
from random import choice

class HealthPotion(pygame.sprite.Sprite): #1
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.potions
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE//2
        self.height = TILESIZE//2
        self.animation_loop = 0
        self.animations = [self.game.red_potion_spritesheet.get_sprite(0,0,self.width,self.height),
                            self.game.red_potion_spritesheet.get_sprite(16,0,self.width,self.height),
                            self.game.red_potion_spritesheet.get_sprite(32,0,self.width,self.height),
                            self.game.red_potion_spritesheet.get_sprite(0,16,self.width,self.height),
                            self.game.red_potion_spritesheet.get_sprite(16,16,self.width,self.height),
                            self.game.red_potion_spritesheet.get_sprite(32,16,self.width,self.height),
                            self.game.red_potion_spritesheet.get_sprite(0,32,self.width,self.height),
                            self.game.red_potion_spritesheet.get_sprite(16,32,self.width,self.height)]

        self.image = self.game.red_potion_spritesheet.get_sprite(0,0,self.width,self.height)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y+10
        
    def update(self):
        self.animate()
    
    def animate(self):
        self.image = self.animations[math.floor(self.animation_loop)]
        self.image = pygame.transform.scale(self.image, (22, 22))
        self.animation_loop += 0.2
        if self.animation_loop >= 8:
            self.animation_loop = 1
    
    def influence(self):
        self.game.player.get_health(choice([8,16,32,64]))
        self.kill()
    
class SpeedPotion(HealthPotion): #2
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.animations = [self.game.blue_potion_spritesheet.get_sprite(0,0,self.width,self.height),
                            self.game.blue_potion_spritesheet.get_sprite(16,0,self.width,self.height),
                            self.game.blue_potion_spritesheet.get_sprite(32,0,self.width,self.height),
                            self.game.blue_potion_spritesheet.get_sprite(0,16,self.width,self.height),
                            self.game.blue_potion_spritesheet.get_sprite(16,16,self.width,self.height),
                            self.game.blue_potion_spritesheet.get_sprite(32,16,self.width,self.height),
                            self.game.blue_potion_spritesheet.get_sprite(0,32,self.width,self.height),
                            self.game.blue_potion_spritesheet.get_sprite(16,32,self.width,self.height)]

        self.image = self.game.blue_potion_spritesheet.get_sprite(0,0,self.width,self.height)
        
    def influence(self):
        self.game.player.speed *= 2
        self.game.player.speed_potion = True
        self.kill()
        
class JumpPotion(HealthPotion): #3 TODO
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.animations = [self.game.green_potion_spritesheet.get_sprite(0,0,self.width,self.height),
                            self.game.green_potion_spritesheet.get_sprite(16,0,self.width,self.height),
                            self.game.green_potion_spritesheet.get_sprite(32,0,self.width,self.height),
                            self.game.green_potion_spritesheet.get_sprite(0,16,self.width,self.height),
                            self.game.green_potion_spritesheet.get_sprite(16,16,self.width,self.height),
                            self.game.green_potion_spritesheet.get_sprite(32,16,self.width,self.height),
                            self.game.green_potion_spritesheet.get_sprite(0,32,self.width,self.height),
                            self.game.green_potion_spritesheet.get_sprite(16,32,self.width,self.height)]

        self.image = self.game.green_potion_spritesheet.get_sprite(0,0,self.width,self.height)

class NoFallDamagePotion(HealthPotion): #4
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.animations = [self.game.yellow_potion_spritesheet.get_sprite(0,0,self.width,self.height),
                            self.game.yellow_potion_spritesheet.get_sprite(16,0,self.width,self.height),
                            self.game.yellow_potion_spritesheet.get_sprite(32,0,self.width,self.height),
                            self.game.yellow_potion_spritesheet.get_sprite(0,16,self.width,self.height),
                            self.game.yellow_potion_spritesheet.get_sprite(16,16,self.width,self.height),
                            self.game.yellow_potion_spritesheet.get_sprite(32,16,self.width,self.height),
                            self.game.yellow_potion_spritesheet.get_sprite(0,32,self.width,self.height),
                            self.game.yellow_potion_spritesheet.get_sprite(16,32,self.width,self.height)]

        self.image = self.game.yellow_potion_spritesheet.get_sprite(0,0,self.width,self.height)
        
    def influence(self):
        self.game.player.no_fall_damage = True
        self.kill()

class DamageResistancePotion(HealthPotion): #5
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.animations = [self.game.purple_potion_spritesheet.get_sprite(0,0,self.width,self.height),
                            self.game.purple_potion_spritesheet.get_sprite(16,0,self.width,self.height),
                            self.game.purple_potion_spritesheet.get_sprite(32,0,self.width,self.height),
                            self.game.purple_potion_spritesheet.get_sprite(0,16,self.width,self.height),
                            self.game.purple_potion_spritesheet.get_sprite(16,16,self.width,self.height),
                            self.game.purple_potion_spritesheet.get_sprite(32,16,self.width,self.height),
                            self.game.purple_potion_spritesheet.get_sprite(0,32,self.width,self.height),
                            self.game.purple_potion_spritesheet.get_sprite(16,32,self.width,self.height)]

        self.image = self.game.purple_potion_spritesheet.get_sprite(0,0,self.width,self.height)
        
    def influence(self):
        self.game.player.damage_resistance = True
        self.kill()

class Description(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE//2
        self.height = TILESIZE//2
        
        self.image = pygame.Surface((25, 25))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y-18
        self.time_to_kill = 0
        
    def update(self):
        if self.time_to_kill<5:
            self.time_to_kill+=.5
        else:
            self.kill()
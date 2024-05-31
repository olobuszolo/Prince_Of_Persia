import pygame
from config import *
import math
from random import choice

"""
All potions refractored but influance in Player to change and placing in game to change.
"""
class AbstractPotion(pygame.sprite.Sprite):
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
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def update(self):
        self.animate()
    
    def animate(self):
        self.image = self.animations[math.floor(self.animation_loop)]
        self.image = pygame.transform.scale(self.image, (22, 22))
        self.animation_loop += 0.2
        if self.animation_loop >= 6:
            self.animation_loop = 1
    
    def influence(self):
        play_sound('resources\\sounds\\potion.wav', 0.3)

class HealthPotion(AbstractPotion):
    def __init__(self, game, x, y):
        super().__init__(game,x,y)
        self.animations = self.game.red_potion_spritesheet.get_sprites(0, 0, self.width, self.height, 3, 2)
        self.image = self.animations[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y+10
    
    def influence(self):
        super().influence()
        self.game.player.get_health(choice([8,16,32,64]))
        self.kill()
    
class SpeedPotion(AbstractPotion):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.animations = self.game.blue_potion_spritesheet.get_sprites(0, 0, self.width, self.height, 3, 2)
        self.image = self.animations[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y+10
        
    def influence(self):
        super().influence()
        self.game.player.speed *= 2
        self.game.player.speed_potion = True
        self.kill()

class NoFallDamagePotion(AbstractPotion):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.animations = self.game.yellow_potion_spritesheet.get_sprites(0, 0, self.width, self.height, 3, 2)
        self.image = self.animations[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y+10
        
    def influence(self):
        super().influence()
        self.game.player.no_fall_damage = True
        self.kill()

class DamageResistancePotion(AbstractPotion):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.animations = self.game.purple_potion_spritesheet.get_sprites(0, 0, self.width, self.height, 3, 2)
        self.image = self.animations[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y+10
        
    def influence(self):
        super().influence()
        self.game.player.damage_resistance = True
        self.kill()


"""
To change sword. Make 2 different class of swords, one for eq one for map.
"""        
class Sword(pygame.sprite.Sprite):
    def __init__(self, game, x, y, typ):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.swords
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.animation_loop = 0
        self.type = typ
        
        if typ == 1:
            self.image = self.game.swords_spritesheet.get_sprite(0,0,self.width,self.height)
            self.attack = PLAYER_DEFAULT_DAMAGE*1.25
        elif typ == 2:
            self.image = self.game.swords_spritesheet.get_sprite(32,0,self.width,self.height)
            self.attack = PLAYER_DEFAULT_DAMAGE*1.5
        elif typ == 3:
            self.image = self.game.swords_spritesheet.get_sprite(64,0,self.width,self.height)
            self.attack = PLAYER_DEFAULT_DAMAGE*1.75
        elif typ == 4:
            self.image = self.game.swords_spritesheet.get_sprite(96,0,self.width,self.height)
            self.attack = PLAYER_DEFAULT_DAMAGE*2
        elif typ == 5:
            self.image = self.game.swords_spritesheet.get_sprite(128,0,self.width,self.height)
            self.attack = PLAYER_DEFAULT_DAMAGE*3
        else:
            self.kill()
            
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def influence(self):
        self.game.player.sword_type = self.type
        self.game.player.damage = self.attack
        self.kill()

"""
Delete Description or use somewhere else.
"""
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
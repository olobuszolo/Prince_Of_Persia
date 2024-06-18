import pygame
from config import *
import math
from random import choice

class Potion(pygame.sprite.Sprite):
    """Abstract class for the potions that the player can collect."""
    def __init__(self, game, x, y, sprite_sheet, influence_action):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.potions
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE // 2
        self.height = TILESIZE // 2
        
        self.animation_loop = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.animations = sprite_sheet.get_sprites(0, 0, self.width, self.height, 3, 2)
        self.image = self.animations[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y + 10
        self.influence_action = influence_action
    
    def update(self):
        self.animate()
    
    def animate(self):
        self.image = self.animations[math.floor(self.animation_loop)]
        self.image = pygame.transform.scale(self.image, (22, 22))
        self.animation_loop += 0.2
        if self.animation_loop >= 6:
            self.animation_loop = 1
    
    def influence(self):
        play_sound(POTION_SOUND_PATH, 0.3)
        self.influence_action()
        self.kill()

class HealthPotion(Potion):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, RED_POTION_SPRITESHEET, self.influence_action)
    
    def influence_action(self):
        self.game.player.get_health(choice([8, 16, 32, 64]))
    
class SpeedPotion(Potion):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, BLUE_POTION_SPRITESHEET, self.influence_action)
    
    def influence_action(self):
        self.game.player.speed *= 2
        self.game.player.speed_potion = True

class NoFallDamagePotion(Potion):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, YELLOW_POTION_SPRITESHEET, self.influence_action)
    
    def influence_action(self):
        self.game.player.no_fall_damage = True

class DamageResistancePotion(Potion):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, PURPLE_POTION_SPRITESHEET, self.influence_action)
    
    def influence_action(self):
        self.game.player.damage_resistance = True
     
class Sword(pygame.sprite.Sprite):
    """Class for the swords that the player can collect."""
    SWORD_TYPES = {
        1: (0, 1.25),
        2: (32, 1.5),
        3: (64, 1.75),
        4: (96, 2),
        5: (128, 3)
    }

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
        
        if typ in self.SWORD_TYPES:
            sprite_x, damage_mult = self.SWORD_TYPES[typ]
            self.image = SWORDS_SPRITESHEET.get_sprite(sprite_x, 0, self.width, self.height)
            self.attack = PLAYER_DEFAULT_DAMAGE * damage_mult
        else:
            self.kill()
            return
            
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    def influence(self):
        self.game.player.sword_type = self.type
        self.game.player.damage = self.attack
        self.kill()
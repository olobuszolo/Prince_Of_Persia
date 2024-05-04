import pygame
from config import *
import math

class HealthPotion(pygame.sprite.Sprite):
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

class Potion2(HealthPotion):
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
        
class Potion3(HealthPotion):
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

class Potion4(HealthPotion):
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

class Potion5(HealthPotion):
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
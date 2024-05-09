import pygame
from config import *
import math
import random


class EnemyGreen(pygame.sprite.Sprite):
    def __init__(self, game, x, y, health, speed, attack, attack_ratio_max):
        self.game = game
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self,self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.x_change = 0
        self.y_change = 0
        
        self.facing = random.choice(['left','right'])
        self.speed = speed
        self.animation_loop = 1
        self.movement_loop = 0

        self.image = self.game.enemy_green_spritesheet.get_sprite(3,2,self.width,self.height)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.current_health = health
        self.attack = attack
        
        self.do_change = False
        self.attack_ratio = 0

        self.attack_ratio_max = attack_ratio_max
        
        self.left_animations = [self.game.enemy_green_spritesheet.get_sprite(3, 98, self.width, self.height),
                                self.game.enemy_green_spritesheet.get_sprite(35, 98, self.width, self.height),
                                self.game.enemy_green_spritesheet.get_sprite(68, 98, self.width, self.height)]

        self.right_animations = [self.game.enemy_green_spritesheet.get_sprite(3, 66, self.width, self.height),
                                self.game.enemy_green_spritesheet.get_sprite(35, 66, self.width, self.height),
                                 self.game.enemy_green_spritesheet.get_sprite(68, 66, self.width, self.height)]
        
    def update(self):
        self.movement()
        self.animate()
        self.collide_player()
        self.rect.x += self.x_change
        self.collide = self.collide_blocks()
        self.rect.y += self.y_change
        self.attack_player()
        self.x_change = 0
        self.y_change = 0
    
    def attack_player(self):
        if abs(self.rect.y - self.game.player.rect.y) <= 64:
            if abs(self.rect.x - self.game.player.rect.x) <= 64 and self.attack_ratio == 0:
                channel = pygame.mixer.find_channel()
                sound = pygame.mixer.Sound('resources\\sounds\\sword_fight_1.wav')
                sound.set_volume(0.15)
                channel.play(sound)
                if self.facing == 'right':
                    Attack(self.game,self.rect.x + TILESIZE,self.rect.y,'player',self.attack)
                if self.facing == 'left':
                    Attack(self.game,self.rect.x - TILESIZE,self.rect.y,'player',self.attack)
            if self.attack_ratio < self.attack_ratio_max:
                self.attack_ratio += 0.5
            if self.attack_ratio == self.attack_ratio_max:
                self.attack_ratio = 0
    
    def collide_player(self):
        hits = pygame.sprite.spritecollide(self, self.game.players, False)
        if hits:
            self.x_change = 0
    
    def collide_blocks(self):
        hits = pygame.sprite.spritecollide(self, self.game.collisions.sprites() + self.game.fakes.sprites(), False)
        if hits:
            if self.x_change > 0:
                self.rect.x = hits[0].rect.left - self.rect.width
                self.facing = 'l_col'
                self.x_change = 0
            if self.x_change < 0:
                self.rect.x = hits[0].rect.right
                self.facing = 'r_col'
                self.x_change = 0

    def movement(self):
        if self.facing == 'left':
            if abs(self.rect.y-self.game.player.rect.y)<=128 and abs(self.rect.x-self.game.player.rect.x)<=128:
                if self.rect.x - self.game.player.rect.x > 0:
                    self.x_change -= self.speed
                    self.movement_loop -= 1
                else:
                    self.facing = 'stay'
            else:
                self.x_change -= self.speed
                self.movement_loop -= 1
                
        if self.facing == 'right':
            if abs(self.rect.y-self.game.player.rect.y)<=128 and abs(self.rect.x-self.game.player.rect.x)<=128:
                if self.rect.x - self.game.player.rect.x < 0:
                    self.x_change += self.speed
                    self.movement_loop += 1
                else:
                    self.facing = 'stay'
            else:
                self.x_change += self.speed
                self.movement_loop += 1
                
        if self.facing == 'stay':
            if abs(self.rect.y-self.game.player.rect.y)<=128 and abs(self.rect.x-self.game.player.rect.x)<=128:
                if self.rect.x - self.game.player.rect.x >= 8:
                    self.facing = 'left'
                elif self.rect.x - self.game.player.rect.x <= -8:
                    self.facing = 'right'
                else:
                    self.facing = 'stay'
            else:
                self.facing = random.choice(['left','right'])
                
        if self.facing == 'l_col':
            if abs(self.rect.y-self.game.player.rect.y)>128 or self.rect.x - self.game.player.rect.x > 0 or self.rect.x - self.game.player.rect.x < -128:
                self.facing = 'left'
        if self.facing == 'r_col':
            if abs(self.rect.y-self.game.player.rect.y)>128 or self.rect.x - self.game.player.rect.x < 0 or self.rect.x - self.game.player.rect.x > 128:
                self.facing = 'right'
                
    def animate(self):
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.left_animations[0]
            else:
                self.image = self.left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.right_animations[0]
            else:
                self.image = self.right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.1
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        
    def get_damage(self,amount):
        self.current_health -= amount
        if self.current_health <=0:
            channel = pygame.mixer.find_channel()
            sound = pygame.mixer.Sound('resources\\sounds\\harm.wav')
            sound.set_volume(0.2)
            channel.play(sound)
            # for sprite in self.game.gate.sprites():
            #     sprite.kill()
            self.kill()
 


class EnemyBlue(EnemyGreen):
    def __init__(self, game, x, y, health, speed, attack, attack_ratio_max):
        super().__init__(game, x, y, health, speed, attack, attack_ratio_max)
        self.left_animations = [self.game.enemy_blue_spritesheet.get_sprite(3, 98, self.width, self.height),
                                self.game.enemy_blue_spritesheet.get_sprite(35, 98, self.width, self.height),
                                self.game.enemy_blue_spritesheet.get_sprite(68, 98, self.width, self.height)]

        self.right_animations = [self.game.enemy_blue_spritesheet.get_sprite(3, 66, self.width, self.height),
                                self.game.enemy_blue_spritesheet.get_sprite(35, 66, self.width, self.height),
                                self.game.enemy_blue_spritesheet.get_sprite(68, 66, self.width, self.height)]
        self.image = self.game.enemy_blue_spritesheet.get_sprite(3,2,self.width,self.height)
        self.image.set_colorkey(BLACK)

class EnemyRed(EnemyGreen):
    def __init__(self, game, x, y, health, speed, attack, attack_ratio_max):
        super().__init__(game, x, y, health, speed, attack, attack_ratio_max)
        self.left_animations = [self.game.enemy_red_spritesheet.get_sprite(3, 98, self.width, self.height),
                                self.game.enemy_red_spritesheet.get_sprite(35, 98, self.width, self.height),
                                self.game.enemy_red_spritesheet.get_sprite(68, 98, self.width, self.height)]

        self.right_animations = [self.game.enemy_red_spritesheet.get_sprite(3, 66, self.width, self.height),
                                self.game.enemy_red_spritesheet.get_sprite(35, 66, self.width, self.height),
                                self.game.enemy_red_spritesheet.get_sprite(68, 66, self.width, self.height)]
        self.image = self.game.enemy_red_spritesheet.get_sprite(3,2,self.width,self.height)
        self.image.set_colorkey(BLACK)

class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y, entity, attack):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.attack
        pygame.sprite.Sprite.__init__(self,self.groups)
        
        self.reciever = entity
        self.attack = attack
        
        self.x = x 
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE
        
        self.animation_loop = 0

        self.image = self.game.attack_spritesheet.get_sprite(0,0,self.width,self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.recieved = False
        
    def update(self):
        self.animate()
        self.collide()
        
    def collide(self):
        if self.reciever == 'enemy':
            hits = pygame.sprite.spritecollide(self,self.game.enemies,False)
            if hits and not self.recieved:
                self.recieved = True
                for enemy in hits:
                    enemy.get_damage(self.attack)
        if self.reciever == 'player':
            hits = pygame.sprite.spritecollide(self,self.game.players,False)
            if hits and not self.recieved:
                self.recieved = True
                for player in hits:
                    if not player.damage_resistance:
                        player.get_damage(self.attack)
            
    def animate(self):
        direction = self.game.player.facing
        right_animations = [self.game.attack_spritesheet.get_sprite(0, 64, self.width, self.height),
                        self.game.attack_spritesheet.get_sprite(32, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 64, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 64, self.width, self.height)]

        left_animations = [self.game.attack_spritesheet.get_sprite(0, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(32, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(64, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(96, 96, self.width, self.height),
                           self.game.attack_spritesheet.get_sprite(128, 96, self.width, self.height)]
        if direction == 'right':
            self.image = right_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                if self.reciever == 'enemy':
                    self.game.player.is_attacking = False
                self.kill()
        
        if direction == 'left':
            self.image = left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.5
            if self.animation_loop >= 5:
                if self.reciever == 'enemy':
                    self.game.player.is_attacking = False
                self.kill()
            
            
class Boss(EnemyGreen):
    def __init__(self, game, x, y, health, speed, attack, attack_ratio_max):
        super().__init__(game, x, y, health, speed, attack, attack_ratio_max)

        self.width = TILESIZE - 4
        self.height = 2 * TILESIZE

        self.rect = pygame.Rect(x * TILESIZE, (y + 1) * TILESIZE - self.height, self.width, self.height)

        self.left_animations = [
            pygame.transform.flip(self.game.boss_spritesheet.get_sprite(0, 7, self.width, self.height), True, False),
            pygame.transform.flip(self.game.boss_spritesheet.get_sprite(36, 7, self.width, self.height), True, False),
            pygame.transform.flip(self.game.boss_spritesheet.get_sprite(64, 7, self.width, self.height), True, False)
        ]

        self.right_animations = [
            self.game.boss_spritesheet.get_sprite(0, 7, self.width, self.height),
            self.game.boss_spritesheet.get_sprite(36, 7, self.width, self.height),
            self.game.boss_spritesheet.get_sprite(64, 7, self.width, self.height)
        ]

        self.image = self.game.boss_spritesheet.get_sprite(194, 7, self.width, self.height)
        self.image.set_colorkey(BLACK)

        self.change_time = 0
        self.activate = False
        self.magic = 0
        self.arrow_time = 0


    def random_version(self):
        result = self.magic
        result = random.randint(8, 39)
        return result

    def magic_changes(self):
        curr_time = pygame.time.get_ticks()
        if curr_time > self.change_time + 5000:
            self.fix_magic_sequence()
            self.magic = self.random_version() % 4 + 1
            self.change_time = curr_time
            if self.magic == 1: #slower 2 times
                self.game.player.speed *= 0.5
            elif self.magic == 2:
                self.game.player.attack *= 5    #change it when boss is ready
            elif self.magic == 3:
                self.rect.x = self.random_version() * TILESIZE
            elif self.magic == 4:
                self.game.player.current_health += 8
   
      
    def activation(self):
        if math.sqrt((self.rect.x - self.game.player.rect.x)**2 + (self.rect.y - self.game.player.rect.y)**2) * TILESIZE < 3 * TILESIZE:
            self.activate = True

    def fix_magic_sequence(self):
        if self.magic == 0 or self.magic == 3 or self.magic == 4:
            pass
        elif self.magic == 1:
            self.game.player.speed *= 2
        elif self.magic == 2:
            self.game.player.attack *= 2
    
    def get_damage(self,amount):
        self.current_health -= amount
        if self.current_health <=0:
            self.fix_magic_sequence()
            channel = pygame.mixer.find_channel()
            sound = pygame.mixer.Sound('resources\\sounds\\harm.wav')
            sound.set_volume(0.2)
            channel.play(sound)
            for sprite in self.game.gate.sprites():
                sprite.kill()
            self.kill()
 
    def cupids_arrow(self):
        curr_time = pygame.time.get_ticks()
        if abs(self.rect.x - self.game.player.rect.x) > 2*TILESIZE:
            if curr_time >= self.arrow_time + 2000:
                Arrow(self.game, self.rect.x, self.rect.y + 32, self.facing) 
                self.arrow_time = curr_time



    def update(self):
        self.activation()
        self.cupids_arrow()
        if self.activate:
            self.magic_changes()
        self.movement()
        self.animate()
        self.collide_player()
        self.rect.x += self.x_change
        self.collide = self.collide_blocks()
        self.rect.y += self.y_change
        self.attack_player()
        self.x_change = 0
        self.y_change = 0
    

class Arrow(pygame.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.arrows
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        self.width = TILESIZE
        self.height = TILESIZE

        if direction =='right':
            self.image = self.game.arrow_spritesheet.get_sprite(0,0,self.width+2,self.height)
            self.x += TILESIZE
        else:
            self.image=pygame.transform.flip(self.game.arrow_spritesheet.get_sprite(0,0,self.width+2,self.height), True, False)
            self.x -= TILESIZE

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.direction = direction

    def change_possition(self):
        if self.direction == 'right':
            self.rect.x += 7
        else:
            self.rect.x -= 7

    def check_collisions(self):
        colissions_player = pygame.sprite.spritecollide(self, self.game.players, False)
        if colissions_player:
            self.game.player.get_damage(16)
            self.kill()
        if self.rect.x >= 38*TILESIZE or self.rect.x <= 7 * TILESIZE:
            self.kill()

    def update(self):
        self.change_possition()
        self.check_collisions()
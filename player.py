import pygame
from config import *
import math
import random
from enemy import Attack
from items import *

'''
To move use left and right.
To jump us up. After reaching the door
use down to enter next level.
'''
"""
Player to refractor.
"""
class Player(pygame.sprite.Sprite):
    def  __init__(self,game,x,y,health,health_bar_size,sword_type):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.players
        pygame.sprite.Sprite.__init__(self,self.groups)
        
        self.x = x * TILESIZE
        self.y = y * TILESIZE # * 2
        self.width = TILESIZE
        self.height = TILESIZE # * 2
        
        self.x_change = 0
        self.y_change = 0
        
        self.is_jump = False
        self.jump_count = PLAYER_JUMP_HEIGHT
        self.speed = PLAYER_SPEED
        
        self.enter_next_level = False
        self.enter_next_semi_level = False
        self.is_on_trap = False
        self.is_on_lift = False
        self.last_spike_damage_time = 0
        self.trap_status = False
        self.hits_upper = False
        self.press_flag = False
        
        self.speed_potion = False
        self.speed_potion_time = 0 
        self.no_fall_damage = False
        self.no_fall_damage_time = 0
        self.damage_resistance = False
        self.damage_resistance_time = 0
        
        self.fall_count = -1
        
        self.facing = 'right'
        self.animation_loop = 1
        
        self.left_animations = self.game.character_spritesheet.get_sprites(3, 98, self.width, self.height, 1, 3)

        self.right_animations = self.game.character_spritesheet.get_sprites(3, 66, self.width, self.height, 1, 3)
        
        self.image = self.right_animations[0]
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.health_bar = HealthBar(self.game,self,health_bar_size)
        self.current_health = health
        self.maximum_health = PLAYER_MAX_HEALTH
        self.health_bar_length = 100
        self.halth_ratio = self.maximum_health / self.health_bar_length
        
        self.damage = PLAYER_DEFAULT_DAMAGE
        self.is_attacking = False

        self.speed = PLAYER_SPEED
        
        self.sword_type = sword_type
        if sword_type == 1:
            self.damage = PLAYER_DEFAULT_DAMAGE * 1.25
        elif sword_type == 2:
            self.damage = PLAYER_DEFAULT_DAMAGE * 1.5
        elif sword_type == 3:
            self.damage = PLAYER_DEFAULT_DAMAGE * 1.75
        elif sword_type == 4:
            self.damage = PLAYER_DEFAULT_DAMAGE * 2
        elif sword_type == 5:
            self.damage = PLAYER_DEFAULT_DAMAGE * 3
        
    def animate(self): 
        if self.facing == "left" and self.x_change != 0:
            self.image = self.left_animations[math.floor(self.animation_loop)]
            self.animation_loop += 0.1
            if self.animation_loop >= 3:
                self.animation_loop = 1
        
        if self.facing == "right" and self.x_change != 0:
            self.image = self.right_animations[math.floor(self.animation_loop)]
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
        self.collide_enemy()
        self.collide_items()
        
        self.potion_influence()
        
        self.x_change = 0
        self.y_change = 0

        if self.get_next_semi_level_pred():
            self.game.change_level = True

        if self.press_flag:
            self.get_damage(32)
            self.rect.x -= 3*TILESIZE
            self.rect.y += 0.5 * TILESIZE
            self.press_flag = False

        
    def movement(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_DOWN] and self.get_next_level_pred():
            self.game.change_level = True
            
        if keys[pygame.K_LEFT]:
            self.x_change -= self.speed
            self.facing = 'left'
            
        if keys[pygame.K_RIGHT]:
            self.x_change += self.speed
            self.facing = 'right'
        
        if keys[pygame.K_SPACE] and not self.is_attacking:
            self.is_attacking = True
            self.attack()
            
        if not self.is_jump:
            if keys[pygame.K_UP] and self.fall_count == -1:
                self.is_jump = True
            else:
                if self.fall_count >= -11:
                    self.y_change -= (self.fall_count * abs(self.fall_count)) * 0.4
                    self.fall_count -= 1
                else:
                    self.y_change = PLAYER_FALL_SPEED + 1
                
        else:
            if self.jump_count >= -11:
                self.y_change -= (self.jump_count * abs(self.jump_count)) * 0.4
                self.jump_count -= 1
            else:
                self.y_change=PLAYER_FALL_SPEED+1
                
    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self,self.game.enemies,False)
        if hits:
            if self.y_change > 32:
                for enemy in hits:
                    enemy.get_damage(8)
                    
    def collide_items(self):
        hits = pygame.sprite.spritecollide(self,self.game.potions.sprites() + self.game.swords.sprites(), False)
        for hit in hits:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                hit.influence()
    
    def potion_influence(self):
        if self.speed_potion:
            if self.speed_potion_time < 20:
                self.speed_potion_time += .1
            else:
                self.speed_potion = False
                self.speed_potion_time = 0
                self.speed = PLAYER_SPEED
        if self.no_fall_damage:
            if self.no_fall_damage_time < 40:
                self.no_fall_damage_time += .1
            else:
                self.no_fall_damage = False
                self.no_fall_damage_time = 0
                
        if self.damage_resistance:
            if self.damage_resistance_time < 40:
                self.damage_resistance_time += .1
            else:
                self.damage_resistance = False
                self.damage_resistance_time = 0
    
    def collide_blocks(self, direction):
        flag_lift = False
        flag_block = False
        flag_down = False

        if direction == "x":
            hits_press = pygame.sprite.spritecollide(self, self.game.movingblocks, False)
            hits = pygame.sprite.spritecollide(self, self.game.collisions.sprites() + self.game.protections.sprites(), False)
            if hits:
                # if self.x_change > 0 and not hits_press:
                #     self.rect.x = hits[0].rect.left - self.rect.width

                # if self.x_change < 0 and not hits_press:
                #     self.rect.x = hits[0].rect.right
                no_hits_press_above = all(obj.rect.y < self.rect.y for obj in hits_press)
        
                if self.x_change > 0 and no_hits_press_above:
                    self.rect.x = hits[0].rect.left - self.rect.width
                
                if self.x_change < 0 and no_hits_press_above:
                    self.rect.x = hits[0].rect.right

                    
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.collisions, False)
            hits_lift = pygame.sprite.spritecollide(self, self.game.lift, False)
            hits_down = pygame.sprite.spritecollide(self, self.game.down_press, False)
            hits_trap = pygame.sprite.spritecollide(self, self.game.traps, False)
            hits_upper = pygame.sprite.spritecollide(self, self.game.upper_press, False)
            hits_press = pygame.sprite.spritecollide(self, self.game.movingblocks, False)


            if hits:
                flag_block = True
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    self.jump_count = PLAYER_JUMP_HEIGHT
                    self.fall_count = -1
                    if self.y_change>PLAYER_FALL_SPEED and not self.no_fall_damage:
                        self.get_damage(32)
                    self.y_change=0
                    self.is_jump = False
                if self.y_change ==-40:
                    self.rect.y -= self.y_change
                elif self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
                    if self.is_jump:
                        self.jump_count = -1
  

            if hits_lift:
                flag_lift = True
                if self.y_change > 0:
                    self.rect.y = hits_lift[0].rect.top - self.rect.height 
                    self.jump_count = PLAYER_JUMP_HEIGHT
                    self.fall_count = -1
                    if self.y_change>PLAYER_FALL_SPEED and not self.no_fall_damage:
                        self.get_damage(32)
                    self.y_change=0
                    self.is_jump = False
                if self.y_change < 0:
                    self.rect.y = hits_lift[0].rect.bottom 
                    if self.is_jump:
                        self.jump_count = -1

            if hits_trap:
                 if self.y_change < 0:
                    self.rect.y = hits_trap[0].rect.bottom 
                    if self.is_jump:
                        self.jump_count = -1
            
            if hits_upper:
                self.hits_upper = True
                
            if hits_down:
                flag_down = True
                if self.y_change > 0:
                    self.rect.y = hits_down[0].rect.top - self.rect.height 
                    self.jump_count = PLAYER_JUMP_HEIGHT
                    self.fall_count = -1
                    if self.y_change>PLAYER_FALL_SPEED and not self.no_fall_damage:
                        self.get_damage(32)
                    self.y_change=0
                    self.is_jump = False
                if self.y_change < 0:
                    self.rect.y = hits_down[0].rect.bottom 
                    if self.is_jump:
                        self.jump_count = -1


            if flag_lift and flag_block:
                self.get_damage(32)
                self.is_on_lift = True

            if hits_upper and hits:
                self.get_damage(32)
                self.rect.y = self.rect.y + 64
                if self.x_change > 0:
                    self.rect.x = self.rect.x - 64
                else:
                    self.rect.x = self.rect.x + 64

            if flag_down and flag_lift:
                self.get_damage(32)
                if self.x_change > 0:
                    self.rect.x += 96
                else:
                    self.rect.x -= 96
                self.rect.y += 32         


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

    def get_next_level_pred(self):
        return self.enter_next_level

    def get_next_semi_level_pred(self):
        return self.enter_next_semi_level
    
    def get_trap_status_pred(self):
        return self.is_on_trap

    def get_damage(self,amount):
        if self.current_health > 0:
            play_sound('resources\\sounds\\guard-hit.wav',0.2)
            self.current_health -= amount
            self.health_bar.change_current_hp(-amount)
        if self.current_health <= 0:
            self.current_health = 0
            
    def get_health(self,amount):
        if self.current_health < self.maximum_health:
            self.current_health += amount
            self.health_bar.change_current_hp(amount)
        if self.current_health >= self.maximum_health:
            self.current_health = self.maximum_health
            
    def attack(self):  
        if self.facing == 'right':
            Attack(self.game, self.rect.x + TILESIZE,self.rect.y,'enemy',self.damage, self.facing)
            if self.sword_type == 2 and random.random()<0.5:
                Attack(self.game, self.rect.x + 2*TILESIZE,self.rect.y,'enemy',self.damage, self.facing)
                
        if self.facing == 'left':
            Attack(self.game, self.rect.x - TILESIZE,self.rect.y,'enemy',self.damage, self.facing)
            if self.sword_type == 2 and random.random()<0.5:
                Attack(self.game, self.rect.x - 2*TILESIZE,self.rect.y,'enemy',self.damage, self.facing)
                
        if self.sword_type == 1 and random.random()<0.15:
                self.get_damage(8)
                
        if self.sword_type == 3 and random.random()<0.1 and self.current_health/self.maximum_health < 0.2:
            self.get_health(8)
            
        if self.sword_type == 4 and random.random()<0.1 and self.current_health/self.maximum_health < 0.2:
            potion_type = random.choice(['1','2','3','4','5'])
            if potion_type == '1':
                HealthPotion(self.game,self.rect.x//32,self.rect.y//32)
            elif potion_type == '2':
                SpeedPotion(self.game,self.rect.x//32,self.rect.y//32)
            elif potion_type == '4':
                NoFallDamagePotion(self.game,self.rect.x//32,self.rect.y//32)
            elif potion_type == '5':
                DamageResistancePotion(self.game,self.rect.x//32,self.rect.y//32)
                
        if self.sword_type == 5 and random.random()<0.05:
            for enemy in self.game.enemies:
                enemy.kill()
                
"""
HealthBar refractored.
"""
class HealthBar(pygame.sprite.Sprite):
    def __init__(self, game, player, size):
        self.game = game
        self.player = player
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.x = size
        self.y = TILESIZE
        self.width = 10 * TILESIZE
        self.height = TILESIZE // 2
        self.border_width = 2
        
        self.image = pygame.Surface((self.width + 2 * self.border_width, self.height + 2 * self.border_width))
        self.rect = self.image.get_rect()
        self.rect.x = TILESIZE // 2
        self.rect.y = HEIGHT - TILESIZE // 1.5
        
        self.update_image()
        
    def update_image(self):
        self.image.fill(WHITE)
        left_surface = pygame.Surface((self.x, self.height))
        left_surface.fill(GREEN)
        right_surface = pygame.Surface((self.width - self.x, self.height))
        right_surface.fill(BLACK)
        self.image.blit(left_surface, (self.border_width, self.border_width))
        self.image.blit(right_surface, (self.x + self.border_width, self.border_width))
    
    def change_current_hp(self, amount):
        self.x = max(0, min(self.width, self.x + amount))
        self.update_image()
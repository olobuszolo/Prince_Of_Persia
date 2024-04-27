import pygame
from config import *
import math
from icecream import ic

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
    def  __init__(self,game,x,y,health,health_bar_size):
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
        
        self.enter_next_level = False
        self.enter_next_semi_level = False
        self.is_on_trap = False
        self.is_on_lift = False
        self.last_spike_damage_time = 0
        self.trap_status = False
        self.hits_upper = False
        
        self.fall_count = -1
        
        self.facing = 'right'
        self.animation_loop = 1
        
        self.image = self.game.character_spritesheet.get_sprite(0,0, self.width, self.height)
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.health_bar = HealthBar(self.game,self,health_bar_size)
        self.current_health = health
        self.maximum_health = PLAYER_MAX_HEALTH
        self.health_bar_length = 100
        self.halth_ratio = self.maximum_health / self.health_bar_length
        
        self.attack = PLAYER_DEFAULT_DAMAGE
        self.is_attacking = False
        
    def animate(self):

        left_animations = [self.game.character_spritesheet.get_sprite(3, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(35, 98, self.width, self.height),
                           self.game.character_spritesheet.get_sprite(68, 98, self.width, self.height)]

        right_animations = [self.game.character_spritesheet.get_sprite(3, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(35, 66, self.width, self.height),
                            self.game.character_spritesheet.get_sprite(68, 66, self.width, self.height)]
        
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
        self.collide_enemy()
        
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
                if self.fall_count >= -11:
                    self.y_change -= (self.fall_count * abs(self.fall_count)) * 0.4
                    self.fall_count -= 1
                else:
                    self.y_change=PLAYER_FALL_SPEED+1
                
        else:
            if self.jump_count >= -11:
                self.y_change -= (self.jump_count * abs(self.jump_count)) * 0.4
                self.jump_count -= 1
            else:
                self.y_change=PLAYER_FALL_SPEED+1
                
    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self,self.game.enemies,False)
        if hits:
            if self.y_change > 2:
                for enemy in hits:
                    enemy.get_damage(8)
    
    def collide_blocks(self, direction):
        flag_lift = False
        flag_block = False
        flag_down = False
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
            hits_falling = pygame.sprite.spritecollide(self, self.game.fakes, False)
            hits_lift = pygame.sprite.spritecollide(self, self.game.lift, False)
            hits_down = pygame.sprite.spritecollide(self, self.game.down_press, False)
            hits_trap = pygame.sprite.spritecollide(self, self.game.traps, False)
            hits_upper = pygame.sprite.spritecollide(self, self.game.upper_press, False)

            if hits:
                flag_block = True
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                    self.jump_count = PLAYER_JUMP_HEIGHT
                    self.fall_count = -1
                    if self.y_change>PLAYER_FALL_SPEED:
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
                    if self.y_change>PLAYER_FALL_SPEED:
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
                    if self.y_change>PLAYER_FALL_SPEED:
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
                self.rect.x = self.rect.x - 64            


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
            channel = pygame.mixer.find_channel()
            sound = pygame.mixer.Sound('resources\\sounds\\guard-hit.wav')
            sound.set_volume(0.2)
            channel.play(sound)
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
        

class HealthBar(pygame.sprite.Sprite):
    def  __init__(self,game,player,size):
        self.game = game
        self.player = player
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)
        
        self.x = size
        self.y = TILESIZE
        self.width = 10 * TILESIZE
        self.height = TILESIZE//2
        
        
        border_width = 2
        self.image = pygame.Surface((self.width+2*border_width,self.height + 2* border_width))
        self.image.fill(WHITE)
        left_surface = pygame.Surface((self.x,self.height))
        left_surface.fill(GREEN)
        right_surface = pygame.Surface((self.width-self.x,self.height))
        right_surface.fill(BLACK)
        self.image.blit(left_surface,(2,2))
        self.image.blit(right_surface,(self.x+2,2))
        self.rect = self.image.get_rect()
        
        self.rect.x = TILESIZE // 2
        self.rect.y = HEIGHT - TILESIZE//1.5
    def change_current_hp(self,amount):
        if self.x+amount > 0 and self.x+amount<self.width:
            self.x+=amount
            left_surface = pygame.Surface((self.x,self.height))
            left_surface.fill(GREEN)
            right_surface = pygame.Surface((self.width-self.x,self.height))
            left_border = pygame.Surface((2,self.height))
            left_border.fill(WHITE)
            right_surface.fill(BLACK)
            self.image.blit(left_surface,(2,2))
            self.image.blit(right_surface,(self.x+2,2))
        elif self.x+amount<=0:
            self.x=self.width
            surface = pygame.Surface((self.x,self.height))
            surface.fill(BLACK)
            self.image.blit(surface,(2,2))
            print("YOU DIED")
        else:
            self.x=self.width
            surface = pygame.Surface((self.x,self.height))
            surface.fill(GREEN)
            self.image.blit(surface,(2,2))
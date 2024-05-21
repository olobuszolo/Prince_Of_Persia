import pygame
from config import *
from map import *
from player import *
from enemy import *
from items import *
import sys
import os

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  # Initialize the mixer for playing sounds
        icon = pygame.image.load('resources/images/icon.png')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Prince Of Persia')
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Load spritesheets and images
        self.character_spritesheet = Spritesheet('resources/images/player_images/character.png')
        self.enemy_green_spritesheet = Spritesheet('resources/images/player_images/enemy_green.png')
        self.enemy_red_spritesheet = Spritesheet('resources/images/player_images/enemy_red.png')
        self.enemy_blue_spritesheet = Spritesheet('resources/images/player_images/enemy_blue.png')
        self.attack_spritesheet = Spritesheet('resources/images/player_images/attack.png')
        self.red_potion_spritesheet = Spritesheet('resources/images/map_images/red_potion.png')
        self.blue_potion_spritesheet = Spritesheet('resources/images/map_images/blue_potion.png')
        self.green_potion_spritesheet = Spritesheet('resources/images/map_images/green_potion.png')
        self.yellow_potion_spritesheet = Spritesheet('resources/images/map_images/yellow_potion.png')
        self.purple_potion_spritesheet = Spritesheet('resources/images/map_images/purple_potion.png')
        self.arrow_spritesheet = Spritesheet('resources/images/map_images/Arrows_pack2.png')
        self.boss_spritesheet = Spritesheet('resources/images/player_images/boss1.png')
        self.swords_spritesheet = Spritesheet('resources/images/map_images/swords.png')

        self.special_images = [
            'resources/images/menu/poziom1.png',
            'resources/images/menu/poziom2.png',
            'resources/images/menu/poziom3.png',
            'resources/images/menu/poziom4.png',
            'resources/images/menu/game_over_image.png'
        ]
        self.current_special_image_index = 0

        self.current_level_index = 0
        self.change_level = False
        self.show_special_image_flag = True
        self.special_image_start_time = pygame.time.get_ticks()
        self.game_over_flag = False

        self.start_time = 0.5 * 60 * 1000 
        self.time_left = self.start_time

        # Load and play background music
        pygame.mixer.music.load('resources/sounds/theme.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)

    def createTilemap(self, level):
        for i, row in enumerate(level):
            for j, column in enumerate(row):
                if column == "B":
                    Block(self, j, i)
                if column == "D":
                    Door(self, j, i)
                if column == "Y":
                    FallingLeft(self, j, i)
                if column == "R":
                    FallingRight(self, j, i)
                if column == "S":
                    Spikes(self, j, i)  
                if column == "H":
                    SemiDoors(self, j, i)
                if column == "P":
                    Protection(self, j, i)
                if column == "T":
                    NewTrap(self, j, i)
                if column == "L":
                    Lift(self, j, i)
                if column == "U":
                    UpperPress(self, j, i) 
                if column == "X":
                    DownPress(self, j, i)
                if column == "Z":
                    FallingLeftBottomUp(self, j, i)
                if column == "V":
                    Fakes(self,j,i)
                if column == "1":
                    HealthPotion(self,j,i)
                if column == "2":
                    SpeedPotion(self,j,i)
                if column == "3":
                    JumpPotion(self,j,i)
                if column == "4":
                    NoFallDamagePotion(self,j,i)
                if column == "5":
                    DamageResistancePotion(self,j,i)
                if column == "A":
                    Gate(self, j, i)

    def new(self, health_bar_size=10*TILESIZE, player_healt=PLAYER_MAX_HEALTH, sword_type=0):
        self.playing = True
        
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.doors = pygame.sprite.LayeredUpdates()
        self.fakes = pygame.sprite.LayeredUpdates()
        self.semidoors = pygame.sprite.LayeredUpdates()
        self.traps = pygame.sprite.LayeredUpdates()
        self.spikes = pygame.sprite.LayeredUpdates()
        self.protections = pygame.sprite.LayeredUpdates()
        self.collisions = pygame.sprite.LayeredUpdates()
        self.lift = pygame.sprite.LayeredUpdates()
        self.upper_press = pygame.sprite.LayeredUpdates()
        self.down_press = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attack = pygame.sprite.LayeredUpdates()
        self.players = pygame.sprite.LayeredUpdates()
        self.potions = pygame.sprite.LayeredUpdates()
        self.gate = pygame.sprite.LayeredUpdates()
        self.arrows = pygame.sprite.LayeredUpdates()
        self.swords = pygame.sprite.LayeredUpdates()

        self.createTilemap(levels[self.current_level_index])
        
        # Place the player
        start_x = start_position[self.current_level_index][0]
        start_y = start_position[self.current_level_index][1]
        self.player = Player(self, start_x, start_y, player_healt, health_bar_size, sword_type)
        
        # Place the boss
        for bosses in boss_positions[self.current_level_index]:
            self.boss = Boss(self, bosses[0], bosses[1], ENEMY_MAX_HEALTH * 8, ENEMY_RED_SPEED, ENEMY_GREEN_DAMAGE, ENEMY_GREEN_ATTACK_RATIO)

        # Place enemies
        for enemy in enemy_positions[self.current_level_index]:
            if enemy[2] == 'g': 
                EnemyGreen(self, enemy[0], enemy[1], ENEMY_MAX_HEALTH, ENEMY_GREEN_SPEED, ENEMY_GREEN_DAMAGE, ENEMY_GREEN_ATTACK_RATIO)
            elif enemy[2] == 'b':
                EnemyBlue(self, enemy[0], enemy[1], ENEMY_MAX_HEALTH, ENEMY_BLUE_SPEED, ENEMY_BLUE_DAMAGE, ENEMY_BLUE_ATTACK_RATIO)
            elif enemy[2] == 'r':
                EnemyRed(self, enemy[0], enemy[1], ENEMY_MAX_HEALTH, ENEMY_RED_SPEED, ENEMY_RED_DAMAGE, ENEMY_RED_ATTACK_RATIO)
        
        for sword in swords_positions[self.current_level_index]:
            Sword(self, sword[0], sword[1], sword[2])

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:  # Debug key to switch level
                if event.key == pygame.K_q:
                    self.change_level = True
                if event.key == pygame.K_u:  # Debug key to deal damage
                    self.player.get_damage(32)
                if event.key == pygame.K_o:  # Debug key to heal
                    self.player.get_health(32)
                if event.key == pygame.K_ESCAPE: 
                    sys.exit()

    def clock_update(self):
        self.time_left -= self.clock.get_time()
        if self.time_left <= 0:
            self.time_left = 0
  
    def update(self):
        if not self.show_special_image_flag and not self.game_over_flag:
            self.all_sprites.update()
            self.clock_update()

    def draw(self):  
        if self.show_special_image_flag or self.game_over_flag:
            special_image_path = self.special_images[self.current_special_image_index]
            special_image = pygame.image.load(special_image_path)
            scaled_image = pygame.transform.scale(special_image, (WIDTH, HEIGHT))
            self.screen.blit(scaled_image, (0, 0))
        else:
            image_as_background = pygame.image.load("resources/images/map_images/peakpx.jpg")
            scaled_background = pygame.transform.scale(image_as_background, (WIDTH, HEIGHT))
            self.screen.blit(scaled_background, (0, 0))
            self.all_sprites.draw(self.screen)

            minutes = self.time_left // 60000
            seconds = (self.time_left % 60000) // 1000
            time_text = f"{minutes:02}:{seconds:02}"
            font = pygame.font.Font(None, 74)
            text = font.render(time_text, True, (255, 255, 255))
            
            text_width, text_height = text.get_size()
            rect_width = text_width + 20  
            rect_height = text_height + 10
            rect_x = WIDTH // 2 - rect_width // 2
            rect_y = 10

            pygame.draw.rect(self.screen, (0, 0, 0), (rect_x, rect_y, rect_width, rect_height))

            self.screen.blit(text, (rect_x + 10, rect_y + 5))
        
        self.clock.tick(FPS)
        pygame.display.update()


    def main(self):
        while self.playing:
            self.events()
            if self.show_special_image_flag or self.game_over_flag:
                current_time = pygame.time.get_ticks()
                if current_time - self.special_image_start_time > 2000:
                    if self.show_special_image_flag:
                        self.show_special_image_flag = False
                        self.current_special_image_index = (self.current_special_image_index + 1) % len(self.special_images)
                        self.new(player_healt=self.player.current_health, health_bar_size=self.player.health_bar.x, sword_type=self.player.sword_type)
                    elif self.game_over_flag:
                        self.playing = False
                        pygame.mixer.music.stop() 

                else:
                    self.draw()
                    continue

            if (self.player.current_health == 0 and not self.game_over_flag) or self.time_left <= 0:
                self.game_over_flag = True
                self.special_image_start_time = pygame.time.get_ticks()
                self.current_special_image_index = 4

            if self.change_level:
                if self.current_level_index in {1, 3, 5, 7}:
                    self.show_special_image_flag = True
                    self.special_image_start_time = pygame.time.get_ticks()

                self.current_level_index = (self.current_level_index + 1) % len(levels)
                if not self.show_special_image_flag:
                    self.new(player_healt=self.player.current_health, health_bar_size=self.player.health_bar.x, sword_type=self.player.sword_type)
                self.change_level = False

            self.update()
            self.draw()

        self.running = False
        
    def game_over(self):
        pass
        #TODO

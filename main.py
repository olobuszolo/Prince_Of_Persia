import pygame
from config import *
from map import *
from player import *
from enemy import *
import sys
import os

class Game:
    def __init__(self):
        pygame.init()
        icon = pygame.image.load('resources/images/icon.png')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Prince Of Persia')
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # wczytanie animacji
        self.character_spritesheet = Spritesheet('resources/images/player_images/character.png')
        self.enemy_spritesheet = Spritesheet('resources/images/player_images/enemy.png')
        self.attack_spritesheet = Spritesheet('resources/images/player_images/attack.png')
        # self.go_background = pygame.image.load('resources/images/game_over.png')
        
        self.current_level_index = 0
        self.change_level = False
        
        
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
                # if column == "E":
                #     Enemy(self,j,i)


    def new(self,health_bar_size=10*TILESIZE, player_healt=PLAYER_MAX_HEALTH):
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

        self.createTilemap(levels[self.current_level_index])
        
        #postawienie gracza
        start_x = start_position[self.current_level_index][0]
        start_y = start_position[self.current_level_index][1]
        self.player = Player(self, start_x, start_y, player_healt, health_bar_size)
        
        #postawienie enemy
        for enemy in enemy_positions[self.current_level_index]:
            Enemy(self,enemy[0],enemy[1],enemy[2])
                
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            elif event.type == pygame.KEYDOWN:  #robocze przelaczanie mapy5
                if event.key == pygame.K_q:
                    self.change_level = True
                if (event.key == pygame.K_DOWN and self.player.get_next_level_pred()):
                    self.change_level = True
                if event.key == pygame.K_u:     # robocze dodawanie obrażeń
                    self.player.get_damage(32)
                if event.key == pygame.K_o:
                    self.player.get_health(32)  # szybkie zamykanie gry
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key == pygame.K_SPACE and not self.player.is_attacking:
                    self.player.is_attacking = True
                    channel = pygame.mixer.find_channel()
                    sound = pygame.mixer.Sound('resources\\sounds\\sword_fight_1.wav')
                    sound.set_volume(0.15)
                    channel.play(sound)
                    if self.player.facing == 'right':
                        Attack(self,self.player.rect.x + TILESIZE,self.player.rect.y,'enemy')
                    if self.player.facing == 'left':
                        Attack(self,self.player.rect.x - TILESIZE,self.player.rect.y,'enemy')



    def update(self):
        self.all_sprites.update()

    def draw(self):
        image_as_background = pygame.image.load("resources/images/map_images/peakpx.jpg")
        scaled_background = pygame.transform.scale(image_as_background, (WIDTH, HEIGHT))

        self.screen.blit(scaled_background, (0,0))
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
            if self.player.current_health==0:
                # self.playing = False
                pass
            if self.change_level:
                self.current_level_index = (self.current_level_index + 1) % len(levels)
                self.new(player_healt=self.player.current_health,health_bar_size=self.player.health_bar.x)
                self.change_level = False

        self.running = False
        
    def game_over(self):
        pass
        #TODO
        
os.chdir(os.path.dirname(os.path.realpath(__file__)))

g = Game()
g.new()
pygame.mixer.music.load('resources\\sounds\\theme.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.3)

# print(g.blocks.layers(),g.all_sprites.layers())
while g.running:
    g.main()
    g.game_over()

# pygame.mixer.music.stop()
pygame.quit()
sys.exit()
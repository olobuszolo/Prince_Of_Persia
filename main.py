import pygame
from config import *
from map import *
from player import *
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
        
        self.current_level_index = 0
        self.change_level = False
        
        
    def createTilemap(self, level):
        for i, row in enumerate(level):
            for j, column in enumerate(row):
                if column == "B":
                    Block(self, j, i)
                if column == "D":
                    Door(self, j, i)
                if column == "L":
                    FallingLeft(self, j, i)
                if column == "R":
                    FallingRight(self, j, i)
                if column == "T":
                    Trap(self, j, i)
                if column == "S":
                    Spikes(self, j, i)  
                if column == "H":
                    SemiDoors(self, j, i)
                if column == "P":
                    Protection(self, j, i)

    def new(self):
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

        self.createTilemap(levels[self.current_level_index])
        
        #postawienie gracza
        start_x = start_position[self.current_level_index][0]
        start_y = start_position[self.current_level_index][1]
        self.player = Player(self, start_x, start_y)

    def map_update(self):
        for sprite in self.all_sprites.sprites():
            if isinstance(sprite, Trap):
                sprite.kill()
                
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            elif event.type == pygame.KEYDOWN:  #robocze przelaczanie mapy
                if event.key == pygame.K_q:
                    self.change_level = True
                if (event.key == pygame.K_DOWN and self.player.get_next_level_pred()):
                    self.change_level = True



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
        
            if self.change_level:
                self.current_level_index = (self.current_level_index + 1) % len(levels)
                self.new()
                self.change_level = False

        self.running = False


os.chdir(os.path.dirname(os.path.realpath(__file__)))

g = Game()
g.new()
# pygame.mixer.music.load('resources\piesn.mp3')
# pygame.mixer.music.play(-1)

print(g.blocks.layers(),g.all_sprites.layers())
while g.running:
    g.main()

# pygame.mixer.music.stop()
pygame.quit()
sys.exit()
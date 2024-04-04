import pygame
from config import *
from map import *
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.running = True

    def createTilemap(self):
        for i, row in enumerate(basemap):
            for j, column in enumerate(row):
                if column == "B":
                    Block(self, j, i)
    
    def new(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()

        self.createTilemap()



    def draw(self):
        self.screen.fill(BLACK)
        self.clock.tick(FPS)
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()

    def draw(self):
        image_as_background = pygame.image.load("images/peakpx.jpg")
        scaled_background = pygame.transform.scale(image_as_background, (WIDTH, HEIGHT))

        self.screen.blit(scaled_background, (0,0))
        self.all_sprites.draw(self.screen)
        self.clock.tick()
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
        
        self.running = False

g = Game()
g.new()
while g.running:
    g.main()

pygame.quit()
import pygame
from config import *
from main import *
import sys
import os

class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        background_image = pygame.image.load("resources\images\menu\start_menu.png")
        self.background = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        self.game_rect = pygame.Rect(518, 51, 152, 67)
        self.instructions_rect = pygame.Rect(400, 120, 500, 74)
        self.results_rect = pygame.Rect(430, 220, 447, 72)
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)
            self.render()

    def handle_mouse_click(self, pos):
        if self.game_rect.collidepoint(pos):
            self.start_game()
        elif self.instructions_rect.collidepoint(pos):
            print("instructions") 
        elif self.results_rect.collidepoint(pos):
            print("results") 

    def start_game(self):
        self.running = False 
        game = Game()
        game.new()
        pygame.mixer.music.load('resources/sounds/theme.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)
        while game.running:
            game.main()
            game.game_over()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

if __name__ == '__main__':
    m = Menu()
    try:
        m.run()
    finally:
        pygame.quit()
        sys.exit()
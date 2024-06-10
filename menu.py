import pygame
from config import *
from game import *

"""
To look and refractor if needed.
"""
class Menu:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        
        background_image = pygame.image.load("resources/images/menu/start_menu.png")
        self.background = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
        
        self.instructions_image = pygame.image.load("resources/images/menu/instructions.png")
        self.instructions_background = pygame.transform.scale(self.instructions_image, (WIDTH, HEIGHT))
        
        self.game_rect = pygame.Rect(518, 51, 152, 67)
        self.instructions_rect = pygame.Rect(400, 120, 500, 74)
        self.results_rect = pygame.Rect(430, 220, 447, 72)
        self.back_rect = pygame.Rect(WIDTH - 150, HEIGHT - 100, 100, 50)

        self.running = True
        self.in_menu = True
        self.showing_instructions = False

        self.menu_music = 'resources/sounds/Artur-Andrus-Cyniczne-córy-Zurychu (1) (mp3cut.net).mp3'

    def play_menu_music(self):
        pass
        # if not pygame.mixer.music.get_busy():
        #     pygame.mixer.music.load(self.menu_music)
        #     pygame.mixer.music.play(-1)
        #     pygame.mixer.music.set_volume(0.3)

    def run(self):
        self.play_menu_music()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event.pos)
            self.render()

    def handle_mouse_click(self, pos):
        if self.in_menu:
            if self.game_rect.collidepoint(pos): 
                self.in_menu = False
                pygame.mixer.music.stop() 
                self.start_game()
            elif self.instructions_rect.collidepoint(pos):
                self.in_menu = False
                self.showing_instructions = True
            elif self.results_rect.collidepoint(pos):
                print("results")
        elif self.showing_instructions:
            if self.back_rect.collidepoint(pos):
                self.showing_instructions = False
                self.in_menu = True

    def start_game(self):
        self.running = False 
        game = Game()
        game.new()

        while game.running:
            game.main()
            game.game_over()
        
        self.running = True
        self.in_menu = True
        self.play_menu_music()

    def render(self):
        if self.showing_instructions:
            self.screen.blit(self.instructions_background, (0, 0))
            pygame.draw.rect(self.screen, (0, 0, 0), self.back_rect) 
            font = pygame.font.Font(None, 36)
            text = font.render("Back", True, (255, 255, 255))
            self.screen.blit(text, (self.back_rect.x + 10, self.back_rect.y + 10))
        else:
            self.screen.blit(self.background, (0, 0))
        
        pygame.display.flip()
        self.clock.tick(60)
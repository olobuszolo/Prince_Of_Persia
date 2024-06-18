import pygame
from config import *
from game import *

class Menu:
    def __init__(self):

        pygame.init()
        pygame.mixer.init()  

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        
        self.background = MENU_BACKGROUND
        self.instructions_background = INSTRUCTIONS_BACKGROUND
        self.results_image = RESULTS_BACKGROUND
        
        self.game_rect = pygame.Rect(518, 51, 152, 67)
        self.instructions_rect = pygame.Rect(400, 120, 500, 74)
        self.results_rect = pygame.Rect(430, 220, 447, 72)
        self.back_rect = pygame.Rect(WIDTH - 150, HEIGHT - 100, 100, 50)

        self.running = True
        self.in_menu = True
        self.showing_instructions = False
        self.showing_results = False
        
        play_music(MENU_MUSIC_PATH)

    def run(self):
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
                self.in_menu = False
                self.showing_results = True

        elif self.showing_instructions and self.back_rect.collidepoint(pos):
            self.showing_instructions = False
            self.in_menu = True

        elif self.showing_results and self.back_rect.collidepoint(pos):
            self.showing_results = False
            self.in_menu = True

    def start_game(self):
        self.running = False 
        game = Game()
        game.new()
        while game.running:
            game.main()
        
        self.running = True
        self.in_menu = True
        pygame.mixer.music.stop()
        play_music(MENU_MUSIC_PATH)
        
    def render(self):
        def draw_text(text, font_size, position, center=False):
            font = pygame.font.Font(FONT_PATH, font_size)
            rendered_text = font.render(text, True, BLACK)
            if center:
                position = (position[0] - rendered_text.get_width() // 2, position[1])
            self.screen.blit(rendered_text, position)

        if self.showing_instructions:
            self.screen.blit(self.instructions_background, (0, 0))
            pygame.draw.rect(self.screen, GREY, self.back_rect)
            draw_text("Back", 36, (self.back_rect.x + 10, self.back_rect.y + 10))

        elif self.showing_results:
            self.screen.blit(self.results_image, (0, 0))
            pygame.draw.rect(self.screen, GREY, pygame.Rect(60, 60, WIDTH - 120, HEIGHT - 164))
            pygame.draw.rect(self.screen, GREY, self.back_rect)
            
            draw_text("High scores", 50, (WIDTH // 2, 70), center=True)
            draw_text("Back", 36, (self.back_rect.x + 10, self.back_rect.y + 10))

            scores = load_scores()
            for i, score in enumerate(scores):
                draw_text(f"{i + 1}. {score['name']} - {score['time']}", 36, (WIDTH // 2, 130 + i * 50), center=True)

        else:
            self.screen.blit(self.background, (0, 0))
            
        pygame.display.flip()
        self.clock.tick(FPS)
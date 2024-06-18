import pygame
from config import *
from map import *
from player import *
from enemy import *
from items import *
import sys

class Game:
    """Class for the main game of the game.
    It creates map, set player and enemies, and handle the game loop.
    Draw the everything on the screen and update the game state."""
    def __init__(self):

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.character_spritesheet = CHARACTER_SPRITESHEET

        self.background = GAME_BACKGROUND

        self.special_images = SPECIAL_IMAGES
        self.current_special_image_index = 0
        self.game_over_image = GAME_OVER_IMAGE

        self.results_screen = RESULTS_BACKGROUND

        self.current_level_index = 0
        self.change_level = False
        self.show_special_image_flag = True
        self.special_image_start_time = 0
        self.game_over_flag = False
        self.new_record = False

        self.start_time = TIME
        self.time_left = self.start_time
        play_music(GAME_MUSIC_PATH)

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
                if column == "Z":
                    FallingLeftBottomUp(self, j, i)
                if column == "V":
                    Fakes(self,j,i)
                if column == "A":
                    Gate(self, j, i)
                if column == "C":
                    MovingBlock(self, j, i)

    def new(self, health_bar_size = 10 * TILESIZE, player_healt = PLAYER_MAX_HEALTH, sword_type = 0):
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
        self.movingblocks = pygame.sprite.LayeredUpdates()

        self.createTilemap(levels[self.current_level_index])
        
        start_x = start_position[self.current_level_index][0]
        start_y = start_position[self.current_level_index][1]
        self.player = Player(self, start_x, start_y, player_healt, health_bar_size, sword_type)
        
        for bosses in boss_positions[self.current_level_index]:
            self.boss = Boss(self, bosses[0], bosses[1])

        for enemy in enemy_positions[self.current_level_index]:
            if enemy[2] == 'g': 
                EnemyGreen(self, enemy[0], enemy[1])
            elif enemy[2] == 'b':
                EnemyBlue(self, enemy[0], enemy[1])
            elif enemy[2] == 'r':
                EnemyRed(self, enemy[0], enemy[1])

        for potion in potions_positions[self.current_level_index]:
            match potion[2]:
                case PotionType.HEALTH:
                    HealthPotion(self, potion[0], potion[1])
                case PotionType.SPEED:
                    SpeedPotion(self, potion[0], potion[1])
                case PotionType.NOFALL:
                    NoFallDamagePotion(self, potion[0], potion[1])
                case PotionType.NODAMAGE:
                    DamageResistancePotion(self, potion[0], potion[1])
        
        for sword in swords_positions[self.current_level_index]:
            Sword(self, sword[0], sword[1], sword[2])

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.change_level = True
                if event.key == pygame.K_u:
                    self.player.get_damage(32)
                if event.key == pygame.K_o:
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
        if self.game_over_flag:
            if self.special_image_start_time <= SHOWING_TIME:
                self.screen.blit(self.game_over_image, (0, 0))
                self.special_image_start_time += 1
            else:
                self.playing = False
                
        elif self.show_special_image_flag:
            if self.special_image_start_time <= SHOWING_TIME:
                image = self.special_images[self.current_special_image_index]
                self.screen.blit(image, (0, 0))
                self.special_image_start_time += 1
            else:
                self.show_special_image_flag = False
                self.special_image_start_time = 0
        
        elif self.new_record:
            font = pygame.font.Font(FONT_PATH, 36)
            title_font = pygame.font.Font(FONT_PATH, 80)

            input_box = pygame.Rect(WIDTH//2 - 100, HEIGHT // 2, WIDTH // 2, 50)

            color_inactive = pygame.Color('lightskyblue3')
            color_active = pygame.Color('dodgerblue2')
            color = color_inactive

            active = False
            text = ''
            done = False

            while not done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if input_box.collidepoint(event.pos):
                            active = not active
                        else:
                            active = False
                        color = color_active if active else color_inactive
                    if event.type == pygame.KEYDOWN:
                        if active:
                            if event.key == pygame.K_RETURN:
                                scores = load_scores()
                                minutes, seconds = count_time(self.time_left)
                                result = str(minutes) + ':' + str(seconds)
                                scores.append({"name": text, "time": result, "score": self.time_left})
                                scores.sort(key=lambda x: x['score'], reverse=True)
                                save_scores(scores[:10])
                                done = True
                            elif event.key == pygame.K_BACKSPACE:
                                text = text[:-1]
                            else:
                                text += event.unicode

                pygame.draw.rect(self.screen, GREY, pygame.Rect(60, 60, WIDTH-120, HEIGHT-164))
                self.screen.blit(self.results_screen, (0, 0))
        
                txt_surface = font.render(text, True, color)
                width = max(200, txt_surface.get_width() + 10)
                input_box.w = width

                tekst = title_font.render("You win!!!", True, BLACK)
                self.screen.blit(tekst, (WIDTH // 2 - tekst.get_width() // 2, HEIGHT // 4))
                
                give_name_txt = font.render("Give your name below:", True, BLACK)
                self.screen.blit(give_name_txt, (WIDTH // 2 - give_name_txt.get_width() // 2, input_box.y - 40))
                
                pygame.draw.rect(self.screen, color, input_box, 4)
                self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
                
                self.clock.tick(FPS)
                pygame.display.update()
            else:
                self.playing = False
            
        else:
            self.screen.blit(self.background, (0, 0))
            self.all_sprites.draw(self.screen)

            minutes, seconds = count_time(self.time_left)
            time_text = f"{minutes:02}:{seconds:02}"

            font = pygame.font.Font(FONT_PATH, 74)
            text = font.render(time_text, True, WHITE)
            
            text_width, text_height = text.get_size()
            rect_width = text_width + 20  
            rect_height = text_height + 10
            rect_x = WIDTH // 2 - rect_width // 2
            rect_y = 10

            pygame.draw.rect(self.screen, BLACK, (rect_x, rect_y, rect_width, rect_height))

            self.screen.blit(text, (rect_x + 10, rect_y + 5))
        
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        while self.playing:
            self.events()
            if self.player.current_health <= 0 or self.time_left <= 0:
                self.game_over_flag = True
                
            elif self.change_level and self.current_level_index != LAST_LEVEL_INDEX:
                self.current_level_index += 1

                if self.current_level_index in NEW_LEVEL_INDEX:
                    self.current_special_image_index += 1
                    self.show_special_image_flag = True

                if self.current_level_index == LAST_LEVEL_INDEX:
                    self.new_record = True

                else:
                    self.new(player_healt = self.player.current_health, health_bar_size = self.player.health_bar.x, sword_type = self.player.sword_type)
                    self.change_level = False

            self.update()
            self.draw()

        self.running = False
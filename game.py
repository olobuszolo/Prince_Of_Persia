import pygame
from config import *
from map import *
from player import *
from enemy import *
from items import *
import sys

"""
To look and refractor if needed.
"""
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
        self.special_image_start_time = 0
        self.game_over_flag = False
        self.new_record = False

        self.start_time = 10 * 60 * 1000 
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
                # if column == "U":
                #     UpperPress(self, j, i) 
                # if column == "X":
                #     DownPress(self, j, i)
                if column == "Z":
                    FallingLeftBottomUp(self, j, i)
                if column == "V":
                    Fakes(self,j,i)
                if column == "A":
                    Gate(self, j, i)
                if column == "C":
                    MovingBlock(self, j, i)

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
            self.boss = Boss(self, bosses[0], bosses[1])

        # Place enemies
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
                    HealthPotion(self,potion[0],potion[1])
                case PotionType.SPEED:
                    SpeedPotion(self,potion[0],potion[1])
                case PotionType.NOFALL:
                    NoFallDamagePotion(self,potion[0],potion[1])
                case PotionType.NODAMAGE:
                    NoFallDamagePotion(self,potion[0],potion[1])
        
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
        if self.game_over_flag:
            if self.special_image_start_time <= 30:
                special_image_path = self.special_images[4]
                special_image = pygame.image.load(special_image_path)
                scaled_image = pygame.transform.scale(special_image, (WIDTH, HEIGHT))
                self.screen.blit(scaled_image, (0, 0))
                self.special_image_start_time += 1
            else:
                self.playing = False
                
        elif self.show_special_image_flag:
            if self.special_image_start_time <= 30:
                special_image_path = self.special_images[self.current_special_image_index]
                special_image = pygame.image.load(special_image_path)
                scaled_image = pygame.transform.scale(special_image, (WIDTH, HEIGHT))
                self.screen.blit(scaled_image, (0, 0))
                self.special_image_start_time += 1
            else:
                self.show_special_image_flag = False
                self.special_image_start_time = 0
        
        elif self.new_record:
            font = pygame.font.Font(None, 36)
            title_font = pygame.font.Font(None, 80)
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
                                minutes = self.time_left // 60000
                                seconds = (self.time_left % 60000) // 1000
                                result = str(minutes) + ':' + str(seconds)
                                scores.append({"name": text, "time": result, "score": self.time_left})
                                scores.sort(key=lambda x: x['score'], reverse=True)
                                save_scores(scores[:10])
                                done = True
                            elif event.key == pygame.K_BACKSPACE:
                                text = text[:-1]
                            else:
                                text += event.unicode
                special_image_path = 'resources/images/menu/results_screen.png'
                special_image = pygame.image.load(special_image_path)
                scaled_image = pygame.transform.scale(special_image, (WIDTH, HEIGHT))
                pygame.draw.rect(self.screen, (192, 192, 192), pygame.Rect(60,60,WIDTH-120,HEIGHT-164))
                self.screen.blit(scaled_image, (0, 0))
        
                txt_surface = font.render(text, True, color)
                width = max(200, txt_surface.get_width() + 10)
                input_box.w = width

                tekst = title_font.render("You win!!!", True, BLACK)
                self.screen.blit(tekst, (WIDTH//2 - tekst.get_width()//2, HEIGHT//4))
                
                give_name_txt = font.render("Give your name below:", True, BLACK)
                self.screen.blit(give_name_txt, (WIDTH//2 - give_name_txt.get_width()//2, input_box.y - 40))
                
                pygame.draw.rect(self.screen, color, input_box, 4)
                self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

                pygame.display.flip()
                
                self.clock.tick(FPS)
                pygame.display.update()
            else:
                self.playing = False
            
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
            if self.player.current_health <= 0 or self.time_left <= 0:
                self.game_over_flag = True
            if self.change_level and self.current_level_index != 8:
                self.current_level_index += 1
                if self.current_level_index in [2, 4, 6]:
                    self.current_special_image_index += 1
                    self.show_special_image_flag = True
                if self.current_level_index == 8:
                    self.new_record = True
                else:
                    self.new(player_healt=self.player.current_health,health_bar_size=self.player.health_bar.x)
                    self.change_level = False
            self.update()
            self.draw()
        pygame.mixer.music.stop()
        self.running = False
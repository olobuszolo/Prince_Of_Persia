import pygame
from enum import Enum
import json

class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file)
        
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width,height])
        sprite.blit(self.sheet, (0,0), (x,y, width, height))
        sprite.set_colorkey(BLACK)
        return sprite
    
    def get_sprites(self, start_x, start_y, width, height, rows, columns):
        sprites = []
        for row in range(rows):
            for col in range(columns):
                sprite_x = start_x + col * width
                sprite_y = start_y + row * height
                sprites.append(self.get_sprite(sprite_x, sprite_y, width, height))
        return sprites

def play_sound(path,volume):
    channel = pygame.mixer.find_channel()
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    pygame.mixer.music.pause()
    channel.play(sound)
    pygame.mixer.music.unpause()

def play_music(path):
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)

def count_time(time):
    minutes = time // 60000
    seconds = (time % 60000) // 1000
    return minutes, seconds
    
def load_scores():
    try:
        with open(SCORES_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_scores(scores):
    with open(SCORES_FILE, 'w') as file:
        json.dump(scores, file, indent=4)

WIDTH = 1280
HEIGHT = 800

FPS = 30
TILESIZE = 32
TIME = 10 * 60 * 1000 
BLUE = (0, 0, 255)
RED = (255,0,0)
GREEN = (0,255,0)
WHITE = (255,255,255)
BLACK = (0, 0, 0)
GREY = (192, 192, 192)

FALL_SPEED = 2
CHANGE_INTERVAL = 400

BLOCK_LAYER = 1
PLAYER_LAYER = 4
ENEMY_LAYER = 3
ARROW_LAYER = 2

PLAYER_SPEED = 5
ENEMY_GREEN_SPEED = 3
ENEMY_BLUE_SPEED = 2
ENEMY_RED_SPEED = 4

PLAYER_DEFAULT_DAMAGE = 16
ENEMY_GREEN_DAMAGE = 16
ENEMY_BLUE_DAMAGE = 32
ENEMY_RED_DAMAGE = 8

ENEMY_GREEN_ATTACK_RATIO = 15
ENEMY_BLUE_ATTACK_RATIO = 30
ENEMY_RED_ATTACK_RATIO = 10

PLAYER_FALL_SPEED = 49
PLAYER_JUMP_HEIGHT = 10

PLAYER_MAX_HEALTH = 320
ENEMY_MAX_HEALTH = 80

TITLE = 'Prince Of Persia'
FONT_PATH = None

MENU_BACKGROUND = pygame.transform.scale(pygame.image.load("resources/images/menu/start_menu.png"), (WIDTH, HEIGHT))
INSTRUCTIONS_BACKGROUND = pygame.transform.scale(pygame.image.load("resources/images/menu/instructions.png"), (WIDTH, HEIGHT))
RESULTS_BACKGROUND = pygame.transform.scale(pygame.image.load("resources/images/menu/results_screen.png"), (WIDTH, HEIGHT))

ICON = pygame.image.load('resources/images/icon.png')

CHARACTER_SPRITESHEET = Spritesheet('resources/images/player_images/character.png')
ENEMY_GREEN_SPRITESHEET = Spritesheet('resources/images/player_images/enemy_green.png')
ENEMY_RED_SPRITESHEET = Spritesheet('resources/images/player_images/enemy_red.png')
ENEMY_BLUE_SPRITESHEET = Spritesheet('resources/images/player_images/enemy_blue.png')
ATTACK_SPRITESHEET = Spritesheet('resources/images/player_images/attack.png')
RED_POTION_SPRITESHEET = Spritesheet('resources/images/map_images/red_potion.png')
BLUE_POTION_SPRITESHEET = Spritesheet('resources/images/map_images/blue_potion.png')
GREEN_POTION_SPRITESHEET = Spritesheet('resources/images/map_images/green_potion.png')
YELLOW_POTION_SPRITESHEET = Spritesheet('resources/images/map_images/yellow_potion.png')
PURPLE_POTION_SPRITESHEET = Spritesheet('resources/images/map_images/purple_potion.png')
ARROW_SPRITESHEET = Spritesheet('resources/images/map_images/Arrows_pack2.png')
BOSS_SPRITESHEET = Spritesheet('resources/images/player_images/boss1.png')
SWORDS_SPRITESHEET = Spritesheet('resources/images/map_images/swords.png')

BRICK_IMAGE = pygame.transform.scale(pygame.image.load("resources/images/map_images/newbrick.png"), (TILESIZE, TILESIZE))
PRESS_IMAGE = pygame.transform.scale(pygame.image.load("resources/images/map_images/press.png"), (2 * TILESIZE, 4 * TILESIZE))
DOORS_IMAGE_CLOSE = pygame.transform.scale(pygame.image.load("resources/images/map_images/door_stairs.png"), (3 * TILESIZE, 4 * TILESIZE))
DOORS_IMAGE_OPEN = pygame.transform.scale(pygame.image.load("resources/images/map_images/door_stairs_open.png"), (3 * TILESIZE, 4 * TILESIZE))
SEMI_DOORS_IMAGE = pygame.transform.scale(pygame.image.load("resources/images/map_images/halfdoors.png"), (TILESIZE, 2 * TILESIZE))
SPIKES_IMAGE = pygame.transform.scale(pygame.image.load("resources/images/map_images/spikes.png"), (TILESIZE, 1.3 * TILESIZE))

EMPTY_IMAGE = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)

FALLING_IMAGES = list(map(pygame.transform.scale, list(map(pygame.image.load, ["resources/images/map_images/fake.png",
                                                                              "resources/images/map_images/fake.png",
                                                                              "resources/images/map_images/fake.png"])), [(TILESIZE, TILESIZE // 2)] * 3))

GAME_BACKGROUND = pygame.transform.scale(pygame.image.load("resources/images/map_images/peakpx.jpg"), (WIDTH, HEIGHT))
SPECIAL_IMAGES = list(map(pygame.transform.scale,list(map(pygame.image.load,['resources/images/menu/poziom1.png',
                                                    'resources/images/menu/poziom2.png',
                                                    'resources/images/menu/poziom3.png',
                                                    'resources/images/menu/poziom4.png'
                                                    ])), [(WIDTH, HEIGHT)] * 4))
GAME_OVER_IMAGE = pygame.transform.scale(pygame.image.load('resources/images/menu/game_over_image.png'), (WIDTH, HEIGHT))
SHOWING_TIME = 10


MENU_MUSIC_PATH = "resources/sounds/Artur-Andrus-Cyniczne-córy-Zurychu (1) (mp3cut.net).mp3"
GAME_MUSIC_PATH = "resources/sounds/theme.mp3"
POTION_SOUND_PATH = "resources\\sounds\\potion.wav"
GET_DAMAGE_SOUND_PATH = "resources\\sounds\\harm.wav"
PLAYER_GET_DAMAGE_SOUND_PATH = "resources\\sounds\\guard-hit.wav"
ATTACK_SOUND_PATH = "resources\\sounds\\sword_fight_1.wav"

SCORES_FILE = "high_scores.json"

NEW_LEVEL_INDEX = [2, 4, 6]
LAST_LEVEL_INDEX = 8


level1 = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B......................................B',
    'B......................................B',
    'B......................................H',
    'B......................................H',
    'B........................BBBBBBBBBBBBBBB',
    'B.......................BB.............B',
    'B......................BBB.............B',
    'B..................BBBBBBB.............B',
    'B.................B....................B',
    'B...............BB.....................B',
    'B......................................B',
    'B...........BB.........................B',
    'B.....V....V...........................B',
    'B......BBBB............................B',
    'B.............BB.......................B',
    'B.............BB...B...................B',
    'B.............BB.......................B',
    'B.............C........BB..............B',
    'B............................BBBB......B',
    'B......................................B',
    'B......................................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
]

level1_2 = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B......................................B',
    'P......................................B',
    'P......................................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBB.............B',
    'B................RRRRRRR..BBB..........B',
    'B......................................B',
    'B...............................BBB....B',
    'B......................................B',
    'B.....BBBBBBBBBBBBBBBBBBBBBBBB.........B',
    'B......................................B',
    'B......................................B',
    'B......................................B',
    'B..BB..................................B',
    'B......................................B',
    'B......B.V.............V...............B',
    'B.........BBBBBBBBBBBBB................B',
    'B......................................B',
    'B......................................B',
    'B......................................B',
    'B..........................BBB.........B',
    'B..................................D...B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
]

level2 = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B......................................B',
    'B......................................B',
    'B......................................H',
    'B......................................H',
    'B.........................BBB..BB..BBBBB',
    'B......................................B',
    'B..................BBBB................B',
    'B......................................B',
    'B......................................B',
    'B.....................BBBBBB...........B',
    'B...................BBBB...............B',
    'B......................................B',
    'B.......BBBBBBBBB......................B',
    'B......................................B',
    'B.................BB.BBB...............B',
    'B......................................B',
    'B...............BB.....................B',
    'B......B.......BB......................B',
    'B.......B....BBBB......................B',
    'B.......B...............BBB...B........B',
    'BBBBBBTTBBBBBBBBBBBBBBBBBBBB..BBBB.....B',
    'BBBBBB........................BBBBBBBBBB',
    'BBBBBB........................BBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
]

level2_2 = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B......................................B',
    'B......................................B',
    'P......................................B',
    'P......................................B',
    'BBBB...................................B',
    'B.........S............................B',
    'B.......BBBB...........................B',
    'B......................................B',
    'B......................................B',
    'B......................................B',
    'B.BBBB.................................B',
    'B......................................B',
    'B......................................B',
    'B.............S........................B',
    'B......B....BBBBB......................B',
    'B......................................B',
    'B..................BBB.................B',
    'B.............................D........B',
    'B.......................B...BBBBB......B',
    'B......................................B',
    'B......................................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
]

level3 = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B......................................B',
    'B......................................H',
    'B......................................H',
    'B............BBBB..BBBBBBBBBBBBBBBBBBBBB',
    'B...........BB.........................B',
    'B......................................B',
    'B...S..................................B',
    'BBBBBBBBBBBBB..........................B',
    'B.................BBBBB................B',
    'B...............B......................B',
    'B...............B......................B',
    'B...........BBBBB......................B',
    'B......................................B',
    'B......................................B',
    'BBB....................................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBB...B..........B',
    'B...................C..................B',
    'B...............................BBBBBBBB',
    'B......................................B',
    'B........................S.............B',
    'B................BBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
]

level3_1 = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B......................................B',
    'P......................................B',
    'P......................................B',
    'BBBBBBBBBBBBBBB...BBBBBBBBBBBBBBBBBBBBBB',
    'B...........B..........................B',
    'B...........B..........................B',
    'B...........B..........................B',
    'B...........B..........................B',
    'B...........B..........................B',
    'B...........B...L......................B',
    'B...........BBBBBBBBB..................B',
    'B...........B..........................B',
    'B...........BT.........................B',
    'B.............B........................B',
    'BBB....DV....VBB.......................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBB..........B',
    'B......................................B',
    'B...............................BBBBBBBB',
    'B......................................B',
    'B...............V...........V..........B',
    'B....DV..........BBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
]

level4 = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B..............ZZZZ....................B',
    'B......................................B',
    'B......................................H',
    'B......................................H',
    'B.....BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B......B...............................B',
    'BBB....B...............................B',
    'B......B...............................B',
    'B......B...............................B',
    'B....BBB...............................B',
    'B......B...............................B',
    'B......BBBBBBBTTTTTTTBBBBBBBBBBBB......B',
    'BBB......................B.............B',
    'B........................B.............B',
    'B........................B.............B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBB.............B',
    'B......................................B',
    'B......................................B',
    'B......................................B',
    'B.....................B................B',
    'B.......S..S.........BB...........L....B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
]

level4_1 = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B......................................B',
    'B......................................B',
    'P......................................B',
    'P......................................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBB..LL......BBBB',
    'B..................................B...B',
    'B......................................B',
    'B......................................B',
    'B...................S..................B',
    'BBBBBBBBBTTTBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B......................................B',
    'B......................................B',
    'BBBBBBBBBBBBBBBBB......................B',
    'B......................................B',
    'B...........BBBBBBBBBBBB...............B',
    'B......................................B',
    'BBBBBB.................................B',
    'B.....BBBBBBBB.........................B',
    'B.....A............BBB...........BBB...B',
    'B.....A................................B',
    'B..D..A................................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
]

class PotionType(Enum):
    HEALTH = 1
    SPEED = 2
    NOFALL = 3
    NODAMAGE = 4

levels = [level1, level1_2, level2, level2_2, level3, level3_1, level4, level4_1]
start_position = [(1,21), (1, 3), (1,20), (2,5), (1, 21), (1, 3), (2,21), (1,4)]
enemy_positions = [
                   [(9,13,'g')],
                   [(11,15,'b')],
                   [(8,23,'r')],
                   [],
                   [],
                   [(7,15,'b'),(13,21,'r'),(22,20,'g'),(30,20,'b')],
                   [],
                   []]
boss_positions = [[],[],[],[],[],[],[],[(12, 21)]]
potions_positions = [[(21,7,PotionType.HEALTH)],
                     [(34,6,PotionType.SPEED)],
                     [],
                     [(3,10,PotionType.NOFALL)],
                     [(1,7,PotionType.HEALTH),(38,17,PotionType.SPEED)],
                     [],
                     [(9,21,PotionType.HEALTH)],
                     [(20,18,PotionType.NODAMAGE),(38,4,PotionType.SPEED),(21,9,PotionType.HEALTH),(15,14,PotionType.HEALTH)]]
swords_positions = [[],[],[(22,23,1)],[],[(1,14,2)],[(1,14,3),(1,21,4)],[(10,21,5)],[]]


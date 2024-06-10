import pygame
from enum import Enum


WIDTH = 1280
HEIGHT = 800

FPS = 60
TILESIZE = 32
BLUE = (0, 0, 255)
RED = (255,0,0)
GREEN = (0,255,0)
WHITE = (255,255,255)
BLACK = (0, 0, 0)

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

new_levels_index = [1, 3, 5, 7]

basemap = [
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'B......................................B',
    'B......................................B',
    'B......................................B',
    'B......................................B',
    'B......................................B',
    'B......................................B',
    'B......................................B',
    'B...........................BBB........B',
    'B......................................B',
    'B......................................B',
    'B......................................B',
    'B......................................B',
    'B........D.............................B',
    'B......BBBBB...B.......................B',
    'B..................BB..................B',
    'B......................................B',
    'B..................BB..................B',
    'B..............BB......................B',
    'B......................................B',
    'B.......BBB............................B',
    'B......................................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB',
]

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
    'B......................................B',
    'B.......BBBB...........................B',
    'B......................................B',
    'B......................................B',
    'B......................................B',
    'B.BBBB.................................B',
    'B......................................B',
    'B......................................B',
    'B......................................B',
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
    'BBB....D......BB.......................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBBBBBB..........B',
    'B......................................B',
    'B...............................BBBBBBBB',
    'B......................................B',
    'B......................................B',
    'B....D...........BBBBBBBBBBBBBBBBBBBBBBB',
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
    'BBBBBBBBBBBBBBBBBBBBBBBBBB..LL.....BBBBB',
    'B......................................B',
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
start_position = [(1,21), (1, 3), (1,20), (2,5), (1, 21), (1, 3), (2,21), (2,5)]
enemy_positions = [
                   [(9,13,'g')],
                   [(11,15,'b')],
                   [(8,23,'r')],
                   [],
                   [],
                   [],
                   [],
                   []]
boss_positions = [[],[],[],[],[],[],[],[(12, 21)]]
potions_positions = [[(21,14,PotionType.HEALTH)],[],[],[(20,4,PotionType.NODAMAGE)],[],[(10,1,PotionType.HEALTH),(6,4,PotionType.SPEED)],[],[]]
swords_positions = [[],[],[(8,10,1),(9,10,2),(10,10,3),(11,10,4),(12,10,5)],[],[],[],[],[]]


class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()
        
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

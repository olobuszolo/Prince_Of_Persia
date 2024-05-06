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
PLAYER_LAYER = 3
ENEMY_LAYER = 2

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
    'B......................................B',
    'B..............BB......................B',
    'B......................................B',
    'B.......BBB............................B',
    'B...SS......12345...............1......B',
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
    'B...................BB...B...B...BB.BB.B',
    'B......................................B',
    'B......................................B',
    'B..................BB....B..BBB........B',
    'B.................B....................B',
    'B...............BB.....................B',
    'B......................................B',
    'B...........BB.........................B',
    'B.....V....V...........................B',
    'B......BBBB............................B',
    'B......................................B',
    'B.............BB...B...................B',
    'B......................................B',
    'B......................BB..............B',
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
    'B.........................BB.B.BB..BBBBB',
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
    'B...5...B...............BBB...B........B',
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
    'B......................................B',
    'BBBBBBBBBBBBB..........................B',
    'B.................BBBBB................B',
    'B...............B......................B',
    'B...............B......................B',
    'B...........BBBBB......................B',
    'B......................................B',
    'B......................................B',
    'BBB....................................B',
    'BBBBBBBBBBBBBBBBBBBBBBBBB...B..........B',
    'B......................................B',
    'B...............................BBBBBBBB',
    'B......................................B',
    'B......................................B',
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


levels = [basemap, level1, level1_2, level2, level2_2, level3, level3_1, level4, level4_1]
start_position = [(1,21), (1,21), (1, 4), (1,20), (2,3), (1, 21), (1, 3), (2,15), (2,16)]
enemy_positions = [[],
                   [(9,13,'g')],
                   [(11,15,'b')],
                   [(8,23,'r')],
                   [],
                   [],
                   [],
                   [],
                   []]
boss_positions = [[],[],[],[],[],[],[],[],[(12, 21 ,100)]]


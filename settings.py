import pygame as pg
vec = pg.math.Vector2

W = 1000
H = 600
FPS = 60
TITLE = "Egypt Game"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 100, 100)

TBLACK1 = (0, 0, 0, 150)
TBLACK2 = (0, 0, 0, 200)

BGcolor= BROWN

TILESIZE = 64
GRIDWIDTH = W / TILESIZE
GRIDHEIGHT = H / TILESIZE

WALL_LAYER = 3
PLAYER_LAYER = 4
CAR_LAYER = 2
ITEMS_LAYER = 1

WALL_IMG = 'tileGreen_39.png'

CAR_GREEN_LEFT = 'car_green_left.png'
CAR_GREEN_RIGHT = 'car_green_right.png'
CAR_RED_LEFT = 'car_red_left.png'
CAR_RED_RIGHT = 'car_red_right.png'
CAR_YELLOW_LEFT = 'car_yellow_left.png'
CAR_YELLOW_RIGHT = 'car_yellow_right.png'

CAR_SPEED = 2

PLAYER_HEALTH = 100
PLAYER_SPEED = 75
PLAYER_ROT_SPEED = 50
PLAYER_IMG = 'manBlue_gun.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)

BARREL_OFFSET = vec(30, 10)
KICKBACK = 27
GUN_SPREAD = 5

ITEM_IMAGES = {'knife': "knife.png", 'key': "key.png"}
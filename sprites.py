from typing import Any
import pygame as pg
from random import randint
from settings import *
from tilemap import collide_hit_rect
vec = pg.math.Vector2

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width // 2, height // 2))
        return image

class CarSpawner:
    def __init__(self, game, x, y, direction):
        self.game = game
        self.pos = (x, y)
        self.direction = direction

    def spawn_car(self):
        Car(self.game, self.pos[0], self.pos[1], self.direction)

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x

    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Car(pg.sprite.Sprite):
    def __init__(self, game, x, y, direction):
        self._layer = CAR_LAYER
        self.groups = game.all_sprites, game.car
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.direction = direction

        if self.direction == 'left':
            self.image = self.game.left_cars[randint(0, 1)]

        if self.direction == 'right':
            self.image = self.game.right_cars[randint(0, 1)]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hit_rect = self.rect
        self.hit_rect.center = self.rect.center

    def die(self):
        if self.direction == "left":
            if self.rect.x > 1920:
                self.kill()

        if self.direction == "left":
            if self.rect.x < 0:
                self.kill()

    def update(self):
        if self.direction == "left":
            self.rect.x += CAR_SPEED

        if self.direction == "right":
            self.rect.x += -CAR_SPEED
        
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        self.pickup_press = False
        self.inventory_has_space = True
        self.player_inv = []
        self.active_slot = 1

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        # click = pg.mou
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)
        if keys[pg.K_e]:
            self.pickup_press = True

    def update(self):
        self.pickup_press = False
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        
        self.inventory_has_space = (len(self.player_inv) != 5)

        if self.active_slot <= 0:
            self.active_slot += 5

            if self.active_slot < -4:
                self.active_slot = 1

        if self.active_slot > 5:
            self.active_slot = 1

        
# class Wall(pg.sprite.Sprite):
#     def __init__(self, game, x, y):
#         self.groups = game.all_sprites, game.walls
#         pg.sprite.Sprite.__init__(self, self.groups)
#         self.game = game
#         # self.image = game.wall_img
#         self.rect = self.image.get_rect()
#         self.x = x
#         self.y = y
#         self.rect.x = x * TILESIZE
#         self.rect.y = y * TILESIZE

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, type = "wall", img = False):
        self._layer = WALL_LAYER
        if img is False:
            self.groups = game.walls

        else:
            self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.type = type

        if img is True:
            if self.type == "Tunnel 1":
                self.image = self.game.spritesheet_scene_2.get_image(1224, 136, 64, 64)
                self.rect = self.image.get_rect()
            if self.type == "Tunnel 2":
                self.image = self.game.spritesheet_scene_2.get_image(1428, 136, 64, 64)
                self.rect = self.image.get_rect()
            if self.type == "Tunnel Floor 1":
                self.image = self.game.spritesheet_scene_2.get_image(1428, 204, 64, 64)
                self.rect = self.image.get_rect()
            if self.type == "Tunnel Floor 2":
                self.image = self.game.spritesheet_scene_2.get_image(1224, 204, 64, 64)
                self.rect = self.image.get_rect()

        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y 

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self._layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.rect.center = pos
        self.hit_rect = self.rect
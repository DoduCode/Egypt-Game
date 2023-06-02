import pygame as pg
import pygame_gui

import random
from os import path
import sys

from settings import *
from sprites import *
from tilemap import *

vec = pg.math.Vector2

def draw_inventory(surf, x, y, item_list, imgs, active_slot):
    BAR_LENGTH = 40
    BAR_HEIGHT = 40

    len_of_player_inv = len(item_list)

    outline_rect_1 = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect_1 = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)

    outline_rect_2 = pg.Rect(x + BAR_LENGTH + 10, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect_2 = pg.Rect(x + BAR_LENGTH + 10, y, BAR_LENGTH, BAR_HEIGHT)

    outline_rect_3 = pg.Rect(x + (BAR_LENGTH * 2) + 20, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect_3 = pg.Rect(x + (BAR_LENGTH * 2) + 20, y, BAR_LENGTH, BAR_HEIGHT)

    outline_rect_4 = pg.Rect(x + (BAR_LENGTH * 3) + 30, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect_4 = pg.Rect(x + (BAR_LENGTH * 3) + 30, y, BAR_LENGTH, BAR_HEIGHT)

    outline_rect_5 = pg.Rect(x + (BAR_LENGTH * 4) + 40, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect_5 = pg.Rect(x + (BAR_LENGTH * 4) + 40, y, BAR_LENGTH, BAR_HEIGHT)

    pg.draw.rect(surf, TBLACK1, fill_rect_1)
    pg.draw.rect(surf, WHITE, outline_rect_1, 2)

    if active_slot == 1:
        pg.draw.rect(surf, WHITE, outline_rect_1, 4)

    if len_of_player_inv >= 1:
        slot1 = imgs[item_list[0]].get_rect()
        slot1.center = fill_rect_1.center

        surf.blit(imgs[item_list[0]], slot1)

    pg.draw.rect(surf, TBLACK1, fill_rect_2)
    pg.draw.rect(surf, WHITE, outline_rect_2, 2)

    if active_slot == 2:
        pg.draw.rect(surf, WHITE, outline_rect_2, 4)

    if len_of_player_inv >= 2:
        slot1 = imgs[item_list[1]].get_rect()
        slot1.center = fill_rect_2.center

        surf.blit(imgs[item_list[1]], slot1)

    pg.draw.rect(surf, TBLACK1, fill_rect_3)
    pg.draw.rect(surf, WHITE, outline_rect_3, 2)

    if active_slot == 3:
        pg.draw.rect(surf, WHITE, outline_rect_3, 4)

    if len_of_player_inv >= 3:
        slot1 = imgs[item_list[2]].get_rect()
        slot1.center = fill_rect_3.center

        surf.blit(imgs[item_list[2]], slot1)

    pg.draw.rect(surf, TBLACK1, fill_rect_4)
    pg.draw.rect(surf, WHITE, outline_rect_4, 2)

    if active_slot == 4:
        pg.draw.rect(surf, WHITE, outline_rect_4, 4)

    if len_of_player_inv >= 4:
        slot1 = imgs[item_list[3]].get_rect()
        slot1.center = fill_rect_4.center

        surf.blit(imgs[item_list[3]], slot1)

    pg.draw.rect(surf, TBLACK1, fill_rect_5)
    pg.draw.rect(surf, WHITE, outline_rect_5, 2)

    if active_slot == 5:
        pg.draw.rect(surf, WHITE, outline_rect_5, 4)

    if len_of_player_inv >= 5:
        slot1 = imgs[item_list[4]].get_rect()
        slot1.center = fill_rect_5.center

        surf.blit(imgs[item_list[4]], slot1)

class Fader:
    def __init__(self):
        self.fading = None
        self.alpha = 0
        sr = pg.display.get_surface().get_rect()
        self.veil = pg.Surface(sr.size)
        self.veil.fill((0, 0, 0))

    def next(self, scene):
        if not self.fading:
            self.fading = 'OUT'
            self.alpha = 0
            scene() 

    def draw(self, screen):
        if self.fading:
            self.veil.set_alpha(self.alpha)
            screen.blit(self.veil, (0, 0))          

    def update(self):
        if self.fading == 'OUT':
            self.alpha += 8
            if self.alpha >= 255:
                self.fading = 'IN'
                # self.scene = next(self.scenes)
        else:
            self.alpha -= 8
            if self.alpha <= 0:
                self.fading = None

class Game:
    def __init__(self): 
        pg.init()
        self.screen = pg.display.set_mode((W, H))
        self.fader = Fader()

        self.show_phone = True
        self.load_level = False
        self.objectives = []
        self.scene = 1
        self.scene_holder = [self.load_scene_two, self.load_scene_three]
        self.player_dead = False

        self.font_name = pg.font.match_font('arial')
        self.font1 = pg.font.Font(self.font_name, 19)
        self.font2 = pg.font.Font(self.font_name, 20)

        self.alphasurflength1 = 240
        self.alphasurfrect2 = (980, 580)
        self.alphasurf1 = pg.Surface((self.alphasurflength1, 40), pg.SRCALPHA)
        self.alphasurf2 = pg.Surface((self.alphasurfrect2), pg.SRCALPHA)
        self.dead_screen = pg.Surface((W, H))

        self.fade_in_surf = pg.Surface((W, H), pg.SRCALPHA)

        self.manager = pygame_gui.UIManager((W, H))

        self.close_phone = pygame_gui.elements.UIButton(relative_rect=pg.Rect((self.screen.get_rect().centerx - (100 / 2), self.screen.get_rect().bottom - 150), (100, 50)),
                                    text = 'Okay',
                                    manager = self.manager)

        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')

        self.map = TiledMap(path.join(map_folder, 'OurHouse.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        self.map2 = TiledMap(path.join(map_folder, 'RoadCross.tmx'))
        self.map2_img = self.map2.make_map()
        self.map2_rect = self.map2_img.get_rect()

        self.map3 = TiledMap(path.join(map_folder, 'FriendHouse.tmx'))
        self.map3_img = self.map3.make_map()
        self.map3_rect = self.map3_img.get_rect()

        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()

        self.car_red_left = pg.image.load(path.join(img_folder, CAR_RED_LEFT)).convert_alpha()
        self.car_red_right = pg.image.load(path.join(img_folder, CAR_RED_RIGHT)).convert_alpha()

        self.car_yellow_left = pg.image.load(path.join(img_folder, CAR_YELLOW_LEFT)).convert_alpha()
        self.car_yellow_right = pg.image.load(path.join(img_folder, CAR_YELLOW_RIGHT)).convert_alpha()

        self.left_cars = [self.car_red_left, self.car_yellow_left]
        self.right_cars = [self.car_red_right, self.car_yellow_right]

        self.spritesheet_scene_2 = Spritesheet(path.join(img_folder, 'tilemap.png'))

        # self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        # self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        # self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        # self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()

    def load_scene_one(self):
        self.scene_obstacles = []
        self.remove = []

        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2, 
                             tile_object.y + tile_object.height / 2)
            
            if tile_object.name == "Player":
                self.player = Player(self, obj_center[0], obj_center[1])
            if tile_object.name == "Door":
                self.scene_obstacles.append(Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, "door"))
            if tile_object.name == "Next Level":
                self.scene_obstacles.append(Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, "nextlevel"))
            if tile_object.name == "Wall":
                self.scene_obstacles.append(Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height))
            if tile_object.name == "Furniture":
                self.scene_obstacles.append(Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height))
            if tile_object.name in ['knife', 'key']:
                Item(self, obj_center, tile_object.name)

    def load_scene_two(self):
        self.left_car_spawner_list = []
        self.right_car_spawner_list = []

        for tile_object in self.map2.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2, 
                             tile_object.y + tile_object.height / 2)
            
            if tile_object.name == "Player":
                self.player = Player(self, obj_center[0], obj_center[1])
            if tile_object.name == "Next Level":
                self.scene_obstacles.append(Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, "nextlevel"))
            if tile_object.name == "Wall":
                self.scene_obstacles.append(Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height))
            if tile_object.name == "Car Spawn Left":
                self.left_car_spawner_list.append(CarSpawner(self, obj_center[0], obj_center[1], "left"))
            if tile_object.name == "Car Spawn Right":
                self.right_car_spawner_list.append(CarSpawner(self, obj_center[0], obj_center[1], "right"))
            if tile_object.name == "Left Car":
                Car(self, obj_center[0], obj_center[1], "left")
            if tile_object.name == "Right Car":
                Car(self, obj_center[0], obj_center[1], "right")
            if tile_object.name == "Tunnel 1":
                self.scene_obstacles.append(Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, "Tunnel 1", True))
            if tile_object.name == "Tunnel 2":
                self.scene_obstacles.append(Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, "Tunnel 2", True))
            if tile_object.name == "Tunnel Floor 1":
                self.scene_obstacles.append(Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, "Tunnel Floor 1", True))
            if tile_object.name == "Tunnel Floor 2":
                self.scene_obstacles.append(Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, "Tunnel Floor 2", True))

            self.camera = Camera(self.map2.width, self.map2.height)
            self.remove.append(self.left_car_spawner_list)
            self.remove.append(self.right_car_spawner_list)


    def load_scene_three(self):
        for tile_object in self.map3.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2, 
                             tile_object.y + tile_object.height / 2)
            
            if tile_object.name == "Player":
                self.player = Player(self, obj_center[0], obj_center[1])
            # if tile_object.name == "Next Level":
            #     self.scene_obstacles.append(Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, "nextlevel"))
            if tile_object.name == "Wall":
                self.scene_obstacles.append(Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height))
            if tile_object.name == "Furniture":
                self.scene_obstacles.append(Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height))

            self.camera = Camera(self.map3.width, self.map3.height)

    def new(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.car = pg.sprite.Group()
        self.items = pg.sprite.Group()
        # self.mobs = pg.sprite.Group()
        # self.bullets = pg.sprite.Group()
        # for row, tiles in enumerate(self.map.data):
        #    for col, tile in enumerate(tiles):
        #        if tile == '1':
        #            Wall(self, col, row)
        #        if tile == 'P':
        #           self.player = Player(self, col, row)
        #        if tile == 'M':
        #             Mob(self, col, row)

        self.load_scene_one()
        self.camera = Camera(self.map.width, self.map.height)

        # self.player = Player(self, 608.00, 928.00)
        self.draw_debug = False

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 100
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type in ['knife', 'key'] and self.player.pickup_press and self.player.inventory_has_space:
                hit.kill()  
                self.player.player_inv.append(hit.type)

            if not self.player.inventory_has_space:
                pass

        hits = pg.sprite.spritecollide(self.player, self.walls, False)
        for hit in hits:
            if hit.type == "door" and "key" in self.player.player_inv and "knife" in self.player.player_inv:
                hit.kill()

            if hit.type == "nextlevel":
                del self.camera
                try:
                    del self.left_car_spawner_list
                    del self.right_car_spawner_list

                    for car in self.car:
                        car.kill()

                except:
                    pass
                # del self.remove

                self.walls.remove()
                self.player.kill()

                for obstacle in self.scene_obstacles:
                    obstacle.kill()
                    
                # for i in self.remove:
                #     for item in self.remove[i]:
                #         del self.remove[i][item]

                self.scene += 1
                self.fader.next(self.scene_holder[self.scene - 2])
                hit.kill()
                self.load_level = True

        hits = pg.sprite.spritecollide(self.player, self.car, False)
        for hit in hits:
            self.player.kill()
            self.player_dead = True

        if self.scene == 2:
            try:
                if self.right_spawned_1 == True:
                    self.right_number_1 = random.randrange(4, 7)

                if self.right_spawned_2 == True:
                    self.right_number_2 = random.randrange(4, 7)

                if self.right_spawned_3 == True:
                    self.right_number_3 = random.randrange(4, 7)

                self.right_spawned_1 = False
                self.right_spawned_2 = False
                self.right_spawned_3 = False

                if (self.last_right_spawn_1 - (pg.time.get_ticks() / 1000)) < -random.randrange(self.right_number_1, 7):
                    self.right_car_spawner_list[0].spawn_car()
                    self.last_right_spawn_1 = pg.time.get_ticks() / 1000
                    self.right_spawned_1 = True

                if (self.last_right_spawn_2 - (pg.time.get_ticks() / 1000)) < -random.randrange(self.right_number_2, 7):
                    self.right_car_spawner_list[1].spawn_car()
                    self.last_right_spawn_2 = pg.time.get_ticks() / 1000
                    self.right_spawned_2 = True

                if (self.last_right_spawn_3 - (pg.time.get_ticks() / 1000)) < -random.randrange(self.right_number_3, 7):
                    self.right_car_spawner_list[2].spawn_car()
                    self.last_right_spawn_3 = pg.time.get_ticks() / 1000
                    self.right_spawned_3 = True

                if self.left_spawned_1 == True:
                    self.left_number_1 = random.randrange(4, 7)

                if self.left_spawned_2 == True:
                    self.left_number_2 = random.randrange(4, 7)

                if self.left_spawned_3 == True:
                    self.left_number_3 = random.randrange(4, 7)

                self.left_spawned_1 = False
                self.left_spawned_2 = False
                self.left_spawned_3 = False

                if (self.last_left_spawn_1 - (pg.time.get_ticks() / 1000)) < -random.randrange(self.left_number_1, 7):
                    self.left_car_spawner_list[0].spawn_car()
                    self.last_left_spawn_1 = pg.time.get_ticks() / 1000
                    self.left_spawned_1 = True

                if (self.last_left_spawn_2 - (pg.time.get_ticks() / 1000)) < -random.randrange(self.left_number_2, 7):
                    self.left_car_spawner_list[1].spawn_car()
                    self.last_left_spawn_2 = pg.time.get_ticks() / 1000
                    self.left_spawned_2 = True

                if (self.last_left_spawn_3 - (pg.time.get_ticks() / 1000)) < -random.randrange(self.left_number_3, 7):
                    self.left_car_spawner_list[2].spawn_car()
                    self.last_left_spawn_3 = pg.time.get_ticks() / 1000
                    self.left_spawned_3 = True

            except:
                self.last_right_spawn_1 = pg.time.get_ticks() / 1000
                self.last_left_spawn_1 = pg.time.get_ticks() / 1000
                self.last_right_spawn_2 = pg.time.get_ticks() / 1000
                self.last_left_spawn_2 = pg.time.get_ticks() / 1000
                self.last_right_spawn_3 = pg.time.get_ticks() / 1000
                self.last_left_spawn_3 = pg.time.get_ticks() / 1000
                self.right_spawned_1 = True
                self.left_spawned_1 = True
                self.right_spawned_2 = True
                self.left_spawned_2 = True
                self.right_spawned_3 = True
                self.left_spawned_3 = True

        self.fader.update()

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        #self.screen.fill(BGcolor)
        if self.scene == 1:
            self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        
        if self.scene == 2:
            self.screen.blit(self.map2_img, self.camera.apply_rect(self.map2_rect))

        if self.scene == 3:
            self.screen.blit(self.map3_img, self.camera.apply_rect(self.map3_rect))
        #self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)

        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, WHITE, self.camera.apply_rect(wall.rect), 1)

        draw_inventory(self.alphasurf1, 0, 0, self.player.player_inv, self.item_images, self.player.active_slot)

        self.screen.blit(self.alphasurf1, 
                        (self.screen.get_rect().centerx - (self.alphasurflength1 / 2), 
                         self.screen.get_rect().bottom - 75))

        if self.show_phone:        
            self.show_phone_call()

            self.screen.blit(self.alphasurf2, (10, 10))

        if self.player_dead:
            self.show_dead()

        if self.load_level:
            self.fader.draw(self.screen)
            # self.screen.blit(self.fade_in_surf, (0, 0))
        
        #pg.draw.rect(self.screen, White, self.player.hit_rect, 2)

        self.manager.draw_ui(self.screen)
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug

                if event.key == pg.K_j:
                    self.show_phone = True

            if event.type == pg.MOUSEWHEEL:
                self.player.active_slot += event.y

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.close_phone:
                    self.show_phone = False
                    self.close_phone.hide()

            
            self.manager.process_events(event)

        self.manager.update(self.dt)

    def draw_text(self, surf, text, size, x, y):
        if size == 19:
            self.font = self.font1

        if size == 20:
            self.font = self.font2

        self.text_surface = self.font.render(text, True, WHITE)
        self.text_rect = self.text_surface.get_rect()
        self.text_rect.topleft = (x, y)
        surf.blit(self.text_surface, self.text_rect)

    def show_phone_call(self):
        if self.scene == 1:
            fill_rect_1 = pg.Rect(0, 0, 980, 580)
            pg.draw.rect(self.alphasurf2, TBLACK2, fill_rect_1)
            self.draw_text(self.alphasurf2, "Phone Call from Anish", 20, 10, 10)
            self.draw_text(self.alphasurf2, "  Anish: Hello Suraj! Come over to my house as I want to show you something I made during these few weeks", 19, 10, (35 * 1) + 10)
            self.draw_text(self.alphasurf2, "  Suraj: Can't you just send a pic to me", 19, 7, (35 * 2) + 10)
            self.draw_text(self.alphasurf2, "  Anish: It just can't be captured on a phone, just come over to my house and I'll show you", 19, 10, (35 * 3) + 10)
            self.draw_text(self.alphasurf2, "  Suraj: Fine! I'll be there over in an hour", 19 , 7, (35 * 4) + 10)
            self.draw_text(self.alphasurf2, "  Anish: Also bring your knife over", 19 , 10, (35 * 5) + 10)
            self.draw_text(self.alphasurf2, "  Suraj: Why? Are you gonna show me a dead body?", 19 , 7, (35 * 6) + 10)
            self.draw_text(self.alphasurf2, "  Anish: No... I just need it to cut some bread I made", 19 , 10, (35 * 7) + 10)
            self.draw_text(self.alphasurf2, "  Suraj: So you gonna call me all the way over just for me to cut some bread", 19 , 7, (35 * 8) + 10)
            self.draw_text(self.alphasurf2, "  Anish: Just come here with a knife, I ain't gonna show you bread", 19 , 10, (35 * 9) + 10)
            self.draw_text(self.alphasurf2, "  Suraj: Ok Fine! I'll come, it better be cool", 19 , 7, (35 * 10) + 10) 
            self.draw_text(self.alphasurf2, "  Anish: It's so cool you'll go back in time a bit", 19 , 10, (35 * 11) + 10) 
            self.draw_text(self.alphasurf2, "You can press 'J' to view the dialogue later", 19 , 10, (35 * 14) + 10) 

            self.close_phone.show()

    def show_start_screen(self):
        pass

    def show_dead(surf):
        pass

    def show_go_screen(self):
        pass

g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()

pg.quit
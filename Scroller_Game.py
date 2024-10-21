import pygame
import sys
import os
import random
import csv
from pygame import *
from tkinter import messagebox

class GameButton: 
        def __init__(self, x, y, image, allow):
            self.image = image
            self.rect = self.image.get_rect(topleft=(x, y))
            self.clicked = False
            self.allow = allow
            self.initial_click_processed = False

        def draw(self, surface):
            surface.blit(self.image, self.rect)
            action = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()[0]  

            if not self.initial_click_processed: 
                if mouse_click == 0:
                    self.initial_click_processed = True
                return action

            if self.rect.collidepoint(mouse_pos) and mouse_click == 1 and not self.clicked:
                action = True
                if not self.allow:
                    self.clicked = True

            if mouse_click == 0:
                self.clicked = False
            return action
        
    
if __name__ == "__main__":
    class World():

        def __init__(self):
            self.obstacle_list = []
            self.img_list=[]
            self.load_images()
        
        def process_data(self, data):
            for y, row in enumerate(data):
                self.level_length = len(data[0])
                for x, tile in enumerate(row):
                    if tile >= 0:
                        img = world.img_list[tile]
                        img_rect = img.get_rect()
                        img_rect.x = x * TILE_SIZE
                        img_rect.y = y * TILE_SIZE
                        tile_data = (img, img_rect,tile)
                        if tile <= 14:
                            self.obstacle_list.append(tile_data)
                        elif tile <= 16:
                            water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                            water_group.add(water)
                        elif tile <= 18:
                            decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                            decoration_group.add(decoration)
                        elif tile == 19:
                            player = soldier('player', x * TILE_SIZE, y * TILE_SIZE,) 
                            health_bar = HealthBar(10, 10, player.health, player.health)
                        elif tile == 20:
                            enemy = soldier('enemy', x * TILE_SIZE, y * TILE_SIZE, )
                            enemy_group.add(enemy)
                        elif tile == 21:
                            item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                            item_box_group.add(item_box)
                        elif tile == 22:
                            item_box = ItemBox('Grenade', x * TILE_SIZE, y * TILE_SIZE)
                            item_box_group.add(item_box)
                        elif tile == 23:
                            item_box = ItemBox('Ammo', x * TILE_SIZE, y * TILE_SIZE)
                            item_box_group.add(item_box)
                        elif tile == 24:
                            flag = Exit(self.img_list[24], x * TILE_SIZE, y * TILE_SIZE) 
                            flag_group.add(flag)
            try:
                return player, health_bar
            except UnboundLocalError:
                pygame.quit()
                pygame.mixer.quit()
                messagebox.showerror("Error!",f"Not a player instance found in level {level}. Please add a player instance through the level editor app.")
                exit()

        def draw(self):
            for tile in self.obstacle_list:
                tile[1][0] += screen_scroll
                screen.blit(tile[0], tile[1])

                
        def load_level(self,level):
            world_data = reset_level()
            with open(f'{pathh}/dependencies/levels/level{level}_data.csv', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        world_data[x][y] = int(tile)
            world = World()
            player, health_bar = world.process_data(world_data)
            bg_scroll=0
            return world_data,world,player,health_bar,bg_scroll
        def load_images(self):
            
            for x in range(TILE_TYPES):
                img = pygame.image.load(f'{pathh}/dependencies/pines/{x}.png').convert_alpha()
                img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
                self.img_list.append(img)
            return self.img_list
        

        
                

            
            


    class soldier(pygame.sprite.Sprite):
        def __init__(self, char_type, x, y,):
            pygame.sprite.Sprite.__init__(self)
            self.alive = True
            self.max_ammo = 25
            self.char_type = char_type
            self.speed = int((SCREEN_HEIGHT+SCREEN_HEIGHT)*0.005)
            self.ammo = self.max_ammo
            self.max_grenades = 7
            self.start_ammo = self.max_ammo
            self.shoot_cooldown = 0
            self.grenades = self.max_grenades
            self.health = 100
            self.max_health = self.health
            self.direction = 1
            self.jump = False
            self.in_air = True
            self.flip = False
            self.vel_y = 0
            self.animation_list = []
            self.frame_index = 0
            self.action = 0
            self.update_time = pygame.time.get_ticks()
            self.fade_out_speed = 3
            self.alpha = 255 #opacity

            self.move_counter = 0
            self.vision = pygame.Rect(0, 0, 150, 20)
            self.idling = False
            self.idling_counter = 0
            self.death_sound_played = False
            self.kills =0

            animation_types = ['Idle', 'Run','Jump','Death']
            temp_list = []
            self.death_animation_complete = False
            self.fade_out_complete = False

            for animation in animation_types:
                temp_list = []
                num_of_frames = len(os.listdir(f'{pathh}/dependencies/{self.char_type}/{animation}'))
                for i in range(num_of_frames):
                    img = pygame.image.load(f'{pathh}/dependencies/{self.char_type}/{animation}/{i}.png').convert_alpha()
                    img = pygame.transform.scale(img, (TILE_SIZE+TILE_SIZE/2,TILE_SIZE+TILE_SIZE//2))
                    
                    temp_list.append(img)
                self.animation_list.append(temp_list)

            self.animation_list.append(temp_list)
            self.image = self.animation_list[self.action][self.frame_index]
            self.rect = self.image.get_rect() 
            self.rect.width = int(self.rect.width * 0.6)  
            self.rect.center = (x, y)
            self.width = self.rect.width  
            self.height = self.image.get_height() 

        def update(self):
            self.update_animation()
            self.check_alive()
            if self.shoot_cooldown > 0:
                self.shoot_cooldown -= 1


            self.fade_out() #DEATH FADEOUT

       
            
        def fade_out(self):
            if not self.alive and self.death_animation_complete:
                self.alpha -= self.fade_out_speed  
                self.image.set_alpha(self.alpha)
                if self.alpha <= 0:
                    self.kill()
                    player.kills+=1
                    self.fade_out_complete = True
    
        def move(self, moving_left, moving_right):
            screen_scroll = 0
            dx = 0
            dy = 0
            
            if moving_left:
                dx = - self.speed
                self.flip = True
                self.direction = -1
            if moving_right:
                dx = + self.speed
                self.flip = False
                self.direction = 1

            if self.jump and not self.in_air:
                self.vel_y = -11
                self.jump = False
                self.in_air = True

            self.vel_y += GRAVITY
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y
            level_complete = False
            for tile in world.obstacle_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                    if self.char_type == 'enemy':
                        self.direction *= -1
                        self.move_counter = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height): 
                    if self.vel_y < 0:  
                        self.vel_y = 0
                        dy = tile[1].bottom - self.rect.top
                    elif self.vel_y >= 0:  
                        self.in_air = False
                        self.vel_y = 0
                        dy = tile[1].top - self.rect.bottom

            
            if pygame.sprite.spritecollide(self, water_group, False) and self.char_type == 'player':
                self.health = 0
            if pygame.sprite.spritecollide(self,flag_group,False):
                if self.kills == total_enemies:
                    level_complete = True
                else:
                    draw_text(f'KILL ALL ENEMIES TO UNLOCK FLAG',font,colors['RED'], 270, 100)
            
            if self.rect.bottom > SCREEN_HEIGHT:
                self.health = 0 
            if self.char_type == 'player':
                if self.rect.left + dx < 0 or self.rect.right +dx >SCREEN_WIDTH:
                    dx = 0

            self.rect.x += dx
            self.rect.y += dy
            if self.char_type == 'player':
                if (self.rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length*TILE_SIZE)- SCREEN_WIDTH)\
                    or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                    self.rect.x -= dx
                    screen_scroll = -dx
            return screen_scroll, level_complete

        def shoot(self):
            if self.shoot_cooldown == 0 and self.ammo > 0:
                sound_effects['shot'].play()
                self.shoot_cooldown = 20
                if self.char_type == 'player': 
                    self.ammo -= 1
                bullet = Bullet(self.rect.centerx + (self.rect.size[0]*0.75 * self.direction), self.rect.centery, self.direction,self.char_type)
                bullet_group.add(bullet)

        def ai(self):
            if self.alive and player.alive:
                if not self.idling and random.randint(1, 200) == 1:
                    self.idling = True
                    self.update_action(0)
                    self.idling_counter = 50
                if self.vision.colliderect(player.rect):
                    if player.rect.centerx < self.rect.centerx:
                        self.direction = -1
                        self.flip = True
                    else:
                        self.direction = 1
                        self.flip = False
                    self.update_action(0)
                    self.shoot()
                else:
                    if not self.idling:
                        if self.direction == 1:
                            ai_moving_right = True
                        else:
                            ai_moving_right = False

                        ai_moving_left = not ai_moving_right
                        self.move(ai_moving_left, ai_moving_right)
                        self.update_action(1)
                        self.move_counter += 1
                        self.vision.center = (
                            self.rect.centerx + 75 * self.direction, self.rect.centery)

                        if self.move_counter > TILE_SIZE:
                            self.direction *= -1
                            self.move_counter *= -1
                    else:
                        self.idling_counter -= 1
                        if self.idling_counter <= 0:
                            self.idling = False
            self.rect.x += screen_scroll

        def update_animation(self):
            ANIMATION_COOLDOWN = 100
            self.image = self.animation_list[self.action][self.frame_index]
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 3:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.frame_index = 0

        def update_action(self, new_action):
            if new_action != self.action:
                self.action = new_action
                self.frame_index = 0
                self.update_time = pygame.time.get_ticks()
       
        def check_alive(self):
            if self.health <= 0:
                self.health = 0
                self.speed = 0
                self.alive = False
                self.update_action(3)
                if self.frame_index >= len(self.animation_list[self.action]) - 1:
                    self.death_animation_complete = True 

        def draw(self):
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        

    class Decoration(pygame.sprite.Sprite):
        def __init__(self, img, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.midtop = (x+TILE_SIZE//2, y +
                                (TILE_SIZE-self.image.get_height()))
        def update(self):
            self.rect.x += screen_scroll
            
        

    class Water(pygame.sprite.Sprite):
        def __init__(self, img, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.midtop = (x+TILE_SIZE//2, y +
                                (TILE_SIZE-self.image.get_height()))
        def update(self):
            self.rect.x += screen_scroll

    class Exit(pygame.sprite.Sprite):
        def __init__(self, img, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.midtop = (x+TILE_SIZE//2, y +
                                (TILE_SIZE-self.image.get_height()))
        def update(self):
            self.rect.x += screen_scroll

    class ItemBox(pygame.sprite.Sprite):
        def __init__(self, item_type, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.item_type = item_type
            self.image = item_boxes[self.item_type]
            self.rect = self.image.get_rect()
            self.rect.midtop = (x + TILE_SIZE // 2, y +
                                (TILE_SIZE - self.image.get_height()))

        def update(self):
            self.rect.x += screen_scroll
            if pygame.sprite.collide_rect(self, player):
            
                if self.item_type == 'Ammo':
                    if player.ammo < player.max_ammo:
                        player.ammo = player.ammo + 25
                        if player.ammo > player.max_ammo:
                            player.ammo = player.max_ammo
                        self.kill()
                    else:
                        if pygame.sprite.collide_rect(self, player):
                            draw_text(f'ALREADY FULL AMMO', font, colors['GREEN'], 270, 100)
                elif self.item_type == 'Health':
                        if(player.health<player.max_health):
                            player.health = player.max_health
                            self.kill()
                        else:
                            draw_text(f'ALREADY FULL HEALTH', font, colors['GREEN'], 270, 100)
                elif self.item_type == 'Grenade':
                    if player.grenades < player.max_grenades:
                        player.grenades += player.grenades+player.max_grenades
                        if player.grenades > player.max_grenades:
                            player.grenades = player.max_grenades
                        self.kill()
                    else:
                        if pygame.sprite.collide_rect(self, player):
                            draw_text(f'ALREADY FULL GRENADES ',
                                    font, colors['GREEN'], 270, 100)

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y, direction,owner_type):
            pygame.sprite.Sprite.__init__(self)
            self.speed = int((SCREEN_HEIGHT+SCREEN_WIDTH)* 0.007)
            self.image = projectile_images['bullet']
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.direction = direction
            self.owner_type = owner_type

        def update(self):
            self.rect.x += (self.direction * self.speed) + screen_scroll

            if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
                self.kill()

            for tile in world.obstacle_list:
                if tile[1].colliderect(self.rect):
                    self.kill()

            if pygame.sprite.spritecollide(player, bullet_group, False):
                bullet = pygame.sprite.spritecollideany(player, bullet_group)  
                if bullet and bullet.owner_type == 'enemy' and player.alive:
                    bullet.kill()  
                    sound_effects['hurt'].play()
                    player.health -= 4  

            for enemy in enemy_group:
                if pygame.sprite.spritecollide(enemy, bullet_group, False):
                    bullet = pygame.sprite.spritecollideany(enemy, bullet_group)  
                    if bullet and bullet.owner_type == 'player' and enemy.alive:
                        bullet.kill()  
                        enemy.health -= 20 

    class Grenade(pygame.sprite.Sprite):
        def __init__(self, x, y, direction):
            pygame.sprite.Sprite.__init__(self)
            self.timer = 100
            self.vel_y = -11
            self.speed = int((SCREEN_WIDTH+SCREEN_HEIGHT)* 0.005)
            self.image = projectile_images['grenade']
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.width = self.image.get_width() 
            self.height = self.image.get_height()
            self.direction = direction
            self.damage = 45

        def update(self):
            self.vel_y += GRAVITY
            dx = self.direction * self.speed
            dy = self.vel_y
            for tile in world.obstacle_list:
                if tile[1].colliderect(self.rect.x+dx, self.rect.y, self.width, self.height):
                    self.direction *= -1
                    dx = self.direction * self.speed
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    self.speed = 0
                    if self.vel_y < 0:  # he is moving up
                        self.vel_y = 0
                        dy = tile[1].bottom - self.rect.top

                    elif self.vel_y >= 0:  # he is falling
                        self.in_air = False
                        self.vel_y = 0
                        dy = tile[1].top - self.rect.bottom

            self.rect.x += dx + screen_scroll
            self.rect.y += dy
            self.timer -= 1
            if self.timer <= 0 :
                self.kill()
                if(self.rect.y<SCREEN_HEIGHT):
                    sound_effects['grenade'].play()
                    explosion = Explosion(self.rect.x, self.rect.y, 0.5)
                    explosion_group.add(explosion)
                    if abs(self.rect.centerx - player.rect.centerx) < TILE_SIZE * 2 and \
                            abs(self.rect.centery - player.rect.centery) < TILE_SIZE * 2:
                        sound_effects['hurt'].play()
                        player.health -= self.damage
                    for enemy in enemy_group:
                        if abs(self.rect.centerx - enemy.rect.centerx) < TILE_SIZE * 2 and \
                                abs(self.rect.centery - enemy.rect.centery) < TILE_SIZE * 2:
                            enemy.health -= 50

    class HealthBar():
        def __init__(self, x, y, health, max_health):
            self.x = x
            self.y = y
            self.health = health
            self.max_health = max_health

        def draw(self, health):
            self.health = health
            ratio = self.health / self.max_health
            pygame.draw.rect(screen, (colors['BLACK']), (self.x-2, self.y-2, 154, 24))
            pygame.draw.rect(screen, (colors['RED']), (self.x, self.y, 150, 20))
            pygame.draw.rect(screen, (colors['GREEN']), (self.x, self.y, 150*ratio, 20))

    class Explosion(pygame.sprite.Sprite):
        def __init__(self, x, y, scale):
            pygame.sprite.Sprite.__init__(self)
            self.images = []
            for num in range(1, 7):
                img = pygame.image.load(
                    f'{pathh}/dependencies/explosion/exp{num}.png').convert_alpha()
                img = pygame.transform.scale(img, (120, 120))
                self.images.append(img)
            self.frame_index = 0
            self.image = self.images[self.frame_index]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.counter = 0

        def update(self):
            self.rect.x += screen_scroll
            EXPLOSION_SPEED = 4
            self.counter += 1
            if self.counter >= EXPLOSION_SPEED:
                self.counter = 0
                self.frame_index += 1
                if self.frame_index >= len(self.images):
                    self.kill() 
                else:
                    self.image = self.images[self.frame_index]
                    
    mixer.init()
    pygame.init()
    pygame.font.init()
    SCREEN_WIDTH = 800 
    SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    if getattr(sys, 'frozen', False):
        pathh = sys._MEIPASS # When it is run as .exe
    else:
        pathh = os.path.dirname(__file__) # When it is run in a Python enviroment
    font = pygame.font.SysFont('Futura', 30)
    SCROLL_THRESH = SCREEN_WIDTH * 0.3125
    start_game = False
    screen_scroll = 0
    bg_scroll = 0 
    ROWS = 16
    COLS = 150
    TILE_SIZE = int((SCREEN_HEIGHT+SCREEN_WIDTH) * 0.0278)
    TILE_TYPES = 25
    explosion_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    grenade_group = pygame.sprite.Group()
    
    def load_music(file_path, volume=0.1):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.set_volume(volume)

    def load_sound(file_path, volume=0.2):
        sound = pygame.mixer.Sound(file_path)
        sound.set_volume(volume)
        return sound

    def load_image(file_path, scale=None):
        image = pygame.image.load(file_path).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    
    colors = {
        'WHITE' : (255, 255, 255),
        'GREEN' : (0, 255, 0),
        'RED': (255, 0, 0),
        'BLACK' : (0, 0, 0),
        'BACKGROUND_COLOR': (29,51,51,255)
    }

    sound_effects = {
        'shot': load_sound(f'{pathh}/dependencies/sound_effects/shot.mp3', 0.2),
        'jump': load_sound(f'{pathh}/dependencies/sound_effects/jump.wav', 0.2),
        'won': load_sound(f'{pathh}/dependencies/sound_effects/won.mp3', 0.4),
        'grenade': load_sound(f'{pathh}/dependencies/sound_effects/explosion.wav', 0.2),
        'hurt': load_sound(f'{pathh}/dependencies/sound_effects/hurt.mp3', 0.2),
        'lost': load_sound(f'{pathh}/dependencies/sound_effects/lost.mp3', 0.5),
    }

    background_images = {
        'pine1': load_image(f'{pathh}/dependencies/background/pine1.png'),
        'pine2': load_image(f'{pathh}/dependencies/background/pine2.png'),
        'mountain': load_image(f'{pathh}/dependencies/background/mountain.png'),
        'sky': load_image(f'{pathh}/dependencies/background/sky_cloud.png'),
    }

    projectile_images = {
        'bullet': load_image(f'{pathh}/dependencies/projectiles/bullet.png',(int(SCREEN_WIDTH * 0.01), int(SCREEN_WIDTH * 0.01))),
        'grenade': load_image(f'{pathh}/dependencies/projectiles/grenade.png', (int(SCREEN_WIDTH * 0.0375), int(SCREEN_WIDTH * 0.0375))),  
    }

    item_boxes = {
        'Health': load_image(f'{pathh}/dependencies/pines/21.png', (TILE_SIZE, TILE_SIZE)),
        'Ammo': load_image(f'{pathh}/dependencies/pines/23.png', (TILE_SIZE, TILE_SIZE)),
        'Grenade': load_image(f'{pathh}/dependencies/pines/22.png', (TILE_SIZE, TILE_SIZE)),
    }

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    def draw_bg():
        screen.fill((colors['BACKGROUND_COLOR']))
        width = background_images['sky'].get_width()
        for x in range(5):
            screen.blit(background_images['sky'], ((x*width) - bg_scroll * 0.5, 0))
            screen.blit(background_images['mountain'], ((x*width)- bg_scroll*0.6, SCREEN_HEIGHT-background_images['mountain'].get_height()-300))
            screen.blit(background_images['pine1'], ((x*width)- bg_scroll*0.7, SCREEN_HEIGHT-background_images['pine1'].get_height()-150))
            screen.blit(background_images['pine2'], ((x*width)- bg_scroll*0.9, SCREEN_HEIGHT-background_images['pine2'].get_height()))

    def reset_level():
        enemy_group.empty()
        bullet_group.empty()
        grenade_group.empty()
        explosion_group.empty()
        item_box_group.empty()
        decoration_group.empty()
        water_group.empty()
        flag_group.empty()
        data = []

        for row in range(ROWS):
            r = [-1] * COLS
            data.append(r)
        return data

    button_images = {
        'start': load_image(f'{pathh}/dependencies/button_images/start_btn.png',(250,75)),
        'exit': load_image(f'{pathh}/dependencies/button_images/exit_btn.png', (250,75)),
        'restart': load_image(f'{pathh}/dependencies/button_images/restart_btn.png',(250,75)),
        'mute': load_image(f'{pathh}/dependencies/button_images/mute.png', scale=(70, 50)),
        'unmute': load_image(f'{pathh}/dependencies/button_images/unmute.png', scale=(70, 50)),
    }

    start_button =GameButton(SCREEN_HEIGHT//2-50 ,SCREEN_WIDTH//2-250,button_images['start'],False)
    exit_button = GameButton(SCREEN_HEIGHT//2 -50,SCREEN_WIDTH//2,button_images['exit'],False)
   
    restart_button = GameButton((SCREEN_WIDTH // 2) - (start_button.rect.width // 2), (SCREEN_HEIGHT // 2) - (start_button.rect.height // 2) - 50 ,button_images['restart'],False)
    mute_button= GameButton(SCREEN_WIDTH -200, 2,button_images['mute'],False)
    unmute_button =GameButton(SCREEN_WIDTH - 200, 2,button_images['unmute'],False)

    level = 1 
    grenade = False
    GRAVITY = 0.75
    shoot = False
    moving_left = False
    moving_right = False
    grenade_thrown = False
    MUSIC_VOLUME = 0.05
    load_music(f'{pathh}/dependencies/sound_effects/music.mp3', MUSIC_VOLUME)
    
    
    
    

    flag_group = pygame.sprite.Group()
    flag_img = pygame.image.load(f'{pathh}/dependencies/pines/22.png')
    flag_img= pygame.transform.scale(flag_img, (TILE_SIZE, TILE_SIZE))

    decoration_group = pygame.sprite.Group()
    water_group = pygame.sprite.Group()
    item_box_group = pygame.sprite.Group()

    death_channel = pygame.mixer.Channel(2)
    muted = False
    run = True
    clock = pygame.time.Clock()
    FPS_CAP = 60
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    is_fullscreen = False
    while run:
        FPS = str(int(clock.get_fps())) 
        if not start_game:
            pygame.display.set_caption('PANOS KENTROS UNIWA')
            screen.fill(colors['BACKGROUND_COLOR'])
            if start_button.draw(screen):
                world = World()
                world_data,world,player,health_bar,bg_scroll = world.load_level(level)
                total_enemies = len(enemy_group)
                start_game = True
                pygame.mixer.music.play()

            if exit_button.draw(screen):
                run = False
        else:

            draw_bg()

            world.draw()

            health_bar.draw(player.health)
            draw_text(f'AMMO: ', font, colors['WHITE'], 10, 35)
            for x in range(player.ammo):
                screen.blit(projectile_images['bullet'], (90 + (x*10), 40))
            draw_text(f'GRENADES: ', font, colors['WHITE'], 10, 70)
            for x in range(player.grenades):
                screen.blit(projectile_images['grenade'
                                              ], (135 + (x*15), 60))

            draw_text(f'FPS: {FPS}', font, colors['WHITE'], SCREEN_WIDTH-100, 20)
            draw_text(f'KILLS: {player.kills}/{total_enemies} ', font, colors['WHITE'], 10, 100)
            item_box_group.update()
            item_box_group.draw(screen)

            decoration_group.update()
            decoration_group.draw(screen)

            water_group.update()
            water_group.draw(screen)

            flag_group.update()
            flag_group.draw(screen)

            grenade_group.update()
            grenade_group.draw(screen)
            for enemy in enemy_group:
                enemy.ai()
                enemy.update()
                enemy.draw()

            

            bullet_group.update()
            bullet_group.draw(screen)
            player.draw()
            explosion_group.update()
            explosion_group.draw(screen)

            
            pygame.display.set_caption('LEVEL: '+str(level))
            if muted == False:
                if mute_button.draw(screen):
                    pygame.mixer.music.set_volume(0)
                    muted = not muted
            else:
                if unmute_button.draw(screen):
                    pygame.mixer.music.set_volume(0.1)
                    muted = not muted
                
            if player.alive:
                if shoot:
                    player.shoot()
                elif grenade and not grenade_thrown and player.grenades > 0:
                    grenade = Grenade(player.rect.centerx + (player.rect.size[0]*0.6*player.direction), player.rect.top, player.direction)
                    grenade_group.add(grenade)
                    grenade_thrown = True
                    player.grenades -= 1

                if player.in_air:
                    player.update_action(2)
                elif moving_left or moving_right:
                    player.update_action(1)
                else:
                    player.update_action(0)
                screen_scroll,level_complete = player.move(moving_left, moving_right)
                bg_scroll -= screen_scroll
                player.update()
                if level_complete : 
                    level += 1
                    try:
                        world_data,world,player,health_bar,bg_scroll = world.load_level(level)
                        total_enemies = len(enemy_group)
                    except FileNotFoundError:
                            pygame.mixer.music.stop()
                            sound_effects['won'].play()
                            messagebox.showinfo('Game over!', "You have won! Please create more levels to continue the game...")
                            run = False
            else:
                player.update()
                if not player.death_sound_played:
                    pygame.mixer.music.stop()
                    death_channel.play(sound_effects['lost']) 
                    player.death_sound_played = True
                if player.death_animation_complete and player.fade_out_complete:

                    screen_scroll = 0
                    screen.fill(colors['BACKGROUND_COLOR'])
                    
                    if exit_button.draw(screen):
                        run = False
                    
                    if restart_button.draw(screen):
                        pygame.mixer.music.play()
                        world_data,world,player,health_bar,bg_scroll = world.load_level(level)
                        
                        
        keys = pygame.key.get_pressed()  
        if keys[pygame.K_w] and player.alive and not player.in_air:
                player.jump = True
                sound_effects['jump'].play()
                
                        
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                run = False
                
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and player.alive:
                    moving_left = True
                if event.key == pygame.K_d and player.alive:
                    moving_right = True
                if event.key == pygame.K_SPACE:
                    shoot = True
                if event.key == pygame.K_q:
                    grenade = True

            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_d:
                    moving_right = False
                if event.key == pygame.K_SPACE:
                    shoot = False
                if event.key == pygame.K_q:
                    grenade = False
                    grenade_thrown = False

           
                


                

        
            

        pygame.display.update()
        clock.tick(FPS_CAP)
pygame.mixer.quit()
pygame.quit()

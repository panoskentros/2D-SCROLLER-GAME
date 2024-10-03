import pygame
import csv
import sys
import os
from SCROLLER_GAME import GameButton
pygame.init()


pygame.display.set_caption('Level Editor')
if getattr(sys, 'frozen', False): # Fom when it is executed as .exe
        pathh = sys._MEIPASS
else: 
	pathh = os.path.dirname(__file__) # For when it is executed in a Python enviroment
clock = pygame.time.Clock()
FPS_CAP = 60
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8) 
LOWER_MARGIN = 130
SIDE_MARGIN = 300
font = pygame.font.SysFont('Futura', 30)
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
ROWS = 16
COLS = 150
TILE_SIZE = int((SCREEN_HEIGHT+SCREEN_WIDTH) * 0.0278)
TILE_TYPES = 25
level = 1
current_tile = 0
scroll = [0]
scroll_speed = 1

def load_image(file_path, scale=None):
        image = pygame.image.load(file_path).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
background_images = {
        'pine1': load_image(f'{pathh}/dependencies/background/pine1.png'),
        'pine2': load_image(f'{pathh}/dependencies/background/pine2.png'),
        'mountain': load_image(f'{pathh}/dependencies/background/mountain.png'),
        'sky': load_image(f'{pathh}/dependencies/background/sky_cloud.png'),
    }
img_list = []
for x in range(TILE_TYPES):
	img = pygame.image.load(f'{pathh}/dependencies/pines/{x}.png').convert_alpha()
	img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
	img_list.append(img)


button_images = {
	'save': load_image(f'{pathh}/dependencies/button_images/save_btn.png'),
	'load': load_image(f'{pathh}/dependencies/button_images/load_btn.png'),
	'left_arrow': load_image(f'{pathh}/dependencies/button_images/left_arrow.png',(60, 60 )),
	'right_arrow': load_image(f'{pathh}/dependencies/button_images/right_arrow.png',(60, 60))
}
save_button = GameButton(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, button_images['save'],False)
load_button = GameButton(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, button_images['load'],False)
left_arrow_button = GameButton(SCREEN_WIDTH // 2 +10  , SCREEN_HEIGHT + LOWER_MARGIN - 120, button_images['left_arrow'],True)
right_arrow_button = GameButton(SCREEN_WIDTH // 2 + 210, SCREEN_HEIGHT + LOWER_MARGIN - 120, button_images['right_arrow'],True)

button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
	tile_button = GameButton(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i],False)
	button_list.append(tile_button)
	button_col += 1
	if button_col == 3:
		button_row += 1
		button_col = 0

colors = {
        'WHITE' : (255, 255, 255),
        'GREEN' : (60, 164, 0),
        'RED': (255, 0, 0),
        'BLACK' : (0, 0, 0),
        'BACKGROUND_COLOR': (29,51,51,255)
    }


def reset_level():
        return [[-1] * COLS for _ in range(ROWS)]

world_data = reset_level()

def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))

def draw_bg():
	screen.fill(colors['GREEN'])
	width = background_images['sky'].get_width()
	for x in range(4):
		screen.blit(background_images['sky'], ((x * width) - scroll[0] * 0.5, 0))
		screen.blit(background_images['mountain'], ((x * width) - scroll[0] * 0.6, SCREEN_HEIGHT - background_images['mountain'].get_height() - 300))
		screen.blit(background_images['pine1'], ((x * width) - scroll[0] * 0.7, SCREEN_HEIGHT - background_images['pine1'].get_height() - 150))
		screen.blit(background_images['pine2'], ((x * width) - scroll[0] * 0.8, SCREEN_HEIGHT - background_images['pine2'].get_height()))

def draw_grid():
	for c in range(COLS + 1):
		pygame.draw.line(screen, colors['WHITE'], (c * TILE_SIZE - scroll[0], 0), (c * TILE_SIZE - scroll[0], SCREEN_HEIGHT))
	for c in range(ROWS + 1):
		pygame.draw.line(screen, colors['WHITE'], (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))


def draw_world():
	for y, row in enumerate(world_data):
		for x, tile in enumerate(row):
			if tile >= 0:
				screen.blit(img_list[tile], (x * TILE_SIZE - scroll[0], y * TILE_SIZE))


def load_level(level, world_data, temp):
    temp[0] = 0
    
    try:
        with open(f'{pathh}/dependencies/levels/level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)
    except FileNotFoundError:
        
        world_data.clear()  
        for row in range(ROWS):
            r = [-1] * COLS  
            world_data.append(r)
        with open(f'{pathh}/dependencies/levels/level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerows(world_data)  

def save_level(level,world_data,pathh):
	with open(f'{pathh}/dependencies/levels/level{level}_data.csv', 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			writer.writerows(world_data)
			

run = True
load_level(level,world_data,scroll) # Loads the first level
while run:
	
	clock.tick(FPS_CAP)
	
	draw_bg()
	draw_grid()
	draw_world()

	draw_text(f'Level: {level}', font, colors['WHITE'], 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
	draw_text('Press UP or DOWN to change level', font, colors['WHITE'], 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)
	keys = pygame.key.get_pressed()

	if save_button.draw(screen) or ((keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]) and keys[pygame.K_s]):
		save_level(level,world_data,pathh)
	if load_button.draw(screen) or keys[pygame.K_RETURN]:
		load_level(level,world_data,scroll)	
		
	if left_arrow_button.draw(screen) or keys[pygame.K_LEFT]:
		if scroll[0]  > 0:
			scroll[0] -= 5 * scroll_speed
	if right_arrow_button.draw(screen) or keys[pygame.K_RIGHT]:
		if scroll[0] < (COLS * TILE_SIZE) - SCREEN_WIDTH:
			scroll[0] += 5 * scroll_speed

	pygame.draw.rect(screen, colors['GREEN'], (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

	button_count = 0
	for button_count, i in enumerate(button_list):
		if i.draw(screen):
			current_tile = button_count

	pygame.draw.rect(screen, colors['RED'], button_list[current_tile].rect, 3)
 
	pos = pygame.mouse.get_pos()
	x = (pos[0] + scroll[0]) // TILE_SIZE
	y = pos[1] // TILE_SIZE

	if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
		if pygame.mouse.get_pressed()[0] == 1:
			if world_data[y][x] != current_tile:
				world_data[y][x] = current_tile
		if pygame.mouse.get_pressed()[2] == 1:
			world_data[y][x] = -1

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.QUIT:
				run = False
			if event.key == pygame.K_UP:
				level += 1
			if event.key == pygame.K_DOWN and level > 1:
				level -= 1
			if event.key == pygame.K_LSHIFT:
				scroll_speed = 5
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LSHIFT:
				scroll_speed = 1
					
		mouse = pygame.mouse.get_pos()
		keys = pygame.key.get_pressed()

	pygame.display.update()
	
pygame.quit()


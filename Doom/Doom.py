import pygame
import math
import sys

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Texturas
wall_texture = pygame.image.load('wall2.png').convert()
floor_texture = pygame.image.load('floor.png').convert()
sky_texture = pygame.image.load('sky.png').convert()
door_texture = pygame.image.load('door.png').convert_alpha()

# Carregar a spritesheet de armas
spritesheet = pygame.image.load("shotgun_1.png").convert_alpha()

# Função para extrair um sprite de uma posição específica na spritesheet
def get_weapon_sprite(sheet, x, y, width, height):
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), (x, y, width, height))
    return sprite

# Dimensões de cada sprite na spritesheet
SPRITE_WIDTH = 82
SPRITE_HEIGHT = 95

# Escolha da arma na grid (coluna, linha) da spritesheet
coluna = 1  # de 0 a 3
linha = 0   # de 0 a 2

# Coordenadas do sprite desejado
weapon_x = SPRITE_WIDTH * coluna
weapon_y = SPRITE_HEIGHT * linha

# Recorta o sprite da arma
weapon_sprite = get_weapon_sprite(spritesheet, weapon_x, weapon_y, SPRITE_WIDTH, SPRITE_HEIGHT)

TILE = 64
MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,1,0,1,0,1],
    [1,0,1,0,1,1,1,2,2,1,0,1,0,1,0,1],
    [1,0,1,0,1,0,0,0,0,1,0,1,0,1,0,1],
    [1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,1],
    [1,0,1,0,1,0,0,0,0,1,0,1,0,1,0,1],
    [1,0,1,0,1,1,1,1,1,1,0,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

player_x, player_y = 100, 100
player_angle = 0

FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 120
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 3 * DIST * TILE
SCALE = screen_width // NUM_RAYS

# Função para desenhar minimapa circular
def draw_minimap():
    minimap_radius = 75
    minimap_surface = pygame.Surface((minimap_radius*2, minimap_radius*2), pygame.SRCALPHA)
    pygame.draw.circle(minimap_surface, (0, 0, 0, 180), (minimap_radius, minimap_radius), minimap_radius)
    for y, row in enumerate(MAP):
        for x, tile in enumerate(row):
            if tile:
                rect = pygame.Rect(x * 4, y * 4, 4, 4)
                pygame.draw.rect(minimap_surface, WHITE, rect)
    px, py = int(player_x / TILE * 4), int(player_y / TILE * 4)
    pygame.draw.circle(minimap_surface, RED, (px, py), 4)
    screen.blit(minimap_surface, (10, 10))

# HUD com vida e inventário
player_health = 100
def draw_hud():
    pygame.draw.rect(screen, RED, (10, screen_height - 40, 200, 20))
    pygame.draw.rect(screen, GREEN, (10, screen_height - 40, 2 * player_health, 20))
    pygame.draw.rect(screen, WHITE, (10, screen_height - 70, 300, 25), 2)  # Inventário

# Raycasting para paredes
def mapping(a, b):
    return int(a // TILE), int(b // TILE)

def ray_casting():
    start_angle = player_angle - HALF_FOV
    for ray in range(NUM_RAYS):
        angle = start_angle + ray * DELTA_ANGLE
        sin_a = math.sin(angle)
        cos_a = math.cos(angle)
        for depth in range(1, MAX_DEPTH):
            x = player_x + depth * cos_a
            y = player_y + depth * sin_a
            i, j = mapping(x, y)
            if MAP[j][i]:
                if MAP[j][i] == 2:
                    texture = door_texture
                else:
                    texture = wall_texture
                depth *= math.cos(player_angle - angle)
                proj_height = PROJ_COEFF / (depth + 0.0001)
                wall_column = pygame.transform.scale(texture, (SCALE, int(proj_height)))
                screen.blit(wall_column, (ray * SCALE, (screen_height // 2) - proj_height // 2))
                break

# Movimento
def move():
    global player_x, player_y, player_angle
    speed = 3
    angle_speed = 0.04
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player_angle -= angle_speed
    if keys[pygame.K_RIGHT]: player_angle += angle_speed
    dx = dy = 0
    if keys[pygame.K_w]:
        dx += speed * math.cos(player_angle)
        dy += speed * math.sin(player_angle)
    if keys[pygame.K_s]:
        dx -= speed * math.cos(player_angle)
        dy -= speed * math.sin(player_angle)
    if keys[pygame.K_a]:
        dx += speed * math.sin(player_angle)
        dy -= speed * math.cos(player_angle)
    if keys[pygame.K_d]:
        dx -= speed * math.sin(player_angle)
        dy += speed * math.cos(player_angle)

    scale = 10
    if not MAP[int((player_y + dy * scale) // TILE)][int((player_x + dx * scale) // TILE)]:
        player_x += dx
        player_y += dy

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))

    # Céu
    screen.blit(pygame.transform.scale(sky_texture, (screen_width, screen_height // 2)), (0, 0))
    # Chão
    screen.blit(pygame.transform.scale(floor_texture, (screen_width, screen_height // 2)), (0, screen_height // 2))

    move()
    ray_casting()
    draw_minimap()
    draw_hud()

    # Desenhar a arma (recortada e renderizada)
    weapon_pos = (screen_width // 2 - weapon_sprite.get_width() // 2, screen_height - weapon_sprite.get_height())
    screen.blit(weapon_sprite, weapon_pos)

    pygame.display.flip()
    clock.tick(60)
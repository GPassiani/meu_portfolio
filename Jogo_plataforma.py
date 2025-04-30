import pygame
import sys

# Inicializar o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Forest Platformer")

clock = pygame.time.Clock()

# Cores
SKY_BLUE = (135, 206, 235)
WHITE = (255, 255, 255)

# Carregar sprites
TILE_SIZE = 64

ground_img = pygame.transform.scale(pygame.image.load('terra_tile.png'), (TILE_SIZE, TILE_SIZE))
brick_img = pygame.transform.scale(pygame.image.load('pedra_tile.png'), (TILE_SIZE, TILE_SIZE))
magic_box_img = pygame.transform.scale(pygame.image.load('caixa_magica_tile.png'), (TILE_SIZE, TILE_SIZE))
portal_top_img = pygame.transform.scale(pygame.image.load('portal_top.png'), (TILE_SIZE, TILE_SIZE))
hero_img = pygame.transform.scale(pygame.image.load('heroi_sprite.png'), (TILE_SIZE, TILE_SIZE))

# Map Layout
level_layout = [
    '                            ',
    '                            ',
    '                            ',
    '        M                   ',
    '    B      B          P     ',
    'GGGGGGGGGGGGGGGGGGGGGGGGGGGG',
]

# Cria retângulos para colisão
tiles = []

for row_idx, row in enumerate(level_layout):
    for col_idx, tile in enumerate(row):
        x = col_idx * TILE_SIZE
        y = row_idx * TILE_SIZE + 200  # desce o mapa
        if tile in ('G', 'B', 'M', 'P'):
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            tiles.append((tile, rect))

# Herói
hero_rect = pygame.Rect(100, HEIGHT - 300, TILE_SIZE, TILE_SIZE)
hero_speed_x = 0
hero_speed_y = 0
gravity = 0.5
jump_power = -12
on_ground = False

# Inimigos
enemy_speed = 2
enemy_rects = [
    pygame.Rect(400, HEIGHT - 250, TILE_SIZE, TILE_SIZE),
    pygame.Rect(600, HEIGHT - 250, TILE_SIZE, TILE_SIZE)
]

# Função para desenhar o mapa
def draw_level():
    for tile, rect in tiles:
        if tile == 'G':
            screen.blit(ground_img, (rect.x, rect.y))
        elif tile == 'B':
            screen.blit(brick_img, (rect.x, rect.y))
        elif tile == 'M':
            screen.blit(magic_box_img, (rect.x, rect.y))
        elif tile == 'P':
            screen.blit(portal_top_img, (rect.x, rect.y))
          

# Função para checar colisão horizontal
def check_collision_x(rect, tiles):
    for tile, tile_rect in tiles:
        if tile in ('G', 'B', 'M') and rect.colliderect(tile_rect):
            return tile_rect
    return None

# Função para checar colisão vertical
def check_collision_y(rect, tiles):
    for tile, tile_rect in tiles:
        if tile in ('G', 'B', 'M') and rect.colliderect(tile_rect):
            return tile_rect
    return None

# Função de vitória
def victory_screen():
    font = pygame.font.SysFont(None, 80)
    text = font.render('Você venceu!', True, WHITE)
    rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.fill((0,0,0))
    screen.blit(text, rect)
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

# Função de morte
def death_screen():
    font = pygame.font.SysFont(None, 80)
    text = font.render('Você morreu!', True, WHITE)
    rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.fill((0,0,0))
    screen.blit(text, rect)
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

# Função para mover o inimigo
def move_enemy(enemy_rect):
    if enemy_rect.left <= 0 or enemy_rect.right >= WIDTH:
        return -enemy_speed
    return enemy_speed

# Loop principal
running = True
while running:
    clock.tick(60)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimentação do herói
    keys = pygame.key.get_pressed()
    hero_speed_x = 0
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        hero_speed_x = -5
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        hero_speed_x = 5
    if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and on_ground:
        hero_speed_y = jump_power

    # Aplicar movimento horizontal
    hero_rect.x += hero_speed_x
    collision_tile = check_collision_x(hero_rect, tiles)
    if collision_tile:
        if hero_speed_x > 0:
            hero_rect.right = collision_tile.left
        if hero_speed_x < 0:
            hero_rect.left = collision_tile.right

    # Aplicar gravidade
    hero_speed_y += gravity
    hero_rect.y += hero_speed_y
    collision_tile = check_collision_y(hero_rect, tiles)
    on_ground = False
    if collision_tile:
        if hero_speed_y > 0:
            hero_rect.bottom = collision_tile.top
            hero_speed_y = 0
            on_ground = True
        elif hero_speed_y < 0:
            hero_rect.top = collision_tile.bottom
            hero_speed_y = 0

    # Checar vitória
    for tile, rect in tiles:
        if tile == 'P' and hero_rect.colliderect(rect):
            victory_screen()

    # Checar morte
    if hero_rect.bottom > HEIGHT or any(hero_rect.colliderect(enemy) for enemy in enemy_rects):
        death_screen()

    # Movimentar inimigos
    for enemy_rect in enemy_rects:
        enemy_rect.x += move_enemy(enemy_rect)

    # Desenhar tudo
    screen.fill(SKY_BLUE)
    draw_level()
    screen.blit(hero_img, (hero_rect.x, hero_rect.y))
    for enemy_rect in enemy_rects:
        pygame.draw.rect(screen, (255, 0, 0), enemy_rect)  # Inimigo em vermelho

    pygame.display.update()

pygame.quit()
sys.exit()
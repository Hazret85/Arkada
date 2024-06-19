import pygame
import random
import sys
import time

# Инициализация Pygame
pygame.init()

# Настройка экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Avoid the Blocks')

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Параметры игрока
player_size = 50
player_pos = [screen_width // 2, screen_height - 2 * player_size]

# Параметры врагов
enemy_size = 50
enemy_pos = [random.randint(0, screen_width-enemy_size), 0]
enemy_list = [enemy_pos]
enemy_speed = 10

# Настройка скорости игры
clock = pygame.time.Clock()

# Функция создания врагов
def create_enemies(enemy_list, enemy_size, screen_width):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, screen_width - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

# Функция прорисовки врагов
def draw_enemies(enemy_list, enemy_size):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, RED, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

# Функция обновления позиций врагов
def update_enemy_positions(enemy_list, enemy_speed, screen_height):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < screen_height:
            enemy_pos[1] += enemy_speed
        else:
            enemy_list.pop(idx)

# Функция проверки коллизий
def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
    return False

# Функция обнаружения столкновений
def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True
    return False

# Функция для текста
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Функция для начального экрана
def main_menu():
    menu = True
    click = False
    while menu:
        screen.fill(BLACK)
        draw_text('Avoid the Blocks', pygame.font.Font(None, 74), WHITE, screen, 200, 100)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(300, 250, 200, 50)
        button_2 = pygame.Rect(300, 350, 200, 50)

        if button_1.collidepoint((mx, my)):
            if click:
                game_loop(1)
        if button_2.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()

        pygame.draw.rect(screen, GREEN, button_1)
        pygame.draw.rect(screen, RED, button_2)

        draw_text('Start', pygame.font.Font(None, 50), WHITE, screen, 370, 260)
        draw_text('Exit', pygame.font.Font(None, 50), WHITE, screen, 370, 360)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(30)

# Основной игровой цикл
def game_loop(level):
    player_pos = [screen_width // 2, screen_height - 2 * player_size]
    enemy_list = [enemy_pos]
    game_over = False
    start_time = time.time()
    enemy_speed = 10 + (level - 1) * 5
    enemy_size = 50 - (level - 1) * 10

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                x = player_pos[0]
                y = player_pos[1]
                if event.key == pygame.K_LEFT:
                    x -= player_size
                elif event.key == pygame.K_RIGHT:
                    x += player_size

                player_pos = [x, y]

        screen.fill(BLACK)

        create_enemies(enemy_list, enemy_size, screen_width)
        update_enemy_positions(enemy_list, enemy_speed, screen_height)
        if collision_check(enemy_list, player_pos):
            game_over = True

        draw_enemies(enemy_list, enemy_size)

        pygame.draw.rect(screen, WHITE, (player_pos[0], player_pos[1], player_size, player_size))

        if time.time() - start_time > 10:
            draw_text('You Win!', pygame.font.Font(None, 74), WHITE, screen, 300, 250)
            pygame.display.update()
            time.sleep(2)
            level += 1
            main_menu()
            game_loop(level)

        clock.tick(30)

        pygame.display.update()

    pygame.quit()

main_menu()

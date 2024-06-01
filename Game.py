import pygame
import sys
import pytmx
from pytmx.util_pygame import load_pygame
import json
import os
import random

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TILE_SIZE = 40
NUM_LIVES = 5

# Цвета
WHITE = (255, 255, 255)
PINK = (255, 102, 204)
BLACK = (0, 0, 0)
PINK2 = (195, 38, 150)

# Настройка экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dark Plants")

# Шрифт
typeface = 'Keleti-Regular.ttf'
font = pygame.font.Font(typeface, 74)
button_font = pygame.font.Font(typeface, 50)
score_font = pygame.font.Font(typeface, 36)

# Загрузка карты
tmx_data = load_pygame('Фон/Тёмная версия фона.tmx')

# Пути к файлам
SAVE_FILE = 'savegame.json'
SCORES_FILE = 'scores.json'
BACKGROUND_IMAGE = 'b ground.png'
LIFE_IMAGE = 'сердце.png'
BERRY_IMAGE = 'ягода жизни.png'
MENU_BUTTON_IMAGE = 'главное меню.png'
BACK_BUTTON_IMAGE = 'стрелочка обратно.png'

# Переменные игры
game_data = {
    'player_pos': [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2],
    'score': 0
}

# Загрузка изображений для анимации
def load_animation_images(prefix, indices):
    images = []
    for i in indices:
        try:
            images.append(pygame.image.load(f'{prefix}/{i}.png'))
        except pygame.error as e:
            print(f"Не удалось загрузить изображение: {prefix}/{i}.png")
            sys.exit(1)
    return images

walk_down_images = load_animation_images('images', [1, 2, 3, 4])
walk_left_images = load_animation_images('images', [5, 6, 7, 8])
walk_right_images = load_animation_images('images', [9, 10, 11, 12])
walk_up_images = load_animation_images('images', [13, 14, 15, 16])

attack_down_images = load_animation_images('Atak', [1, 2, 3, 4])
attack_left_images = load_animation_images('Atak', [5, 6, 7, 8])
attack_right_images = load_animation_images('Atak', [9, 10, 11, 12])
attack_up_images = load_animation_images('Atak', [13, 14, 15, 16])

# Загрузка других изображений
life_image = pygame.image.load(LIFE_IMAGE)
berry_image = pygame.image.load(BERRY_IMAGE)
menu_button_image = pygame.image.load(MENU_BUTTON_IMAGE)
back_button_image = pygame.image.load(BACK_BUTTON_IMAGE)

# Функции работы с файлами
def save_game(data):
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f)

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            return json.load(f)
    return None

def save_score(score):
    scores = load_scores()
    scores.append(score)
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f)

def load_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE, 'r') as f:
            return json.load(f)
    return []

# Функция отображения меню
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

def show_menu():
    try:
        background = pygame.image.load("b_ground.png")
    except pygame.error as e:
        print(f"Не удалось загрузить изображение фона: b_ground.png")
        sys.exit(1)

    screen.blit(background, (0, 0))

    draw_text('Dark Plants', font, PINK2, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

    button_width = 300
    button_height = 50
    button_x = SCREEN_WIDTH // 2 - button_width // 2
    button_start = pygame.Rect(button_x, SCREEN_HEIGHT // 2 - 50, button_width, button_height)
    button_scores = pygame.Rect(button_x, SCREEN_HEIGHT // 2 + 20, button_width, button_height)
    button_exit = pygame.Rect(button_x, SCREEN_HEIGHT // 2 + 90, button_width, button_height)

    pygame.draw.rect(screen, WHITE, button_start)
    pygame.draw.rect(screen, WHITE, button_scores)
    pygame.draw.rect(screen, WHITE, button_exit)

    draw_text('Начать игру', button_font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 25)
    draw_text('Результаты', button_font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 45)
    draw_text('Выйти из игры', button_font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 115)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_start.collidepoint(event.pos):
                    return 'create'
                if button_scores.collidepoint(event.pos):
                    return 'scores'
                if button_exit.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

# Функция отображения результатов
def show_scores():
    try:
        background = pygame.image.load("b_ground.png")
    except pygame.error as e:
        print(f"Не удалось загрузить изображение фона: b_ground.png")
        sys.exit(1)

    screen.blit(background, (0, 0))

    draw_text('Результаты', font, PINK2, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

    scores = load_scores()
    y_offset = SCREEN_HEIGHT // 4 + 50
    for score in scores[-10:]:
        draw_text(f'{score} очков', button_font, WHITE, screen, SCREEN_WIDTH // 2, y_offset)
        y_offset += 50

    back_button_rect = back_button_image.get_rect(topleft=(20, 20))
    screen.blit(back_button_image, back_button_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    return

# Функция размещения ягод жизни
def place_berries(num_berries, map_width, map_height):
    berries = []
    for _ in range(num_berries):
        x = random.randint(0, map_width - 1) * TILE_SIZE
        y = random.randint(0, map_height - 1) * TILE_SIZE
        berries.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
    return berries

# Игровой цикл
def main():
    global game_data
    if os.path.exists(SAVE_FILE):
        game_data = load_game()

    player_pos = game_data['player_pos']
    player_speed = 2  # скорость передвижения
    score = game_data['score']
    lives = NUM_LIVES

    # Камера
    camera = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

    # Анимационные переменные
    current_frame = 0
    animation_speed = 0.1
    direction = 'down'
    is_moving = False
    is_attacking = False
    attack_frame = 0
    attack_pos = player_pos.copy()

    running = True
    clock = pygame.time.Clock()

    # Размещение ягод жизни
    map_width = tmx_data.width
    map_height = tmx_data.height
    berries = place_berries(10, map_width, map_height)

    menu_button_rect = menu_button_image.get_rect(topright=(SCREEN_WIDTH - 20, 20))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game({'player_pos': player_pos, 'score': score})
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    is_attacking = True
                    attack_frame = 0
                    attack_pos = player_pos.copy()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button_rect.collidepoint(event.pos):
                    save_game({'player_pos': player_pos, 'score': score})
                    return

        keys = pygame.key.get_pressed()
        is_moving = False
        if not is_attacking:
            if keys[pygame.K_w] and keys[pygame.K_a]:
                player_pos[1] -= player_speed
                player_pos[0] -= player_speed
                direction = 'left'
                is_moving = True
            elif keys[pygame.K_w] and keys[pygame.K_d]:
                player_pos[1] -= player_speed
                player_pos[0] += player_speed
                direction = 'right'
                is_moving = True
            elif keys[pygame.K_s] and keys[pygame.K_a]:
                player_pos[1] += player_speed
                player_pos[0] -= player_speed
                direction = 'left'
                is_moving = True
            elif keys[pygame.K_s] and keys[pygame.K_d]:
                player_pos[1] += player_speed
                player_pos[0] += player_speed
                direction = 'right'
                is_moving = True
            elif keys[pygame.K_w]:
                player_pos[1] -= player_speed
                direction = 'up'
                is_moving = True
            elif keys[pygame.K_s]:
                player_pos[1] += player_speed
                direction = 'down'
                is_moving = True
            elif keys[pygame.K_a]:
                player_pos[0] -= player_speed
                direction = 'left'
                is_moving = True
            elif keys[pygame.K_d]:
                player_pos[0] += player_speed
                direction = 'right'
                is_moving = True

        # Ограничение перемещения камеры краями карты
        if player_pos[0] < SCREEN_WIDTH // 2:
            camera.x = 0
        elif player_pos[0] > map_width - SCREEN_WIDTH // 2:
            camera.x = map_width - SCREEN_WIDTH
        else:
            camera.x = player_pos[0] - SCREEN_WIDTH // 2

        if player_pos[1] < SCREEN_HEIGHT // 2:
            camera.y = 0
        elif player_pos[1] > map_height - SCREEN_HEIGHT // 2:
            camera.y = map_height - SCREEN_HEIGHT
        else:
            camera.y = player_pos[1] - SCREEN_HEIGHT // 2

        # Обновление позиции камеры
        camera.center = player_pos

        # Обновление кадра анимации
        if is_moving:
            current_frame += animation_speed
            if current_frame >= len(walk_down_images):
                current_frame = 0
        else:
            current_frame = 0  # Остановка на первом кадре

        if is_attacking:
            attack_frame += animation_speed
            if attack_frame >= len(attack_down_images):
                is_attacking = False
                attack_frame = 0

        # Выбор текущего кадра в зависимости от направления и состояния
        if is_attacking:
            player_pos = attack_pos.copy()  # Фиксация позиции игрока при атаке
            if direction == 'up':
                player_image = attack_up_images[int(attack_frame)]
            elif direction == 'down':
                player_image = attack_down_images[int(attack_frame)]
            elif direction == 'left':
                player_image = attack_left_images[int(attack_frame)]
            elif direction == 'right':
                player_image = attack_right_images[int(attack_frame)]
        else:
            if direction == 'up':
                player_image = walk_up_images[int(current_frame)]
            elif direction == 'down':
                player_image = walk_down_images[int(current_frame)]
            elif direction == 'left':
                player_image = walk_left_images[int(current_frame)]
            elif direction == 'right':
                player_image = walk_right_images[int(current_frame)]

        # Проверка на сбор ягод
        player_rect = pygame.Rect(player_pos[0], player_pos[1], TILE_SIZE, TILE_SIZE)
        for berry in berries[:]:
            if player_rect.colliderect(berry):
                berries.remove(berry)
                score += 10

        # Отрисовка
        screen.fill(BLACK)

        # Отрисовка карты
        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        screen.blit(tile, (x * tmx_data.tilewidth - camera.x, y * tmx_data.tileheight - camera.y))

        # Отрисовка ягод жизни
        for berry in berries:
            screen.blit(berry_image, (berry.x - camera.x, berry.y - camera.y))

        # Отрисовка игрока
        screen.blit(player_image, (player_pos[0] - camera.x, player_pos[1] - camera.y))

        # Отрисовка интерфейса
        for i in range(lives):
            screen.blit(life_image, (20 + i * 40, 20))

        # Отображение счёта
        draw_text(f'Счёт: {score}', score_font, WHITE, screen, 100, 60)

        # Отображение кнопки меню
        screen.blit(menu_button_image, menu_button_rect)
        clock.tick(FPS)

        pygame.display.flip()

    # Сохранение данных при выходе
    save_game({'player_pos': player_pos, 'score': score})

if __name__ == '__main__':
    while True:
        mode = show_menu()
        if mode == 'create':
            main()
        elif mode == 'scores':
            show_scores()


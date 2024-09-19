import pygame
import random
import math

# Инициализация PyGame
pygame.init()

# Настройки экрана
screen = pygame.display.set_mode((1024, 1024))

# Заголовок и иконка
pygame.display.set_caption("Spaceship Battle")
icon = pygame.image.load('media/menu_background.jpg')
pygame.display.set_icon(icon)

# Фон
background = pygame.image.load('media/game_background.jpg')

# Звук
pygame.mixer.music.load('media/background_music.mp3')
pygame.mixer.music.play(-1)
# Игрок
player_img = pygame.image.load('media/spaceship_hero_model.png')
player_img = pygame.transform.scale(player_img, (50, 62))
player_x = 370
player_y = 700
player_x_change = 0

# Враг
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_ = pygame.image.load('media/spaceship_enemy_model.png')
    enemy_img.append(pygame.transform.scale(enemy_, (46, 80)))
    enemy_x.append(random.randint(0, 978))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(0.5)
    enemy_y_change.append(10)

# Пуля
bullet_img = pygame.image.load('media/bullet.png')
bullet_img = pygame.transform.scale(bullet_img, (16, 16))
bullet_x = 0
bullet_y = 700
bullet_x_change = 0
bullet_y_change = 1.5
bullet_state = "ready"  # "ready" - готово к стрельбе, "fire" - пуля в полете

# Очки
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# Конец игры
game_over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (300, 300))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    if distance < 27:
        return True
    else:
        return False


# Основной игровой цикл
running = True
while running:

    # Заливка фона
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Проверка нажатия клавиш
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -1
            if event.key == pygame.K_RIGHT:
                player_x_change = 1
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Движение игрока
    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 974:
        player_x = 974

    # Движение врагов
    for i in range(num_of_enemies):

        # Конец игры
        if enemy_y[i] > 800:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 0.5
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 978:
            enemy_x_change[i] = -0.5
            enemy_y[i] += enemy_y_change[i]

        # Столкновение
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            bullet_y = 700
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)

    # Движение пули
    if bullet_y <= 0:
        bullet_y = 700
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()

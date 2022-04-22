import pygame
import random
import math
from pygame import mixer

WIDTH = 800
HEIGHT = 600
GAME_SPEED = 1
# Initialize Pygame
pygame.init()
# Create screen

# Background sound
# mixer.music.load("background.wav")
# mixer.music.play(-1)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("data/img/spaceship.png")
pygame.display.set_icon(icon)

# loading and scaling the background image
bg = pygame.image.load("data/img/bg.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# Player
player_img = pygame.image.load("data/img/player.png")
player_x = 370
player_y = 480
player_x_change = 0

# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):

    enemy = (pygame.image.load("data/img/enemy.png"))
    enemy_img.append(enemy)
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(30, 120))
    enemy_x_change.append(GAME_SPEED)
    enemy_y_change.append(40)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - bullet is on the screen
bullet_img = pygame.image.load("data/img/bullet.png")
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 5
bullet_state = "ready"

# Tracking Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

text_x = 10
text_y = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) +
                         (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True

while running:
    # Set background image
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Checks if a key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -GAME_SPEED
            if event.key == pygame.K_RIGHT:
                player_x_change = +GAME_SPEED
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("data/sound/laser.wav")
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # CHecking the boundary of the screen
    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    if player_x >= 736:
        player_x = 736
    player(player_x, player_y)

    # Enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = GAME_SPEED
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -GAME_SPEED
            enemy_y[i] += enemy_y_change[i]

        # Collision
        collision = is_collision(
            enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            explosion_sound = mixer.Sound("data/sound/explosion.wav")
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(30, 120)
        enemy(enemy_x[i], enemy_y[i], i)

    # Bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
        bullet_state == "ready"
    show_score(text_x, text_y)

    pygame.display.update()

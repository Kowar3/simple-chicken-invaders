import pygame
import random
import math as m
from pygame import mixer

enemy_list = []

pygame.init()

screen = pygame.display.set_mode((800, 600))

pozadina = pygame.image.load("background.png")

mixer.music.load("background.wav")
mixer.music.play(-1)

pygame.display.set_caption("Space Invaders")

icon = pygame.image.load("ufo.png")

pygame.display.set_icon(icon)

running = True

playerSlika = pygame.image.load("space-invaders.png")

playerX = 370
playerY = 480

playerX_promena = 0

for _ in range(6):
    enemy_list.append([random.randint(0, 735), random.randint(50, 300), pygame.image.load("play.png"), 2, 2])

bulletSlika = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletY_promena = 3
bullet_state = False

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
scoreX = 10
scoreY = 10

go_font = pygame.font.Font("freesansbold.ttf", 64)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    kraj_tekst = go_font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(kraj_tekst, (200, 250))

def player(x, y):
    screen.blit(playerSlika, (x, y))

def enemy_function(slika, x, y):
    screen.blit(slika, (x, y))

def ispali_metak(x, y):
    global bullet_state
    bullet_state = True
    screen.blit(bulletSlika, (x + 16, y))

def isCollision(enemyX, enemyY, bulletX, bulletY):

    razdaljina = m.sqrt(pow(enemyX-bulletX, 2) + pow(enemyY-bulletY, 2))

    if razdaljina < 27:
        return True
    return False

while running:

    screen.blit(pozadina, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_promena = -5
            if event.key == pygame.K_RIGHT:
                playerX_promena = 5
            if event.key == pygame.K_SPACE and bullet_state is False:
                zvuk_metka = mixer.Sound("laser.wav")
                zvuk_metka.play()
                bulletX = playerX
                ispali_metak(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_promena = 0

    playerX += playerX_promena

    if playerX <= 0:
        playerX = 0
        playerX_promena = 0
    elif playerX >= 736:
        playerX = 736
        playerX_promena = 0

    for enemy in enemy_list:

        if isCollision(enemy[0], enemy[1], playerX, playerY) or enemy[1] == 2000:
            for j in enemy_list:
                j[1] = 2000
            game_over_text()
            break

        if enemy[0] <= 0 or enemy[0] >= 736:
            enemy[3] = -enemy[3]

        if enemy[1] <= 50 or enemy[1] >= 550:
            enemy[4] = -enemy[4]

        enemy[0] += enemy[3]
        enemy[1] += enemy[4]

        if isCollision(enemy[0], enemy[1], bulletX, bulletY):
            zvuk_pogotka = mixer.Sound("explosion.wav")
            zvuk_pogotka.play()
            bulletY = 480
            bullet_state = False
            score_value += 1
            enemy[0] = random.randint(0, 735)
            enemy[1] = random.randint(50, 300)

        enemy_function(enemy[2], enemy[0], enemy[1])

    if bulletY <= 0:
        bulletY = 480
        bullet_state = False

    if bullet_state:
        ispali_metak(bulletX, bulletY)
        bulletY -= bulletY_promena

    player(playerX, playerY)

    show_score(scoreX, scoreY)

    pygame.display.update()


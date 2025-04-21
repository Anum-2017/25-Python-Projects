import math
import random
import pygame
from pygame import mixer

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('images/background.png')

# Background Sound
mixer.music.load("images/background.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('images/ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('images/player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

def reset_enemies():
    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('images/enemy.png'))
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(4)
        enemyY_change.append(40)

reset_enemies()

# Bullet
bulletImg = pygame.image.load('images/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Pause Text
pause_font = pygame.font.Font('freesansbold.ttf', 48)

# Flags
game_over = False
paused = False

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))
    restart_text = font.render("Press R to Restart", True, (255, 255, 255))
    screen.blit(restart_text, (260, 330))

def pause_text():
    paused_text = pause_font.render("PAUSED", True, (255, 255, 0))
    screen.blit(paused_text, (310, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    return distance < 27

def restart_game():
    global playerX, score_value, bulletY, bullet_state, game_over
    global enemyImg, enemyX, enemyY, enemyX_change, enemyY_change
    enemyImg.clear()
    enemyX.clear()
    enemyY.clear()
    enemyX_change.clear()
    enemyY_change.clear()
    reset_enemies()
    playerX = 370
    bulletY = 480
    bullet_state = "ready"
    score_value = 0
    game_over = False

# Game Loop
running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE and not paused and not game_over:
                if bullet_state == "ready":
                    bulletSound = mixer.Sound("images/laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

            if event.key == pygame.K_p:
                paused = not paused

            if event.key == pygame.K_r and game_over:
                restart_game()

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                playerX_change = 0

    if not paused and not game_over:
        playerX += playerX_change
        playerX = max(0, min(playerX, 736))

        for i in range(num_of_enemies):
            if enemyY[i] > 440:
                game_over = True
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]

            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosionSound = mixer.Sound("images/explosion.wav")
                explosionSound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        # Bullet Movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(10, 10)

    if paused:
        pause_text()

    if game_over:
        game_over_text()

    pygame.display.update()


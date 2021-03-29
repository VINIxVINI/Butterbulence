import pygame
import random
import math
from pygame import mixer

# initializing pygame
pygame.init()

# Creating display screen
screen = pygame.display.set_mode((900, 600))

# Background
BackGround = pygame.image.load('Images/bgCave.png')

# Background sound
mixer.music.load('Sounds/little-village.wav')
mixer.music.play(-1)

# Title and game icon
pygame.display.set_caption("Butter's Adventure")
icon = pygame.image.load('Images/beetle.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('Images/Player.png')
playerX = 400
playerY = 490
changeX = 0

# Enemy 1
enemyImg = pygame.image.load('Images/death.png')
enemyX = random.randint(0, 850)
enemyY = random.randint(10, 80)
changeEnemyX = 4
changeEnemyY = 60

# Bullet
bulletImg = pygame.image.load('Images/Bullet.png')
bulletX = 0
bulletY = 480
changeBulletX = 0
changeBulletY = 10
Bullet_state = "ready"

# Scoring
score_value = 0
font = pygame.font.Font('Fonts/Alphakind.ttf', 32)
textX = 10
textY = 10

# Game over
over_font = pygame.font.Font('Fonts/Alphakind.ttf', 64)


def gameOver():
    screen.fill((254, 220, 86))
    over_text = over_font.render("GAME OVER", True, (100, 50, 50))
    screen.blit(over_text, (200, 250))


def show_Score(x, y):
    score = font.render("Score: " + str(score_value), True, (100, 50, 50))
    screen.blit(score, (x, y))


def Player(x, y):
    screen.blit(playerImg, (x, y))


def Enemy(x, y):
    screen.blit(enemyImg, (x, y))


def fireBullet(x, y):
    global Bullet_state
    Bullet_state = "fire"
    screen.blit(bulletImg, (x + 20, y + 20))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 47:
        return True
    else:
        return False


# Keeping the game running
running = True
while running:
    # Background RGB
    screen.fill((254, 220, 86))

    # Keep Background image
    screen.blit(BackGround, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key stroke configurations
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                changeX = -3
            if event.key == pygame.K_RIGHT:
                changeX = +3
            if event.key == pygame.K_SPACE:
                if Bullet_state == "ready":
                    bullet_sound = mixer.Sound('fx/SilencedGunShot.wav')
                    bullet_sound.play()
                    bulletX = playerX  # Getting current x coordinate of Player
                    fireBullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                changeX = 0

    playerX += changeX

    # Player boundary check to keep in bounds
    if playerX <= -10:
        playerX = 0
    elif playerX >= 825:
        playerX = 815



    # Game over
    if enemyY > 400:
         enemyY = 2000
         gameOver()

    # Enemy movement, relative to boundary
    enemyX += changeEnemyX

    if enemyX <= 0:
        changeEnemyX = 4
        enemyY += changeEnemyY
    elif enemyX >= 790:
        changeEnemyX = -4
        enemyY += changeEnemyY

    # Bullet movement
    if Bullet_state == "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= changeBulletY

    # Multiple Bullets
    if bulletY <= 0:
        bulletY = 480
        Bullet_state = "ready"

    # Collision
    collision = isCollision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        contact_fx = mixer.Sound('fx/SmallLoudExplosion.wav')
        contact_fx.play()
        bulletY = 480
        Bullet_state = "ready"
        score_value += 1
        enemyX = random.randint(0, 850)
        enemyY = random.randint(10, 80)

    Player(playerX, playerY)
    Enemy(enemyX, enemyY)
    show_Score(textX, textY)

    pygame.display.update()

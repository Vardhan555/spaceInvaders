import pygame
import random
import math

from pygame import mixer
pygame.init()

#screen
screen = pygame.display.set_mode((800, 600))

#title
pygame.display.set_caption("Space Invaders")
#background
background = pygame.image.load("background.jpg")

#sound
mixer.music.load("background.wav")
mixer.music.play(-1)
#icon
icon = pygame.image.load('icons8-flying-saucer-48.png')
pygame.display.set_icon(icon)
#player
playerImg = pygame.image.load('shaceship.png')
playerX = 370
playerY = 480
playerX_change = 0

#enemy
enemyX = []
enemyImg = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_enemies = 6

for i in range(num_enemies):
    enemyImg.append(pygame.image.load('asteroid3-removebg-preview.png'))
   # enemyImg.append(pygame.image.load('comet2.jpg'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.3)
    enemyY_change.append(30)


#bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"


score_value = 0
font = pygame.font.Font("Adventure.ttf", 32)
textX= 10
textY= 10

over_font = pygame.font.Font("Adventure.ttf", 70)

def game_over():
    over = over_font.render("Game Over" ,True, (255,255,255))
    screen.blit(over, (200, 250))

def showScore(x ,y):
    score = font.render("Score : "+str(score_value) ,True, (255,255,255))
    screen.blit(score,(x,y))

def player(x , y):
    screen.blit(playerImg, (x, y))

def enemy(x , y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+8, y+10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    dist = math.sqrt(math.pow(enemyX-bulletX,2) + math.pow(enemyY-bulletY,2))
    if dist < 27:
        return True
    else:
        return False
#window
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # key movements
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.4
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.4
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound= mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    screen.fill((0, 0, 0))
    #background image
    screen.blit(background, (0, 0))
    playerX += playerX_change


    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_enemies):

        if enemyY[i] > 400:
            for j in range(num_enemies):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 738:
            enemyX_change[i] = -0.4
            enemyY[i] +=enemyY_change[i]
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)

        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()

        enemy(enemyX[i], enemyY[i] ,i)




    if bulletY <=0 :
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    player(playerX, playerY)
    showScore(textX,textY)
    pygame.display.update()
import math
import random
import pygame
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load('background.png')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Space Invader")

mixer.music.load("Space_Invaders_Juego.wav")

font = pygame.font.Font('calamity.ttf', 32)
over_font = pygame.font.Font('calamity.ttf', 64)

menu_active = True
difficulty = "Normal"

def show_menu():
    screen.blit(background, (0, 0))
    title = over_font.render("SPACE INVADER", True, (255, 165, 0))
    title_rect = title.get_rect(center=(800 // 2, 150))
    screen.blit(title, title_rect)
    option1 = font.render("1. Facil", True, (0, 255, 0))
    option1_rect = option1.get_rect(center=(800 // 2, 250))
    screen.blit(option1, option1_rect)
    option2 = font.render("2. Normal", True, (0, 0, 255))
    option2_rect = option2.get_rect(center=(800 // 2, 300))
    screen.blit(option2, option2_rect)
    option3 = font.render("3. Dificil", True, (255, 0, 0))
    option3_rect = option3.get_rect(center=(800 // 2, 350))
    screen.blit(option3, option3_rect)
    instruction = font.render("Oprime el numero para escoger la dificultad", True, (255, 165, 0))
    instruction_rect = instruction.get_rect(center=(800 // 2, 450))
    screen.blit(instruction, instruction_rect)
    pygame.display.update()

while menu_active:
    show_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                difficulty = "Fácil"
                menu_active = False
            elif event.key == pygame.K_2:
                difficulty = "Normal"
                menu_active = False
            elif event.key == pygame.K_3:
                difficulty = "Difícil"
                menu_active = False

mixer.music.play(-1)

playerImg = pygame.image.load('player.png')
playerX, playerY = 370, 480
playerX_change = 0

if difficulty == "Fácil":
    enemy_speed = 2
elif difficulty == "Normal":
    enemy_speed = 4
elif difficulty == "Difícil":
    enemy_speed = 6

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(enemy_speed)
    enemyY_change.append(40)

bulletImg = pygame.image.load('bullet.png')
bulletX, bulletY = 0, 480
bulletY_change = 10
bullet_state = "ready"

score_value = 0
textX, textY = 10, 10

def show_score(x, y):
    score = font.render(f"Score: {score_value}", True, (255, 165, 0))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 165, 0))
    restart_text = font.render("Presiona R para reiniciar", True, (255, 165, 0))
    screen.blit(over_text, (800 // 2 - over_text.get_width() // 2, 250))
    screen.blit(restart_text, (800 // 2 - restart_text.get_width() // 2, 350))
    pygame.display.update()

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

running = True
game_over = False

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                game_over = False
                score_value = 0
                playerX, playerY = 370, 480
                bullet_state = "ready"
                for i in range(num_of_enemies):
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(50, 150)

            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                mixer.Sound("laser.wav").play()
                bulletX = playerX
                fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    if not game_over:
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        for i in range(num_of_enemies):
            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                game_over = True
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0 or enemyX[i] >= 736:
                enemyX_change[i] *= -1
                enemyY[i] += enemyY_change[i]

            if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
                mixer.Sound("explosion.wav").play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, textY)
    else:
        game_over_text()

    pygame.display.update()
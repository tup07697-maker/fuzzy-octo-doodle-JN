# fuzzy-octo-doodle-JN
import pygame
import random
import math

from pygame import mixer

mixer.init()
pygame.init()

mixer.music.load("backgroundmusic.mp3")
mixer.music.play(-1)


screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("GALAXY DEFENDER")

title_img = pygame.image.load("spacecraft.png")
pygame.display.set_icon(title_img)

background = pygame.image.load("background.jpg")

player_img = pygame.image.load("spaceship.png")

bullet_img = pygame.image.load("bullet.png")

explosion_img = pygame.image.load("explosion.png").convert_alpha()

reset_img = pygame.image.load("reset.png")
reset_rect = reset_img.get_rect()

enemy_img=[]
enemyX=[]
enemyY=[]
enmyspeedX=[]
enmyspeedY=[]
explosion = []

no_of_enemies = 6
base_enemyX = 0.2
base_enemyY = 10

for enmy in range(no_of_enemies):

    enemy_img.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(30,200))
    enmyspeedX.append(base_enemyX)
    enmyspeedY.append(base_enemyY)

spaceshipX = 370
spaceshipY = 480
speedX = 0
bulletX = 386
bulletY = 490
score_value = 0

working = True
check = False
game_over = False
game_over_sound = False

font = pygame.font.SysFont("Times New Roman", 32, "bold") 

def Show_score():
    img = font.render(f"Score: {score_value}", True, "White")
    screen.blit(img,(10,10))

font_gameover = pygame.font.SysFont("Times New Roman", 50, "bold")

def Explosion_created(x,y):
    explosion.append({"x":x,
                      "y":y,
                      "last_update": pygame.time.get_ticks()})

def Gameover():
    go_img = font.render("GAME OVER", True, "White")
    screen.blit(go_img,(300,220))

    reset_rect.center = (400,360)
    screen.blit(reset_img, reset_rect)

def Restart():
    global spaceshipX, spaceshipY, speedX
    global bulletX, bulletY, check
    global score_value, game_over, game_over_sound
    global enemyX,enemyY,enmyspeedX, enmyspeedY

    spaceshipX = 370
    spaceshipY = 480
    speedX = 0
    bulletX = 386
    bulletY = 490
    score_value = 0
    check = False
    game_over = False
    game_over_sound = False

    enemyX.clear()
    enemyY.clear()
    enmyspeedX.clear()
    enmyspeedY.clear()

    for enmy in range(no_of_enemies):
        enemyX.append(random.randint(0,736))
        enemyY.append(random.randint(30,200))
        enmyspeedX.append(base_enemyX)
        enmyspeedY.append(base_enemyY)

    mixer.music.load("backgroundmusic.mp3")
    mixer.music.play(-1)
    
while working:
    screen.blit(background,(0,0)) 

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over and reset_rect.collidepoint(event.pos):
                Restart()
                
        if event.type == pygame.QUIT:
            working = False

        # moving player left and right
        if event.type ==pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speedX =-1
            if event.key == pygame.K_RIGHT:
                speedX = 1

            # creating bullet
            if event.key == pygame.K_SPACE:
                if check is False:
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    check=True
                    bulletX = spaceshipX+16
                
        if event.type == pygame.KEYUP:
            speedX = 0

    if not game_over:
        spaceshipX += speedX
        if spaceshipX <= 0:
            spaceshipX = 0
        elif spaceshipX >=736:
            spaceshipX = 736

    # moving enemy
        for i in range(no_of_enemies):
            if enemyY[i]>420:
                game_over = True
                break

            if score_value <5:
                diff_enmyspeedX = 0.5
                diff_enmyspeedY = 10
            elif score_value <10:
                diff_enmyspeedX = 0.7
                diff_enmyspeedY = 20
            elif score_value < 15:
                diff_enmyspeedX = 0.9
                diff_enmyspeedY = 30
            else:
                diff_enmyspeedX = 1.1
                diff_enmyspeedY = 40

            if enmyspeedX[i] > 0:
                enmyspeedX[i] = diff_enmyspeedX
            else:
                enmyspeedX[i] = -diff_enmyspeedX

            enmyspeedY[i] = diff_enmyspeedY


            enemyX[i]+=enmyspeedX[i]
        
            if enemyX[i]<=0:
                enmyspeedX[i] = 0.25
                enemyY[i] +=enmyspeedY[i]
        
            if enemyX [i] >=736:
                enmyspeedX[i] = -0.25
                enemyY[i] +=enmyspeedY[i]

            distance = math.sqrt((math.pow(bulletX - enemyX[i],2)) + (math.pow(bulletY - enemyY[i],2)))
            if distance <30:
                explosionSound = mixer.Sound("explosion.wav")
                explosionSound.play()

                Explosion_created(enemyX[i], enemyY[i])
                
                bulletY = 480
                check = False
                enemyX[i] = random.randint(0,736)
                enemyY[i] = random.randint(30,200)
                score_value +=1

            screen.blit(enemy_img[i], (enemyX[i],enemyY[i]))

        if bulletY <=0:
            bulletY = 490
            check = False
        
        if check is True:
            screen.blit(bullet_img,(bulletX,bulletY))
            bulletY -=2

    if game_over:
        if not game_over_sound:
            mixer.music.stop()
            GameOverSound = mixer.Sound("gameover.wav")
            GameOverSound.play()
            game_over_sound = True

        Gameover()


    for e in explosion[:]:
        current_time = pygame.time.get_ticks()

        if current_time - e["last_update"] < 200:
            screen.blit(explosion_img, (e["x"]-20, e["y"]-20))
        else:
            explosion.remove(e)
            
    
    screen.blit(player_img, (spaceshipX,spaceshipY))
    Show_score()
    pygame.display.update()
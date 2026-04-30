import pygame
import random
import math

from pygame import mixer

mixer.init()
pygame.init()

mixer.music.load("backgroundmusic.mp3")
mixer.music.play(-1)

laser_sound = mixer.Sound("laser.wav")
explosion_sound = mixer.Sound("explosion.wav")
gameover_sound = mixer.Sound("gameover.wav")

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("GALAXY DEFENDER")

title_img = pygame.image.load("spacecraft.png")
pygame.display.set_icon(title_img)

intro_page_img = pygame.image.load("intro_page.webp")
intro_page_img = pygame.transform.scale(intro_page_img, (800,600))

background_img = pygame.image.load("background.jpg")
background_img = pygame.transform.scale(background_img, (800,600))

boss_background_img = pygame.image.load("boss_background.webp")
boss_background_img = pygame.transform.scale(boss_background_img, (800, 600))

player_img = pygame.image.load("spaceship.png")

player_bullet_img = pygame.image.load("bullet.png")

enmy_bullet_img = pygame.image.load("laser.png")

boss_img = pygame.image.load("monster.png").convert_alpha()

boss_bullet_img = pygame.image.load("nuclear-bomb.png")
boss_bullet_img = pygame.transform.scale(boss_bullet_img, (45,45))

explosion_img = pygame.image.load("explosion.png").convert_alpha()

reset_img = pygame.image.load("reset.png")
reset_rect = reset_img.get_rect()

enemy_img=[]
enemyX=[]
enemyY=[]
enmyspeedX=[]
enmyspeedY=[]
explosion = []
enemy_bullet = []
boss_bullets = []

no_of_enemies = 6
base_enemyX = 0.2
base_enemyY = 10
enmy_bullet_speed = 1.5
last_enmy_shot = 0
enemy_shot_delay = 1200

boss_bullet_speed = 0.5
last_boss_shot = 0
boss_shot_delay = 800
boss_attack_count = 0

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
player_health = 4
max_health = 4

start_page= True
game_started= False
working = True
check = False
game_over = False
game_over_sound = False
game_won = False

#boss level
boss_intro = False
boss_intro_show = False
boss_level = False
boss_spawned = False
bossX = 350
bossY = 50
boss_speedX = 0.4
boss_health = 10
boss_max_health = 10
boss_trig_score = 10
boss_phase = 1

font_title = pygame.font.SysFont("Times New Roman", 55, "bold")
font = pygame.font.SysFont("Times New Roman", 32, "bold")
font_gameover = pygame.font.SysFont("Times New Roman", 55, "bold")
font_warning = pygame.font.SysFont("Times New Roman", 50, "bold")
font_text = pygame.font.SysFont("Times New Roman", 30, "bold")


def Intro_screen():
    title = font_title.render("GALAXY DEFENDER", True, "White")
    l1 = font_text.render("Defeat all Enemies and survive the Boss fight", True, "Green")
    l2 = font_text.render("Left/ Right Arrow key to Move", True, "White")
    l3 = font_text.render("Spacebar to Shoot", True, "Blue")
    l4 = font_text.render("Press any key to begin", True, "Yellow")
    l5 = font_text.render("Boss level starts after your score reaches 10", True, "Green")
    
    screen.blit(title, (130,150))
    screen.blit(l1, (140,250))
    screen.blit(l2, (210,310))
    screen.blit(l3, (280,360))
    screen.blit(l4, (260,440))
    screen.blit(l5, (160,400))
    
def Show_score():
    img = font.render(f"Score: {score_value}", True, "White")
    screen.blit(img,(10,10))

def Show_health():
    pygame.draw.rect(screen, "red", (600,10,150,20))
    pygame.draw.rect(screen, "green", (600,10,150 * (player_health / max_health), 20))

    player_health_img = font_text.render("Player Health:", True, "White")
    screen.blit(player_health_img, (420,8))

def Show_boss_health():
    if boss_level:
        pygame.draw.rect(screen, "red", (250,40,300,20))
        pygame.draw.rect(screen, "purple", (250, 40, 300 * (boss_health/ boss_max_health), 20))

def Enemy_shoot(x,y):
    enemy_bullet.append({
        "x": x +16,
        "y": y + 20
        })

def Boss_intro_screen():
    health_restored = font_warning.render("HEALTH RESTORED", True, "Green")
    warning = font_warning.render("WARNING!!!", True, "Red")
    boss_incoming = font_text.render("Boss Incoming...", True, "White")
    boss_life = font_text.render("Boss Health = 10", True, "White")
    key = font_text.render("Press ENTER to begin...", True,"White")

    screen.blit(health_restored, (160, 140))
    screen.blit(warning, (270,200))
    screen.blit(boss_incoming, (300,270))
    screen.blit(boss_life, (300,340))
    screen.blit(key, (250,400))

def Boss_shoot(x,y):
    global boss_attack_count

    boss_attack_count +=1
    
    if boss_health > 8:
        boss_bullets.append({
            "x":x +35,
            "y": y + 40,
            "dx": -0.6,
            "dy": boss_bullet_speed
            })
        boss_bullets.append({
            "x":x + 85,
            "y": y + 40,
            "dx": 0.6,
            "dy": boss_bullet_speed
            })

    elif boss_health > 4:
        boss_bullets.append({
            "x":x + 20,
            "y": y + 60,
            "dx": -0.6,
            "dy": boss_bullet_speed
            })
        boss_bullets.append({
            "x":x + 60,
            "y": y + 60,
            "dx": 0,
            "dy": boss_bullet_speed
            })
        boss_bullets.append({
            "x":x +100,
            "y": y + 60,
            "dx": 0.6,
            "dy": boss_bullet_speed
            })

    else:
        boss_bullets.append({
            "x":x +10,
            "y": y + 80,
            "dx": -1.0,
            "dy": boss_bullet_speed
            })
        boss_bullets.append({
               "x":x + 85,
            "y": y + 80,
            "dx": -0.4,
            "dy": boss_bullet_speed
            })
        boss_bullets.append({
            "x":x +35,
            "y": y + 80,
            "dx": 0.4,
            "dy": boss_bullet_speed
            })
        boss_bullets.append({
            "x":x + 85,
            "y": y + 80,
            "dx": 1.0,
            "dy": boss_bullet_speed
            })

def Boss_phases():
    if boss_level:
        if boss_health > 8:
            phase_img = font.render("Boss Phase 1", True, "White")
        elif boss_health >4:
            phase_img = font.render("Boss Phase 2", True, "Yellow")
        else:
            phase_img = font.render("Boss Phase 3", True, "Red")

        screen.blit(phase_img, (300,70))
    
def Explosion_occur(x,y):
    explosion.append({"x":x,
                      "y":y,
                      "last_update": pygame.time.get_ticks()})

def Low_health_warning():
    if player_health == 1 and not game_over:
        warning_img = font.render("LOW HEALTH!", True, "Red")
        screen.blit(warning_img, (300,100))
        
def Gameover():
    go_img = font.render("GAME OVER", True, "White")
    screen.blit(go_img,(300,220))

    reset_rect.center = (400,360)
    screen.blit(reset_img, reset_rect)

def Victory():
    win_img = font_gameover.render("YOU WIN", True, "Yellow")
    info_img = font.render("Boss Defeated", True,"White")

    screen.blit(win_img, (260,200))
    screen.blit(info_img, (290,280))

    reset_rect.center = (400,420)
    screen.blit(reset_img, reset_rect)
    
def Restart():
    global start_page, game_started
    global spaceshipX, spaceshipY, speedX
    global bulletX, bulletY, check
    global score_value, game_over, game_over_sound, game_won
    global enemyX,enemyY,enmyspeedX, enmyspeedY
    global enemy_bullet, last_enmy_shot
    global player_health
    global boss_intro, boss_intro_show
    global boss_level, boss_spawned, bossX, bossY, boss_speedX, boss_health, boss_phase
    global boss_bullets, last_boss_shot, boss_attack_count
    global explosion
    
    
    spaceshipX = 370
    spaceshipY = 480
    speedX = 0
    bulletX = 386
    bulletY = 490
    score_value = 0
    player_health = 4
    last_enmy_shot = 0
    start_page = True
    game_started = False
    check = False
    game_over = False
    game_over_sound = False
    game_won = False

    boss_intro = False
    boss_intro_show = False
    boss_level = False
    boss_spawned = False
    bossX = 350
    bossY = 50
    boss_speedX = 0.4
    boss_health = 10
    last_boss_shot = 0
    boss_attack_count = 0
    boss_phase = 1    

    explosion.clear()
    enemyX.clear()
    enemyY.clear()
    enmyspeedX.clear()
    enmyspeedY.clear()
    enemy_bullet.clear()
    boss_bullets.clear()
    
    for enmy in range(no_of_enemies):
        enemyX.append(random.randint(0,736))
        enemyY.append(random.randint(30,200))
        enmyspeedX.append(base_enemyX)
        enmyspeedY.append(base_enemyY)

    mixer.music.load("backgroundmusic.mp3")
    mixer.music.play(-1)
    
while working:
    
    if start_page or game_over or game_won:
        screen.blit(intro_page_img, (0,0))
    elif boss_intro or boss_level:
        screen.blit(boss_background_img, (0,0))
    else:
        screen.blit(background_img, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (game_over or game_won) and reset_rect.collidepoint(event.pos):
                Restart()
                
        if event.type == pygame.QUIT:
            working = False

        if event.type ==pygame.KEYDOWN:
            if start_page:
                start_page = False
                game_started = True

            elif boss_intro:
                if event.key == pygame.K_RETURN:
                    boss_intro = False
                    boss_level = True
                    boss_spawned = True
                    player_health = max_health

            else:
                if event.key == pygame.K_LEFT:
                    speedX =-1
                if event.key == pygame.K_RIGHT:
                    speedX = 1
                if event.key == pygame.K_SPACE:
                    if check is False:
                        laser_sound.play()
                        check=True
                        bulletX = spaceshipX+16
                
        if event.type == pygame.KEYUP:
            speedX = 0

    if not game_over and not game_won:

        if start_page:
            Intro_screen()
            pygame.display.update()
            continue

        if boss_intro:
            Boss_intro_screen()
            pygame.display.update()
            continue
        
        current_time = pygame.time.get_ticks()
        
        spaceshipX += speedX
        if spaceshipX <= 0:
            spaceshipX = 0
        elif spaceshipX >=736:
            spaceshipX = 736
            
        if score_value >= boss_trig_score and not boss_spawned and not boss_intro_show:
            boss_intro = True
            boss_intro_show = True
            
        if not boss_level:
            for i in range(no_of_enemies):
                if enemyY[i]>420:
                    player_health -=1

                    Explosion_occur(spaceshipX, spaceshipY)

                    enemyX[i] = random.randint(0,736)
                    enemyY[i] = random.randint(30,200)

                    if player_health <= 0:
                        game_over = True
                    continue

                if score_value <5:
                    diff_enmyspeedX = 0.3
                    diff_enmyspeedY = 10
                elif score_value <10:
                    diff_enmyspeedX = 0.5
                    diff_enmyspeedY = 20
                elif score_value < 15:
                    diff_enmyspeedX = 0.7
                    diff_enmyspeedY = 30
                else:
                    diff_enmyspeedX = 0.9
                    diff_enmyspeedY = 40

                if enmyspeedX[i] > 0:
                    enmyspeedX[i] = diff_enmyspeedX
                else:
                    enmyspeedX[i] = -diff_enmyspeedX

                enmyspeedY[i] = diff_enmyspeedY

                enemyX[i]+=enmyspeedX[i]
            
                if enemyX[i] <=0:
                    enemyX[i] = 0
                    enmyspeedX[i] = diff_enmyspeedX
                    enemyY[i] +=enmyspeedY[i]
            
                if enemyX[i] >=736:
                    enemyX[i] = 736
                    enmyspeedX[i] = -diff_enmyspeedX
                    enemyY[i] +=enmyspeedY[i]

                distance = math.sqrt((math.pow(bulletX - enemyX[i],2)) + (math.pow(bulletY - enemyY[i],2)))

                if distance <30 and check:
                    explosion_sound.play()

                    Explosion_occur(enemyX[i], enemyY[i])
                    
                    bulletY = 480
                    check = False
                    enemyX[i] = random.randint(0,736)
                    enemyY[i] = random.randint(30,200)
                    score_value +=1

                screen.blit(enemy_img[i], (enemyX[i],enemyY[i]))
                
        if not boss_level and current_time - last_enmy_shot > enemy_shot_delay:
            shooter = random.randint(0, no_of_enemies -1)
            Enemy_shoot(enemyX[shooter], enemyY[shooter])
            last_enmy_shot = current_time

        for b in enemy_bullet[:]:
            b["y"] += enmy_bullet_speed
            screen.blit(enmy_bullet_img,(b["x"], b["y"]))

            dist_to_player = math.sqrt((math.pow(b["x"] - spaceshipX, 2)) + (math.pow(b["y"] - spaceshipY, 2)))

            if dist_to_player < 30:
                explosion_sound.play()

                Explosion_occur(spaceshipX, spaceshipY)
                enemy_bullet.remove(b)
                player_health -=1

                if player_health <= 0:
                    game_over = True

            elif b["y"] > 600:
                enemy_bullet.remove(b)
            
        if boss_level:
            if boss_health > 6:
                boss_speedX = 0.3 if boss_speedX > 0 else -0.3
            elif boss_health > 4:
                boss_speedX = 0.4 if boss_speedX > 0 else -0.4
            else:
                boss_speedX = 0.6 if boss_speedX > 0 else -0.6

            bossX += boss_speedX

            if bossX <=0 or bossX >=680:
                boss_speedX *= -1

            screen.blit(boss_img, (bossX, bossY))

            if boss_health <=7:
                boss_shot_delay = 500
            else:
                boss_shot_delay = 800

            if current_time - last_boss_shot > boss_shot_delay:
                Boss_shoot(bossX, bossY)
                last_boss_shot = current_time

            boss_distance = math.sqrt((math.pow(bulletX - (bossX + 60), 2)) + (math.pow(bulletY - (bossY + 60), 2)))

            if boss_distance < 70 and check:
                explosion_sound.play()

                Explosion_occur(bossX + 40, bossY + 40)

                boss_health -= 1
                bulletY = 450
                check = False

            if boss_health <= 0:
                boss_level = False
                boss_spawned = False
                boss_bullets.clear()
                score_value += 5
                game_won = True

        for b in boss_bullets[:]:
            b["x"] += b["dx"]
            b["y"] += b["dy"]

            screen.blit(boss_bullet_img, (b["x"], b["y"]))

            dist_to_player = math.sqrt(
                (math.pow(b["x"] - spaceshipX, 2)) +
                (math.pow(b["y"] - spaceshipY, 2))
            )

            if dist_to_player < 30:
                explosion_sound.play()

                Explosion_occur(spaceshipX, spaceshipY)
                boss_bullets.remove(b)
                player_health -= 1

                if player_health <= 0:
                    game_over = True

            elif b["y"] > 600 or b["x"] < 0 or b["x"] > 800:
                boss_bullets.remove(b)
                
        if bulletY <=0:
            bulletY = 490
            check = False
            
        if check is True:
            screen.blit(player_bullet_img,(bulletX,bulletY))
            bulletY -=2

    if game_over:
        if not game_over_sound:
            mixer.music.stop()
            gameover_sound.play()
            game_over_sound = True

        Gameover()

    if game_won:
        Victory()

    for e in explosion[:]:
        current_time = pygame.time.get_ticks()

        if current_time - e["last_update"] < 200:
            screen.blit(explosion_img, (e["x"]-20, e["y"]-20))
        else:
            explosion.remove(e)
            
    
    screen.blit(player_img, (spaceshipX,spaceshipY))
    Show_score()
    Show_health()
    Show_boss_health()
    Boss_phases()
    Low_health_warning()
    pygame.display.update()

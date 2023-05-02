import pygame as py
import os
py.font.init()
py.mixer.init()

WIDTH, HEIGHT = 800, 900
WINDOW = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption('SPACESHIP WARS')

GOLD = (255, 215, 0) 
CYAN = (0, 255, 255)
PALE_LAVENDER =  (230, 230, 250) 
BEIGE = (245, 245, 220) 
WHITE = (255, 255, 255)

BORDER = py.Rect(0, HEIGHT//2 - 5, WIDTH, 10)

BULLET_HIT_SOUND = py.mixer.Sound(os.path.join('Assets', 'launch.mp3'))
BULLET_LAUNCH_SOUND = py.mixer.Sound(os.path.join('Assets', 'Impact.mp3'))

HEALTH_FONT = py.font.SysFont('comic sans ms', 20)
WINNER_FONT = py.font.SysFont('comic sans ms', 70)
INFO_FONT = py.font.SysFont('comic sans ms', 15)
PLAYER_FONT = py.font.SysFont('comic sans ms', 10)

# how many frames per sec
FPS = 60
# speed of how fast you move
VELOCITY = 8
# bullet speed
BULLET_VEL = 20
MAX_BULLETS = 10
SPACESHIPS_WIDTH, SPACESHIPS_HEIGHT = 100, 220

P1_HIT = py.USEREVENT + 4
P2_HIT = py.USEREVENT + 4

PLAYER_1_IMAGE = py.image.load(os.path.join('Assets', 'spaceship1.png'))
PLAYER_1 = py.transform.scale(PLAYER_1_IMAGE, (SPACESHIPS_WIDTH, SPACESHIPS_HEIGHT))
PLAYER_2_IMAGE = py.image.load(os.path.join('Assets', 'spaceship2.png'))
PLAYER_2 = py.transform.rotate(py.transform.scale(PLAYER_2_IMAGE, (SPACESHIPS_WIDTH, SPACESHIPS_HEIGHT)), 180)

SNOW_BULLET_IMAGE = py.image.load(os.path.join('Assets', 'snowflake.png'))
SNOW_BULLET = py.transform.scale(SNOW_BULLET_IMAGE, (27, 32))
FIRE_BULLET_IMAGE = py.image.load(os.path.join('Assets', 'fireball.png'))
FIRE_BULLET = py.transform.rotate(py.transform.scale(FIRE_BULLET_IMAGE, (27, 32)), -35)



BACKGROUND = py.transform.scale(py.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

#call function in main function in order the designs refresh everytime
def draw_window(p1, p2, p1_bullets, p2_bullets, p1_health, p2_health):
    WINDOW.blit(BACKGROUND, (0, 0))
    py.draw.rect(WINDOW, CYAN, BORDER)

    p1_health_text = HEALTH_FONT.render('HEARTS: ' + str(p1_health), 1, GOLD)
    p2_health_text = HEALTH_FONT.render('HEARTS: ' + str(p2_health), 1, WHITE)
    WINDOW.blit(p1_health_text, (5, 5))
    WINDOW.blit(p2_health_text, (600, 855))

   #WILL SHOW IN GAME AND TELLS USER HOW TO MOVE UP AND DOWN LEFT OR RIGHT
    wasdkeys_text = INFO_FONT.render('MOVE ~ ALLEN', 1, GOLD)
    arrowkeys_text = INFO_FONT.render('MOVE ~ ARROW KEYS', 1, GOLD)
    wasd_launch = INFO_FONT.render('FIRE ~ R', 1, WHITE)
    arrow_keys_launch = INFO_FONT.render('SNOWBALL ~ L', 1, WHITE)
    WINDOW.blit(wasdkeys_text, (WIDTH-wasdkeys_text.get_width()-5, 5))
    WINDOW.blit(arrowkeys_text, (5, HEIGHT-arrowkeys_text.get_height()-5))
    WINDOW.blit(wasd_launch, (WIDTH-wasdkeys_text.get_width()-5, wasdkeys_text.get_height()+10))
    WINDOW.blit(arrow_keys_launch, (5, HEIGHT-arrowkeys_text.get_height()-arrow_keys_launch.get_height()-10))

    #displays players 
    p1_name = PLAYER_FONT.render('PLAYER 1', 1, GOLD)
    p2_name = PLAYER_FONT.render('PLAYER 2', 1, WHITE)
    WINDOW.blit(p1_name, (p1.x + PLAYER_1.get_width()//2 - p1_name.get_width()//2, p1.y - p1_name.get_height() + 20))
    WINDOW.blit(p2_name, (p2.x + PLAYER_2.get_width()//2 - p2_name.get_width()//2, p2.y + PLAYER_2.get_height() - 20))

    WINDOW.blit(PLAYER_1, (p1.x, p1.y))
    WINDOW.blit(PLAYER_2, (p2.x, p2.y))

    for bullet in p2_bullets:
        WINDOW.blit(SNOW_BULLET, bullet)
    
    for bullet in p1_bullets:
        WINDOW.blit(FIRE_BULLET, bullet)

    py.display.update()

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, GOLD)
    text_rect = draw_text.get_rect(center=(WIDTH/2, HEIGHT/2))
    WINDOW.blit(draw_text, text_rect)
    py.display.update()
    py.time.delay(3000) # GAME WILL RESET BY ITSLEF OR USER CAN LEAVE BY ITSELF


#spaceship1 movements
def spaceship1_movement(keys_pressed, p1):
    if keys_pressed[py.K_a]:
        p1.x = max(p1.x - VELOCITY, -20)  # Move left
    if keys_pressed[py.K_d]:
        p1.x = min(p1.x + VELOCITY, WIDTH - SPACESHIPS_WIDTH + 20)  # Move right
    if keys_pressed[py.K_w]:
        p1.y = max(p1.y - VELOCITY, -30)  # Move up
    if keys_pressed[py.K_s]:
        p1.y = min(p1.y + VELOCITY, HEIGHT/2 - SPACESHIPS_HEIGHT + 15)  # Move down
#spaceship2 movements
def spaceship2_movement(keys_pressed, p2):
    if keys_pressed[py.K_LEFT]:
        p2.x = max(p2.x - VELOCITY, -20)  # move left
    if keys_pressed[py.K_RIGHT]:
        p2.x = min(p2.x + VELOCITY, WIDTH - SPACESHIPS_WIDTH + 20)  # move right
    if keys_pressed[py.K_UP]:
        p2.y = max(p2.y - VELOCITY, HEIGHT/2 - 15)  # move up
    if keys_pressed[py.K_DOWN]:
        p2.y = min(p2.y + VELOCITY, HEIGHT - SPACESHIPS_HEIGHT + 30)  # move down

def handle_bullets(p1_bullets, p2_bullets, p1, p2):
    # check if spaceship 2 gets hit by shot
    for bullet in p1_bullets:
        bullet.y += BULLET_VEL
        if p2.colliderect(py.Rect(bullet.x, bullet.y - 25, bullet.width, bullet.height - 5)):
            py.event.post(py.event.Event(P2_HIT))
            p1_bullets.remove(bullet)
        elif bullet.y > WIDTH + 100:
            p1_bullets.remove(bullet)
    #checks if spaceship 1 gets hit by shot
    for bullet in p2_bullets:
        bullet.y -= BULLET_VEL
        if p1.colliderect(py.Rect(bullet.x, bullet.y + 35, bullet.width, bullet.height - 5)):
            py.event.post(py.event.Event(P1_HIT))
            p2_bullets.remove(bullet)
        elif bullet.y < 0:
            p2_bullets.remove(bullet)
             

def main():
    p2 = py.Rect(550, 700, SPACESHIPS_WIDTH, SPACESHIPS_HEIGHT)
    p1 = py.Rect(150, 100, SPACESHIPS_WIDTH, SPACESHIPS_HEIGHT)
    
    p1_bullets = []
    p2_bullets = []

    p1_health = 20
    p2_health = 20

    clock = py.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()

            if event.type == py.KEYDOWN:
                if event.key == py.K_r and len(p1_bullets) < MAX_BULLETS:
                    #shooting for spaceship 1
                    bullet = py.Rect(p1.x + SPACESHIPS_WIDTH//2 - 12, p1.y + SPACESHIPS_HEIGHT, 7, 15)
                    p1_bullets.append(bullet)
                    BULLET_LAUNCH_SOUND.play()
                if event.key == py.K_l and len(p2_bullets) < MAX_BULLETS:
                   #shooting for spaceship2
                    bullet = py.Rect(p2.x + SPACESHIPS_WIDTH//2 - 12, p2.y, 7, 15)
                    p2_bullets.append(bullet)
                    BULLET_LAUNCH_SOUND.play()

            if event.type == P1_HIT:
                p1_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == P2_HIT:
                p2_health -= 1
                BULLET_HIT_SOUND.play()

        if p1_health == 0:
            winning_message = 'PLAYER 2 HAS WON!'
            draw_winner(winning_message)
            break
            

        if p2_health == 0:
            winning_message = 'PLAYER 1 HAS WON!'
            draw_winner(winning_message)
            break
    
        keys_pressed = py.key.get_pressed()
        spaceship1_movement(keys_pressed, p1)
        spaceship2_movement(keys_pressed, p2)

        handle_bullets(p1_bullets, p2_bullets, p1, p2)

        draw_window(p1, p2, p1_bullets, p2_bullets, p1_health, p2_health)
    
    main()

if __name__ == "__main__":
    main()









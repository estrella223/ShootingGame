import pygame
import random
import os
import sys
import time

# 게임창 위치설정
padX = 600
padY = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (padX, padY)

# image_dir = os.path.join(os.path.dirname(__file__), 'img')
# sound_dir = os.path.join(os.path.dirname(__file__), 'sfx')
# print(image_dir)

# 전역
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
FPS = 60

score = 0
playtime = 1

# 색상
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN1 = 25, 102, 25
GREEN2 = 51, 204, 51
GREEN3 = 233, 249, 185
BLUE = 17, 17, 212
BLUE2 = 0, 0, 147
YELLOW = 255, 255, 197
LIGHT_PINK1 = 250, 235, 255
LIGHT_PINK2 = 255, 204, 255
LAVENDER = 250, 235, 255

def initialize_game(width, height):    #초기화
    pygame.init()
    surface = pygame.display.set_mode((width, height))    #set_mode 통해 surface 반환
    pygame.display.set_caption("Duty-free Game")
    return surface

def game_loop(surface):    #루프 안에서 게임이 돌아감  stage 1
    #이미지 로드
    background_image = pygame.image.load(r'img\airplane1.jpg')
    player_image = pygame.image.load(r'img\luggage2.png').convert()
    bullet_image = pygame.image.load(r'img\passport.jpg')
    mob_image = pygame.image.load(r'img\perfume.png').convert()
    start_image = pygame.image.load(r'img\stage1.png').convert()
    main_image = pygame.image.load(r'img\main5.png').convert()

    shoot_sound = pygame.mixer.Sound(r'sfx\laser.mp3')
    shoot_sound.set_volume(0.3)
    explosion_sound = pygame.mixer.Sound(r'sfx\coin.mp3')
    explosion_sound.set_volume(0.3)

    pygame.mixer.music.load(r'sfx\dreams.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)

    clock = pygame.time.Clock()
    sprite_group = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = PlayerShip(player_image)
    global player_health
    player_health = 100
    global score
    score = 0
    sprite_group.add(player)

    for i in range(6):
        enemy = Mob(mob_image)
        sprite_group.add(enemy)
        mobs.add(enemy)

    running = 0
    while running == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    close_game()
                if event.key == pygame.K_RETURN:
                    running = 1
            surface.blit(main_image, (0, 0))  # 배경은 항상 가장 위에 그려야함

        pygame.display.flip()

        while running == 1:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    close_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        close_game()
                    if event.key == pygame.K_BACKSPACE:
                        running = 0
                    if event.key == pygame.K_RETURN:
                        running = 2
                surface.blit(start_image, (0, 0))
            pygame.display.flip()

    running = 2
    while running == 2:
        for event in pygame.event.get():    #키보드, 마우스 설정
            if event.type == pygame.QUIT:
                running = 3
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:    #esc키
                    running = 3
                if event.key == pygame.K_SPACE:
                    player.shoot(sprite_group, bullets, bullet_image, shoot_sound)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    player.shoot(sprite_group, bullets, bullet_image , shoot_sound)

        sprite_group.update()

        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)    #spritecooide는 적과 충돌 감지. 그룹간 비교도 가능
        for hit in hits:
            explosion_sound.play()
            mob = Mob(mob_image)
            sprite_group.add(mob)
            mobs.add(mob)
            score += 1
            if score >= 60:
                clear_stage1(surface)
                game_loop1(surface)

        hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
        if hits:
            player_health -= 5
            if player_health < 0:
                gameover(surface)
                restart()

        background_image = pygame.transform.scale(background_image, (500, 800))
        surface.blit(background_image, (0, 0))
        sprite_group.draw(surface)
        score_update(surface)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    print('game played: ', playtime)

def game_loop1(surface):    #stage 2

    #이미지 로드
    background_image = pygame.image.load(r'img\airplane1.jpg')
    player_image = pygame.image.load(r'img\luggage2.png').convert()
    bullet_image = pygame.image.load(r'img\passport.jpg')
    mob_image = pygame.image.load(r'img\cigarette.png').convert()
    stage2_image = pygame.image.load(r'img\stage2.png').convert()
    shoot_sound = pygame.mixer.Sound(r'sfx\laser.mp3 ')
    shoot_sound.set_volume(0.1)
    explosion_sound = pygame.mixer.Sound(r'sfx\coin.mp3')
    explosion_sound.set_volume(0.7)

    pygame.mixer.music.load(r'sfx\dreams.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)

    clock = pygame.time.Clock()
    sprite_group = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = PlayerShip(player_image)
    global player_health
    player_health = 100
    global score
    score = 0
    sprite_group.add(player)
    for i in range(10):    # 2스테이지라 적의 양을 늘림
        enemy = Mob(mob_image)
        sprite_group.add(enemy)
        mobs.add(enemy)

    running = 0
    while running == 0:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    close_game()
                if event.key == pygame.K_BACKSPACE:
                    restart()
                if event.key == pygame.K_RETURN:
                    running = 2
            surface.blit(stage2_image, (0, 0))
        pygame.display.flip()

    running = 2
    while running == 2:
        for event in pygame.event.get():  # 키보드, 마우스 설정
            if event.type == pygame.QUIT:
                running = 3
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # esc키
                    running = 3
                if event.key == pygame.K_SPACE:
                    player.shoot(sprite_group, bullets, bullet_image, shoot_sound)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    player.shoot(sprite_group, bullets, bullet_image, shoot_sound)

        sprite_group.update()

        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            explosion_sound.play()
            mob = Mob(mob_image)
            sprite_group.add(mob)
            mobs.add(mob)
            score += 1
            if score >= 200:
                clear_stage1(surface)
                game_loop2(surface)
            elif score < 0:
                gameover(surface)
                restart()

        hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
        if hits:
            mob = Mob(mob_image)
            sprite_group.remove(mob)
            mobs.remove(mob)
            player_health -= 5
            if player_health < 0:
                gameover(surface)
                restart()

        background_image = pygame.transform.scale(background_image, (500, 800))
        surface.blit(background_image, (0, 0))
        sprite_group.draw(surface)
        score_update(surface)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    print('game played: ', playtime)

def game_loop2(surface):    #stage 3

    #이미지 로드
    background_image = pygame.image.load(r'img\airplane1.jpg')
    player_image = pygame.image.load(r'img\luggage2.png').convert()
    bullet_image = pygame.image.load(r'img\passport.jpg')
    mob_image = pygame.image.load(r'img\whiskey.png').convert()
    stage3_image = pygame.image.load(r'img\stage3.png').convert()
    shoot_sound = pygame.mixer.Sound(r'sfx\laser.mp3 ')
    shoot_sound.set_volume(0.1)
    explosion_sound = pygame.mixer.Sound(r'sfx\coin.mp3')
    explosion_sound.set_volume(0.7)

    pygame.mixer.music.load(r'sfx\dreams.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(loops=-1)

    clock = pygame.time.Clock()
    sprite_group = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = PlayerShip(player_image)
    global player_health
    player_health = 100
    global score
    score = 0
    sprite_group.add(player)
    for i in range(15):
        enemy = Mob(mob_image)
        sprite_group.add(enemy)
        mobs.add(enemy)

    running = 0
    while running == 0:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    close_game()
                if event.key == pygame.K_BACKSPACE:
                    restart()
                if event.key == pygame.K_RETURN:
                    running = 1
            surface.blit(stage3_image, (0, 0))
        pygame.display.flip()

    running = 1
    while running == 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 2
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = 2
                if event.key == pygame.K_SPACE:
                    player.shoot(sprite_group, bullets, bullet_image, shoot_sound)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    player.shoot(sprite_group, bullets, bullet_image, shoot_sound)

        sprite_group.update()

        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            explosion_sound.play()
            mob = Mob(mob_image)
            sprite_group.add(mob)
            mobs.add(mob)
            score += 1
            if score >= 1000:
                clear_stage1(surface)
                restart()
            elif score < 0:
                gameover(surface)
                restart()

        hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
        if hits:
            mob = Mob(mob_image)
            sprite_group.remove(mob)
            mobs.remove(mob)
            player_health -= 5
            if player_health < 0:
                gameover(surface)
                restart()

        background_image = pygame.transform.scale(background_image, (500, 800))
        surface.blit(background_image, (0, 0))
        sprite_group.draw(surface)
        score_update(surface)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    print('game played: ', playtime)

def score_update(surface):    #점수 카운트
    font = pygame.font.Font(r'font\comicbd.ttf', 30)
    image = font.render(f'Score : {score}            HP : {player_health}', True, BLUE2)
    pos = image.get_rect()
    pos.move_ip(30, 20)    #좌표 설정
    surface.blit(image, pos)

def clear_stage1(surface):    #클리어 했을 때
    font = pygame.font.Font(r'font\comicbd.ttf', 50)
    image = font.render('CLEAR', True, BLUE)
    pos = image.get_rect()
    pos.move_ip(175, int(SCREEN_HEIGHT / 2 - 60))
    surface.blit(image, pos)
    pygame.display.update()
    time.sleep(2)

def gameover(surface):    #게임 오버
    font = pygame.font.Font(r'font\comicbd.ttf', 50)
    image = font.render('GAME OVER', True, RED)
    pos = image.get_rect()
    pos.move_ip(90, int(SCREEN_HEIGHT/2-30))
    surface.blit(image, pos)
    pygame.display.update()
    time.sleep(1)

#def next_stage(surface):
    #screen = initialize_game(SCREEN_WIDTH, SCREEN_HEIGHT)

def close_game():
    pygame.quit()
    print('Game closed')

def restart():   #다시시작
    screen = initialize_game(SCREEN_WIDTH, SCREEN_HEIGHT)
    game_loop(screen)
    close_game()


class PlayerShip(pygame.sprite.Sprite):    #player 설정
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (100, 110))    #이미지 사이즈 변경
        self.image.set_colorkey(WHITE)    #png파일 여백부분 없애줌
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .9/2)    #충돌감지 기능 향상
        self.rect.centerx = int(SCREEN_WIDTH/2)
        self.rect.centery = SCREEN_HEIGHT -20
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -10
        if keystate[pygame.K_RIGHT]:
            self.speedx = 10
        if keystate[pygame.K_UP]:
            self.speedy = -10
        if keystate[pygame.K_DOWN]:
            self.speedy = 10

        self.rect.x += self.speedx    #화면 나가지 않게 설정
        self.rect.y += self.speedy
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self, all_sprites, bullets, image, sound):    #미사일 슈팅
        bullet = Bullet(self.rect.centerx, self.rect.top, image)
        all_sprites.add(bullet)
        bullets.add(bullet)
        sound.play()

class Mob(pygame.sprite.Sprite):    #떨어지는 물체 설정
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (60, 60))  # 이미지 사이즈 변경
        self.image.set_colorkey(WHITE)  # png파일 여백부분 없애줌
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .9 / 2)
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.direction_change = False
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.top > SCREEN_HEIGHT + 10 or self.rect.left < -25 or self.rect.right > SCREEN_WIDTH + 20:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 8)


class Bullet(pygame.sprite.Sprite):    #미사일 설정
    def __init__(self, playerX, playerY, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(image, (30, 30))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = playerY
        self.rect.centerx = playerX
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

#sprite group 생성
playership_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
mob_group = pygame.sprite.Group()

#게임 실행
if __name__ == '__main__':
        screen = initialize_game(SCREEN_WIDTH, SCREEN_HEIGHT)
        game_loop(screen)
        sys.exit()    #시스템에 모든 자원을 반환하고 프로그램 종료. 이후에 코드 사용할 수 없으니 주의
import pygame
import sys
from pygame.transform import scale
from pygame.image import load
pygame.init()

BACKGROUND = 1200, 600
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
FPS = 20
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
ADD_NEW_FLAME_RATE = 18
cactus_img = pygame.image.load('queMario/images/cactus_bricks_down.png')
cactus_img_rect = cactus_img.get_rect()
cactus_img_rect.left = 0
fire_img = pygame.image.load('queMario/images/cactus_bricks_up.png')
fire_img_rect = fire_img.get_rect()
fire_img_rect.left = 0
CLOCK = pygame.time.Clock()
font = pygame.font.SysFont('forte', 20)
global flame_scale
flame_scale = 20
global flames_velocity
flames_velocity = 20
mario_up = pygame.image.load('queMario/images/mario/mario_1.png')
mario_up_image = pygame.transform.scale(mario_up, (50, 50))
mario_down = pygame.image.load('queMario/images/mario/mario_2.png')
mario_down_image = pygame.transform.scale(mario_down, (50, 50))

canvas = pygame.display.set_mode(BACKGROUND)
pygame.display.set_caption('Mario Survivor')

fundo = scale(load('queMario/images/background.jpg'), BACKGROUND)


class Topscore:
    def __init__(self):
        self.high_score = 0
    def top_score(self, score):
        if score > self.high_score:
            self.high_score = score
        return self.high_score

topscore = Topscore()


class Dragon:
    dragon_velocity = 10

    def __init__(self):
        self.dragon_img = pygame.image.load('queMario/images/dragon.png')
        self.dragon_img_rect = self.dragon_img.get_rect()
        self.dragon_img_rect.width -= 10
        self.dragon_img_rect.height -= 10
        self.dragon_img_rect.top = WINDOW_HEIGHT/2
        self.dragon_img_rect.right = WINDOW_WIDTH
        self.up = True
        self.down = False

    def update(self):
        canvas.blit(self.dragon_img, self.dragon_img_rect)
        if self.dragon_img_rect.top <= cactus_img_rect.bottom:
            self.up = False
            self.down = True
        elif self.dragon_img_rect.bottom >= fire_img_rect.top:
            self.up = True
            self.down = False

        if self.up:
            self.dragon_img_rect.top -= self.dragon_velocity
        elif self.down:
            self.dragon_img_rect.top += self.dragon_velocity


class Flames:

    def __init__(self):
        self.flames = pygame.image.load('queMario/images/fireball.png')
        self.flames_img = pygame.transform.scale(self.flames, (flame_scale, flame_scale))
        self.flames_img_rect = self.flames_img.get_rect()
        self.flames_img_rect.right = dragon.dragon_img_rect.left
        self.flames_img_rect.top = dragon.dragon_img_rect.top + 30


    def update(self):
        canvas.blit(self.flames_img, self.flames_img_rect)

        if self.flames_img_rect.left > 0:
            self.flames_img_rect.left -= flames_velocity


class Mario(pygame.sprite.Sprite):
    velocity = 10

    def __init__(self):
        self.mario_img = scale(load('queMario/images/mario/mario_1.png'), (50, 50))
        self.mario_img_rect = self.mario_img.get_rect()
        self.mario_img_rect.left = 20
        self.mario_img_rect.top = WINDOW_HEIGHT/2 - 100
        self.down = True
        self.up = False

    def update(self):
        canvas.blit(self.mario_img, self.mario_img_rect)
        if self.mario_img_rect.top <= cactus_img_rect.bottom:
            game_over()
            if SCORE > self.mario_score:
                self.mario_score = SCORE
        if self.mario_img_rect.bottom >= fire_img_rect.top:
            game_over()
            if SCORE > self.mario_score:
                self.mario_score = SCORE
        if self.up:
            self.mario_img_rect.top -= 10
        if self.down:
            self.mario_img_rect.bottom += 10


def game_over():
    pygame.mixer.music.stop()
    music = pygame.mixer.Sound('queMario/media/mario_dies.wav')
    music.play()
    topscore.top_score(SCORE)
    game_over_img = pygame.image.load('queMario/images/end.png')
    game_over_img_rect = game_over_img.get_rect()
    game_over_img_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    canvas.blit(game_over_img, game_over_img_rect)
    global flame_scale
    flame_scale = 20
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                music.stop()
                game_loop()
        pygame.display.update()


def start_game():
    canvas.fill(BLACK)
    canvas.blit(fundo, (0, 0))
    start_img = pygame.image.load('queMario/images/start.png')
    start_img_rect = start_img.get_rect()
    start_img_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    canvas.blit(start_img, start_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                game_loop()
        pygame.display.update()

def check_level(SCORE):
    global LEVEL
    if SCORE in range(0, 10):
        cactus_img_rect.bottom = 50
        fire_img_rect.top = WINDOW_HEIGHT - 50
        LEVEL = 1
    elif SCORE in range(10, 20):
        cactus_img_rect.bottom = 100
        fire_img_rect.top = WINDOW_HEIGHT - 100
        LEVEL = 2
    elif SCORE in range(20, 30):
        global flame_scale
        flame_scale = 80
        LEVEL = 3
    elif SCORE > 30:
        global flames_velocity
        flames_velocity = 40
        LEVEL = 4

def game_loop():

    while True:
        global dragon
        dragon = Dragon()
        flames = Flames()
        mario = Mario()
        add_new_flame_counter = 0
        global SCORE
        SCORE = 0
        global  HIGH_SCORE
        flames_list = []
        pygame.mixer.music.load('queMario/media/mario_theme.wav')
        pygame.mixer.music.play(-1, 0.0)
        while True:
            canvas.blit(fundo, (0, 0))
            check_level(SCORE)
            dragon.update()
            add_new_flame_counter += 1

            if add_new_flame_counter == ADD_NEW_FLAME_RATE:
                add_new_flame_counter = 0
                new_flame = Flames()
                flames_list.append(new_flame)
            for f in flames_list:
                if f.flames_img_rect.left <= 0:
                    flames_list.remove(f)
                    SCORE += 1
                f.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        mario.up = True
                        mario.down = False
                        mario.mario_img = mario_up_image
                    elif event.key == pygame.K_DOWN:
                        mario.down = True
                        mario.up = False
                        mario.mario_img = mario_down_image
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        mario.up = False
                        mario.down = True
                        mario.mario_img = mario_down_image
                    elif event.key == pygame.K_DOWN:
                        mario.down = True
                        mario.up = False
                        mario.mario_img = mario_down_image

            score_font = font.render('Score:'+str(SCORE), True, GREEN)
            score_font_rect = score_font.get_rect()
            score_font_rect.center = (200, cactus_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(score_font, score_font_rect)

            level_font = font.render('Level:'+str(LEVEL), True, GREEN)
            level_font_rect = level_font.get_rect()
            level_font_rect.center = (500, cactus_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(level_font, level_font_rect)

            top_score_font = font.render('Top Score:'+str(topscore.high_score),True,GREEN)
            top_score_font_rect = top_score_font.get_rect()
            top_score_font_rect.center = (800, cactus_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(top_score_font, top_score_font_rect)

            canvas.blit(cactus_img, cactus_img_rect)
            canvas.blit(fire_img, fire_img_rect)
            mario.update()
            for f in flames_list:
                if f.flames_img_rect.colliderect(mario.mario_img_rect):
                    game_over()
                    if SCORE > mario.mario_score:
                        mario.mario_score = SCORE
            pygame.display.update()
            CLOCK.tick(FPS)


start_game()
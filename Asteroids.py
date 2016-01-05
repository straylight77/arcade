import pygame, sys, math, random, os
from pygame.locals import *

FPS = 30
MAX_X = 800
MAX_Y = 600

WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
GRAY      = (128, 128, 128)
DARKGRAY  = ( 40,  40,  40)
RED       = (255,  40,  40)
BGCOLOR   = BLACK


#### Class: Asteroid ########################################################
class Asteroid(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        side = random.randint(1, 4)
        if side == 1:    self.pos = (random.randint(0, MAX_X), 0)
        elif side == 2:  self.pos = (0, random.randint(0, MAX_Y))
        elif side == 3:  self.pos = (random.randint(0, MAX_X), MAX_Y)
        elif side == 4:  self.pos = (MAX_X, random.randint(0, MAX_Y))

        s = random.randint(3, 6)
        self.vel = (random.randint(-s, s), random.randint(-s, s))

        #load asteroid sprite
        self.ast_spritesheet = pygame.image.load('assets/asteroid2.png').convert_alpha()
        self.ast_img = []
        s = 64
        for y in range(0,6):
            for x in range (0, 5):
                self.ast_img.append(self.ast_spritesheet.subsurface( (x*s,y*s,s,s) ))

        self.frame = 0
        self.image = self.ast_img[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self):
        x = self.pos[0] + self.vel[0]
        y = self.pos[1] + self.vel[1]
        if x >= MAX_X:  x = 0
        if x < 0:       x = MAX_X
        if y >= MAX_Y:  y = 0
        if y < 0:       y = MAX_Y
        self.pos = (x, y)

        self.rect.center = self.pos
        self.image = self.ast_img[self.frame]
        self.frame += 1
        if self.frame >= len(self.ast_img):
            self.frame = 0



#### Class: Explosion ############################################
class Explosion(pygame.sprite.Sprite):

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, 64, 64)
        self.rect.center = pos
        self.frame = 0

        #load explosion sprite
        self.exp_spritesheet = pygame.image.load('assets/explosion1_64x64.png').convert_alpha()
        self.exp_img = []
        s = 64
        for y in range(0, 5):
            for x in range (0, 5):
                self.exp_img.append(self.exp_spritesheet.subsurface( (x*s,y*s,s,s) ))
        self.image = self.exp_img[self.frame]


    def update(self):
        if self.frame < len(self.exp_img):
            self.image = self.exp_img[self.frame]
            self.frame += 1


    def is_done(self):
        return self.frame >= len(self.exp_img)


#### class: Ship #################################################
class Ship(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.reset()
        self.image_orig = pygame.image.load('assets/ship1_32x32.png').convert_alpha()
        self.rect = self.image_orig.get_rect()

        self.rect.center = self.pos
        self.image = self.image_orig

    def reset(self):
        self.pos = (MAX_X/2, MAX_Y/2)
        self.angle = 90
        self.vel = (0, 0)
 

    def update(self, thrust, left, right):
        if left:
            self.angle += 10
        if right:
            self.angle -= 10
        if thrust:
            vel_x = self.vel[0] + math.cos(math.radians(self.angle))*0.5
            vel_y = self.vel[1] - math.sin(math.radians(self.angle))*0.5
            #set max?
            self.vel = (vel_x, vel_y)

        if self.angle >= 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360

        x = self.pos[0] + self.vel[0]
        y = self.pos[1] + self.vel[1]
        if x >= MAX_X:  x = 0
        if x < 0:       x = MAX_X
        if y >= MAX_Y:  y = 0
        if y < 0:       y = MAX_Y
        self.pos = (x, y)

        self.image = pygame.transform.rotate(self.image_orig, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

#### class: Shot ############################################################
class Shot(pygame.sprite.Sprite):

    def __init__(self, pos, angle, speed=40):
        pygame.sprite.Sprite.__init__(self)

        #draw sprite
        size = 8
        self.image = pygame.Surface((size, size))
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.circle(self.image, (192,  10,  10), (size/2, size/2), size/2)
        pygame.draw.circle(self.image, (192, 128, 128), (size/2, size/2), size/4)
        self.rect = self.image.get_rect()

        self.vel = (0, 0)
        self.pos = pos
        self.angle = angle
        self.time_to_live = FPS/2

        vel_x = self.vel[0] + math.cos(math.radians(self.angle))*speed
        vel_y = self.vel[1] - math.sin(math.radians(self.angle))*speed
        self.vel = (vel_x, vel_y)


    def update(self):
        x = self.pos[0] + self.vel[0]
        y = self.pos[1] + self.vel[1]
        if x >= MAX_X:  x = 0
        if x < 0:       x = MAX_X
        if y >= MAX_Y:  y = 0
        if y < 0:       y = MAX_Y
        self.pos = (x, y)

        self.rect.center = self.pos

        self.time_to_live -= 1

    def is_done(self):
        return self.time_to_live <= 0


def terminate():
    pygame.quit()
    sys.exit()



#### main ########################################
pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((MAX_X, MAX_Y))
BASICFONT = pygame.font.SysFont('courier', 15)
pygame.display.set_caption('pyGame Template')
random.seed()

a = Asteroid()
asteroids = pygame.sprite.RenderPlain(a)
explosions = pygame.sprite.RenderPlain()

ship = Ship()
ships = pygame.sprite.RenderPlain(ship)

shots = pygame.sprite.RenderPlain()

score = 0
level = 1
lives = 2
cmd_thrust = False
cmd_left = False
cmd_right = False
delay_game = 0

#main game loop
while True:

    #event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()

        elif event.type == KEYDOWN:
            if event.key == K_UP:    cmd_thrust = True
            if event.key == K_LEFT:  cmd_left = True
            if event.key == K_RIGHT: cmd_right = True
            if event.key == K_LCTRL:
                if ship.alive():
                    sh = Shot(ship.pos, ship.angle)
                    shots.add(sh)

        elif event.type == KEYUP:
            if event.key == K_UP:    cmd_thrust = False
            if event.key == K_LEFT:  cmd_left = False
            if event.key == K_RIGHT: cmd_right = False

            if event.key == K_n:
                asteroids.add( Asteroid() )
            if event.key == K_ESCAPE:
                terminate()

    #update game objects
    asteroids.update()
    explosions.update()
    shots.update()
    if ship.alive():
        ships.update(cmd_thrust, cmd_left, cmd_right)

    for exp in explosions.sprites():
        if exp.is_done():
            exp.kill()

    for sh in shots.sprites():
        if sh.is_done():
            sh.kill()

    # detect collisions
    for a in pygame.sprite.spritecollide(ship, asteroids, False):
        if ship.alive():
            explosions.add(Explosion(ship.pos))
            ship.kill()

    for a in pygame.sprite.groupcollide(asteroids, shots, True, True).keys():
        explosions.add(Explosion(a.pos))
        score += 10



    # draw frame
    DISPLAYSURF.fill(BGCOLOR)
    explosions.draw(DISPLAYSURF)
    asteroids.draw(DISPLAYSURF)
    shots.draw(DISPLAYSURF)
    ships.draw(DISPLAYSURF)

    msg = "LEVEL: %d   SCORE: %d    LIVES: %d"%(level, score, lives)
    msg_disp = BASICFONT.render(msg, True, WHITE, BLACK)
    DISPLAYSURF.blit(msg_disp, (10, 10))


    if len(asteroids) == 0 and len(explosions) == 0:
        level += 1
        ship.reset()
        for i in range (0, level):
            asteroids.add( Asteroid() )
        delay_game = FPS*2

    if len(ships) == 0 and len(explosions) == 0 and lives > 0:
        lives -= 1
        ship = Ship()
        ships.add(ship)
        delay_game = FPS*2

    if delay_game > 0:
        delay_game -= 1

    #advance frame
    #pygame.display.update()
    pygame.display.flip()
    FPSCLOCK.tick(FPS)


terminate()   # won't actually get called




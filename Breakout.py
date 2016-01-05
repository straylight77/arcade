import pygame, sys, math, random
from pygame.locals import *

FPS = 30
MAX_X = 800
MAX_Y = 600

WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
GRAY      = (128, 128, 128)
DARKGRAY  = ( 40,  40,  40)
RED       = (255,  40,  40)
BGCOLOR = BLACK



class Paddle(pygame.sprite.Sprite):

    def __init__(self, arena):
        pygame.sprite.Sprite.__init__(self)
        self.load_sprite()
        self.rect = self.image.get_rect()
        self.rect.y = arena.bottom-50
        self.rect.x = arena.centerx - self.image.get_width()/2

    def load_sprite(self):
        self.image = pygame.Surface((70, 20))
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        pygame.draw.rect(self.image, GRAY, (10, 0, 50, 20))
        pygame.draw.circle(self.image, GRAY, (10, 10), 10)
        pygame.draw.circle(self.image, GRAY, (60, 10), 10)

    def dist_from_middle(self, x):
        """returns the number of pixels from the center of the paddle along x-axis"""
        pass
        return x - self.rect.centerx

    def update(self, arena, left, right):
        if left:
            self.rect.move_ip(-10, 0)
            if not arena.contains(self.rect):
                self.rect.left = arena.left
        if right:
            self.rect.move_ip(10, 0)
            if not arena.contains(self.rect):
                self.rect.right = arena.right


class Ball(pygame.sprite.Sprite):

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.load_sprite()
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.vel_x = 6
        self.vel_y = -8
        self.caught = False
        self.dead = False

    def load_sprite(self):
        self.image = pygame.Surface((16, 16))
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        pygame.draw.circle(self.image, GRAY, (8, 8), 8)

    def bounce_vert(self):
        self.vel_x = -self.vel_x

    def bounce_horiz(self):
        self.vel_y = -self.vel_y

    def bounce_paddle(self, rect):
        self.vel_y = -self.vel_y

    def bounce_walls(self, walls):
        """Ensure ball remains contained within the given Rect (walls)"""
        if ball.rect.bottom >= arena_rect.bottom:
            #kill the ball
            self.dead = True
            self.vel_x = 0
            self_vel_y = 0
            self.kill()
            print "DEAD!"
        elif ball.rect.left <= arena_rect.left:
            self.vel_x = -self.vel_x
        elif ball.rect.right >= arena_rect.right:
            self.vel_x = -self.vel_x
        elif ball.rect.top <= arena_rect.top:
            self.vel_y = -self.vel_y

    def bounce_block(self, block):
        """Ensure balls remains outside given Rect (block) by bouncing away"""
        pass



    def set_velocity(angle, speed = -1):
        if speed <> -1:
            self.speed = speed
        rad = math.radians(angle)
        self.vel_x = self.speed * math.cos(rad)
        self.vel_y = self.speed * math.sin(rad)



    def update(self, arena):
        #if self.angle > 360:  self.angle -= 360
        #if self.angle < 0:    self.angle += 360
        #dx = self.speed * math.cos( math.radians(self.angle) )
        #dy = self.speed * math.sin( math.radians(self.angle) )
        #self.rect.move_ip(dx, dy)
        self.rect.move_ip( self.vel_x, self.vel_y )


def terminate():
    pygame.quit()
    sys.exit()

#### main ###############################################
pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((MAX_X, MAX_Y))
BASICFONT = pygame.font.SysFont('arial', 15)
pygame.display.set_caption('pyGame Template')
random.seed()

#create sprites and groups

arena_rect = pygame.Rect(20, 20, MAX_X-220, MAX_Y)
paddle = pygame.sprite.GroupSingle( Paddle(arena_rect) )
balls = pygame.sprite.RenderPlain( Ball(arena_rect.center) )

cmd_left = False
cmd_right = False

score = 0
lives = 2
level = 1

while True:

    #event handling
    for event in pygame.event.get():
        if event.type == QUIT:           terminate()

        elif event.type == KEYDOWN:
            if event.key == K_LEFT:      cmd_left = True
            elif event.key == K_RIGHT:   cmd_right = True

        elif event.type == KEYUP:
            if event.key == K_ESCAPE:    terminate()
            elif event.key == K_LEFT:    cmd_left = False
            elif event.key == K_RIGHT:   cmd_right = False


    #update game state
    paddle.update(arena_rect, cmd_left, cmd_right)
    balls.update(arena_rect)

    # detect collisions with paddle
    for ball in pygame.sprite.spritecollide(paddle.sprite, balls, 0):
        ball.bounce_paddle(paddle.sprite)


    # detect collisions with walls
    for ball in balls.sprites():
        ball.bounce_walls(arena_rect)

    if not balls:
        if lives == 0:
            gameover = True
            print "GAMEOVER!"
        else:
            lives -= 1
            balls.add( Ball(arena_rect.center) )
            print "lives: ", lives

    # draw frame
    DISPLAYSURF.fill(BGCOLOR)
    paddle.draw(DISPLAYSURF)
    balls.draw(DISPLAYSURF)

    pygame.draw.rect(DISPLAYSURF, RED, arena_rect, 1)
    #pygame.display.update()
    pygame.display.flip()
    FPSCLOCK.tick(FPS)

terminate()



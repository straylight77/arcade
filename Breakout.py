import pygame, sys, math, random
from pygame.locals import *

FPS = 60
MAX_X = 800
MAX_Y = 600

WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
GRAY      = (128, 128, 128)
DARKGRAY  = ( 40,  40,  40)
RED       = (255,  40,  40)
ORANGE    = (255, 128,  40)
BGCOLOR = BLACK


#### class: Paddle ##########################################################
class Paddle(pygame.sprite.Sprite):

    def __init__(self, arena):
        pygame.sprite.Sprite.__init__(self)
        self.load_sprite()
        self.rect = self.image.get_rect()
        self.rect.y = arena.bottom-80
        self.rect.x = arena.centerx - self.image.get_width()/2
        self.balls_held = []

    def load_sprite(self):
        self.image = pygame.Surface((70, 20))
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        pygame.draw.rect(self.image, GRAY, (10, 0, 50, 20))
        pygame.draw.circle(self.image, GRAY, (10, 10), 10)
        pygame.draw.circle(self.image, GRAY, (60, 10), 10)

    def catch_ball(self, sprite):
        self.balls_held.append(sprite)

    def throw_ball(self, sprite):
        self.balls_held.remove(sprite)

    def dist_from_middle(self, x):
        """returns the number of pixels from the center of the paddle along x-axis"""
        pass
        return x - self.rect.centerx

    def update(self, arena):
        self.rect.centerx = pygame.mouse.get_pos()[0]
        self.rect.clamp_ip(arena)

#### class: Ball ############################################################
class Ball(pygame.sprite.Sprite):

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.load_sprite()
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.set_velocity(300, 6)
        self.caught = False
        self.dead = False

    def load_sprite(self):
        self.image = pygame.Surface((16, 16))
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        pygame.draw.circle(self.image, GRAY, (8, 8), 8)

    def bounce_paddle(self, sprite):
        pct = (self.rect.centerx - sprite.rect.centerx) / (float(sprite.rect.width) / 2.0)
        angle = 270 + (50*pct)
        self.set_velocity(angle)

    def bounce_walls(self, walls):
        """Ensure ball remains contained within the given Rect (walls)"""
        if self.rect.bottom >= walls.bottom:
            #kill the ball
            self.dead = True
            self.vel_x = 0
            self_vel_y = 0
            self.kill()
        elif self.rect.left <= walls.left:
            self.vel_x = -self.vel_x
        elif self.rect.right >= walls.right:
            self.vel_x = -self.vel_x
        elif self.rect.top <= walls.top:
            self.vel_y = -self.vel_y

    def set_velocity(self, angle, speed = -1):
        if speed <> -1:
            self.speed = speed
        rad = math.radians(angle)
        self.vel_x = self.speed * math.cos(rad)
        self.vel_y = self.speed * math.sin(rad)

    def update(self, arena):
        self.rect.move_ip( self.vel_x, self.vel_y )
        self.rect.clamp_ip(arena)

#### class: Block ######################################################################
class Block(pygame.sprite.Sprite):

    WIDTH = 32
    HEIGHT = 16

    def __init__(self, arena, pos, color = GRAY):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.load_sprite()
        self.rect = self.image.get_rect()
        self.offset_x = arena.x
        self.offset_y = arena.y
        self.set_grid_position(pos)

    def set_grid_position(self, pos):
        self.rect.x = (pos[0] * self.WIDTH) + self.offset_x
        self.rect.y = (pos[1] * self.HEIGHT) + self.offset_y

    def load_sprite(self):
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.image.fill(self.color)
        pygame.draw.rect(self.image, GRAY, (0, 0, self.WIDTH, self.HEIGHT), 1)

    def generate_level(arena, level):
        pass


def terminate():
    pygame.quit()
    sys.exit()

def generate_level(arena, level):
        sprites = []
        for i in range(2, 13):
            sprites.append( Block(arena, (i, 4), (255,40,40)) )
            sprites.append( Block(arena, (i, 5), (40,255,40)) )
            sprites.append( Block(arena, (i, 6), (40,40,255)) )
        return sprites
        #return []


#### main ###############################################
pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((MAX_X, MAX_Y))
BASICFONT = pygame.font.SysFont('courier', 25, True)
pygame.display.set_caption('pyGame Template')
random.seed()

score = 0
lives = 2
level = 1

#create sprites and groups
arena_rect = pygame.Rect(20, 20, 15 * Block.WIDTH, MAX_Y)
paddle = pygame.sprite.GroupSingle( Paddle(arena_rect) )
balls = pygame.sprite.RenderPlain( Ball(arena_rect.center) )
blocks = pygame.sprite.RenderPlain()

l = generate_level(arena_rect, level)
blocks.add(l)

right_margin_center = (MAX_X - arena_rect.right)/2 + arena_rect.right

score_title_img = BASICFONT.render("SCORE", True, ORANGE, BGCOLOR)
score_title_x = right_margin_center - score_title_img.get_width()/2
lives_title_img = BASICFONT.render("LIVES", True, ORANGE, BGCOLOR)
lives_title_x = right_margin_center - lives_title_img.get_width()/2
level_title_img = BASICFONT.render("LEVEL", True, ORANGE, BGCOLOR)
level_title_x = right_margin_center - level_title_img.get_width()/2

while True:

    #event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()

        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                for ball in paddle.sprite.balls_held:
                    ball.bounce_paddle(paddle.sprite)
                    paddle.sprite.throw_ball(ball)

        elif event.type == KEYUP:
            if event.key == K_ESCAPE:
                terminate()


    #update game state
    paddle.update(arena_rect)
    balls.update(arena_rect)
    blocks.update()

    # detect collisions with paddle
    for ball in pygame.sprite.spritecollide(paddle.sprite, balls, 0):
        ball.bounce_paddle(paddle.sprite)
        #ball.vel_x = 0
        #ball.vel_y = 0
        #paddle.sprite.catch_ball(ball)

    # detect collisions with walls
    for ball in balls.sprites():
        ball.bounce_walls(arena_rect)


    # detect collisions with blocks
    for ball in balls.sprites():
        blocks_collided = pygame.sprite.spritecollide(ball, blocks, False)

        if blocks_collided:
            orig_rect = ball.rect
            left = right = up = down = 0
            for b in blocks_collided:
                # block = []  ball = ()

                # ([)]
                if orig_rect.left < b.rect.left < orig_rect.right < b.rect.right:
                    ball.rect.right = b.rect.left
                    left = -1

                # [(])
                if b.rect.left < orig_rect.left < b.rect.right < orig_rect.right:
                    ball.rect.left = b.rect.right
                    right = 1

                # top ([)] bottom
                if orig_rect.top < b.rect.top < orig_rect.bottom < b.rect.bottom:
                    ball.rect.bottom = b.rect.top
                    up = -1

                # top [(]) bottom
                if b.rect.top < orig_rect.top < b.rect.bottom < orig_rect.bottom:
                    ball.rect.top = b.rect.bottom
                    down = 1

                b.kill()
                score += 10

            #print left, up, right, down
            if (left + right ) != 0:
                ball.vel_x = (left + right)*abs(ball.vel_x)
            if (up + down) != 0:
                ball.vel_y = (up + down)*abs(ball.vel_y)


    if not balls:
        if lives == 0:
            gameover = True
            print "GAMEOVER!"
        else:
            lives -= 1
            balls.add( Ball(arena_rect.center) )
            print "lives: ", lives

    if not blocks:
        level += 1
        score += level*100
        balls.empty()
        balls.add( Ball(arena_rect.center) )
        blocks.empty()
        blocks.add( generate_level(arena_rect, level) )



    # draw frame
    DISPLAYSURF.fill(BGCOLOR)
    paddle.draw(DISPLAYSURF)
    balls.draw(DISPLAYSURF)
    blocks.draw(DISPLAYSURF)

    level_img = BASICFONT.render("%d"%(level), True, WHITE, BGCOLOR)
    x = right_margin_center - level_img.get_width()/2
    DISPLAYSURF.blit(level_title_img, (level_title_x, 200))
    DISPLAYSURF.blit(level_img, (x, 230))

    score_img = BASICFONT.render("%d"%(score), True, WHITE, BGCOLOR)
    x = right_margin_center - score_img.get_width()/2
    DISPLAYSURF.blit(score_title_img, (score_title_x, 300))
    DISPLAYSURF.blit(score_img, (x, 330))

    lives_img = BASICFONT.render("%d"%(lives), True, WHITE, BGCOLOR)
    x = right_margin_center - lives_img.get_width()/2
    DISPLAYSURF.blit(lives_title_img, (lives_title_x, 400))
    DISPLAYSURF.blit(lives_img, (x, 430))



    pygame.draw.rect(DISPLAYSURF, RED, arena_rect, 1)
    #pygame.display.update()
    pygame.display.flip()
    FPSCLOCK.tick(FPS)

terminate()



#!/usr/bin/env python

import pygame, sys, math, random
from pygame.locals import *

FPS = 30
MAX_X = 600
MAX_Y = 600

WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
GRAY  =     (128, 128, 128)
DARKGRAY  = ( 40,  40,  40)
RED       = (255,  40,  40)
BGCOLOR = BLACK
FONTSIZE = 15
SHIP_ACCEL = 1


####################################
class Ship():
    pos_x = MAX_X//2
    pos_y = 15
    vel_x = 0
    vel_y = 0
    fuel = 250
    crashed = False
    landed = False
    color = WHITE

    def __init__(self):
        self.reset()

    def reset(self):
        self.pos_x = MAX_X//2
        self.pos_y = 40
        self.vel_x = 0
        self.vel_y = 0
        self.fuel = 250
        self.crashed = False
        self.landed = False
        self.color = WHITE

    def thrust_left(self):
        if self.fuel > 0:
            self.vel_x -= 0.1
            self.fuel -= 1

    def thrust_right(self):
        if self.fuel > 0:
            self.vel_x += 0.1
            self.fuel -= 1

    def thrust(self):
        if self.fuel > 0:
            self.vel_y += 0.4
            self.fuel -= 2

    def update(self):
        self.vel_y -= 0.1

        self.pos_x += self.vel_x
        self.pos_y -= self.vel_y

        if self.pos_x > MAX_X:
            self.pos_x = 0
        if self.pos_x < 0:
            self.pos_x = MAX_X

    def detect_crash(self, seg):
        last_pt = seg[0]
        b = self.get_lower_bound()
        for pt in seg[1:]:
            if intersect(b[0], b[1], last_pt, pt):
                self.crashed = True
                self.color = RED
                return self.crashed
            last_pt = pt
        return self.crashed

    def detect_landing(self, plat):
        x1 = plat[0][0]
        x2 = plat[1][0]
        y  = plat[0][1]
        b = self.get_lower_bound()
        landed = False
        if b[0][1] > y and x1 <= b[0][0] and b[1][0] <= x2:
            self.pos_y = y-6  #using 6 from get_bounds()
            if self.vel_y < -5:
                self.landed = False
                self.crashed = True
                self.color = RED
            else:
                self.landed = True

        return landed


    def get_bounds(self):
        return ( (self.pos_x-10, self.pos_y-12),
            (self.pos_x+10, self.pos_y-12),
            (self.pos_x+10, self.pos_y+6),
            (self.pos_x-10, self.pos_y+6))

    def get_lower_bound(self):
        b = self.get_bounds()
        return (b[2], b[3])

    def draw(self, thrust = False):
        x = int(self.pos_x)
        y = int(self.pos_y)
        if thrust and not self.crashed:
            pygame.draw.polygon(DISPLAYSURF, RED, ((x-3, y+3), (x, y+12), (x+3, y+3)) )
        pygame.draw.circle(DISPLAYSURF, self.color, (x, y-4), 8)
        pygame.draw.line(DISPLAYSURF, self.color, (x, y-4), (x+10, y-4+8), 3)
        pygame.draw.line(DISPLAYSURF, self.color, (x, y-4), (x-10, y-4+8), 3)

        c = WHITE
        if self.fuel < 50:
            c = RED
        msg = 'FUEL %3d     ALT %3d     VERT SPD %3d     HORZ SPD %3d'%(self.fuel, MAX_Y-self.pos_y, self.vel_y, self.vel_x)
        msg_disp = BASICFONT.render(msg, True, c, BLACK)
        DISPLAYSURF.blit(msg_disp, (25, MAX_Y-FONTSIZE-5))

    def animate_crash(self):
        for i in range(1, FPS):
            #do something
            advance_frame()

####################################
class Planet():

    segments = []
    platform = []
    seg_size = 40
    num_of_segments = MAX_X // seg_size

    platform_seg = 3

    seg_max_y = MAX_Y-50
    seg_min_y = 150

    def __init__(self):
        segments = self.generate_level()

    def generate_level(self):
        self.segments = []
        self.platform_seg = random.randint(2, self.num_of_segments-2)
        for i in range (0, self.num_of_segments+1):
            amp = random.randint(50, 100)
            factor = random.randint(110, 140)
            shift = random.randint(0, 50)
            rand = random.randint(-20, 50)

            x = i*self.seg_size

            if i != self.platform_seg:
                y = int(80 * math.sin(120 * i + 50) + rand + 400)

            self.segments.append( (x,y) )

        self.platform = (self.segments[self.platform_seg-1], self.segments[self.platform_seg])


    def draw(self):
        pygame.draw.lines(DISPLAYSURF, WHITE, False, self.segments, 1)
        pygame.draw.line(DISPLAYSURF, RED, self.platform[0], self.platform[1], 4)


####################################
def terminate():
    pygame.quit()
    sys.exit()

def advance_frame():
    pygame.display.update()
    FPSCLOCK.tick(FPS)

#http://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
def ccw(A,B,C):
    #return (C.y-A.y)*(B.x-A.x) > (B.y-A.y)*(C.x-A.x)
    return (C[1]-A[1])*(B[0]-A[0]) > (B[1]-A[1])*(C[0]-A[0])

def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)



####################################
# main
pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((MAX_X, MAX_Y))
BASICFONT = pygame.font.SysFont('courier', FONTSIZE)
pygame.display.set_caption('Lunar Lander')
random.seed()

s = Ship()
p = Planet()
level = 1
score = 0
lives = 2

# use name-value pairs (dictionary?) for this?
cmdLeft = False
cmdRight = False
cmdThrust = False
cmdBrake = False

gameover = False

# MAIN GAME LOOP
while not gameover:

    #event handling
    for event in pygame.event.get():
        if event.type == QUIT:         terminate()

        elif event.type == KEYDOWN:
            if event.key == K_UP:      cmdThrust = True
            elif event.key == K_LEFT:  cmdLeft = True
            elif event.key == K_RIGHT: cmdRight = True
            elif event.key == K_r:
                score = 0
                level = 1
                lives = 3
                p.generate_level()
                s.reset()
                crashed = True

        elif event.type == KEYUP:
            if event.key == K_ESCAPE:  terminate()
            elif event.key == K_UP:    cmdThrust = False
            elif event.key == K_LEFT:  cmdLeft = False
            elif event.key == K_RIGHT: cmdRight = False


    if not s.landed and not s.crashed:
        # update game state
        if cmdThrust:   s.thrust()
        elif cmdLeft:   s.thrust_left()
        elif cmdRight:  s.thrust_right()

        s.update()

        s.detect_landing(p.platform)
        s.detect_crash(p.segments)


    # draw frame
    DISPLAYSURF.fill(BGCOLOR)

    score_msg = "LEVEL: %d    SCORE: %d    SHIPS: %d"%(level, score, lives)
    score_msg_disp = BASICFONT.render(score_msg, True, WHITE, BLACK)
    DISPLAYSURF.blit(score_msg_disp, (10, 10))

    if s.crashed:
        crash_msg = "YOU HAVE CRASHED!"
        crash_msg_disp = BASICFONT.render(crash_msg, True, RED, BLACK)
        DISPLAYSURF.blit(crash_msg_disp, (225, 95))
        lives -= 1
        if lives < 0:
            gameover = True

    if s.landed:
        crash_msg = "Success, you have safely landed!"
        crash_msg_disp = BASICFONT.render(crash_msg, True, WHITE, BLACK)
        DISPLAYSURF.blit(crash_msg_disp, (150, 80))
        score += level * 10
        score += s.fuel
        level += 1

    s.draw(cmdThrust)
    p.draw()

    advance_frame()

    if s.landed:
        pygame.time.wait(2000)
        p.generate_level()
        s.reset()

    if s.crashed:
        pygame.time.wait(2000)
        s.reset()


terminate()

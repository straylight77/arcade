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
BLUE      = (40,   40, 255)
GREEN     = (40,  255,  40)
BGCOLOR   = BLACK


#---- class: Paddle ------------------------------------------------------
class Paddle(pygame.sprite.Sprite):

    def __init__(self, pos, color = BLUE):
        pygame.sprite.Sprite.__init__(self)
        self.load_sprite(color)
        self.score = 0
        self.rect.center = pos
        self.cmd = [0, 0] # [up, down]
        self.speed = 8

    def load_sprite(self, color):
        self.image = pygame.Surface((16, 80))
        self.image.fill(BGCOLOR)
        self.image.set_colorkey(BGCOLOR)
        pygame.draw.rect(self.image, color, (0, 8, 16, 64))
        pygame.draw.circle(self.image, color, (8, 8), 8)
        pygame.draw.circle(self.image, color, (8, 72), 8)
        self.rect = self.image.get_rect()

    def set_cmd(self, index):
        """Set various commands based on user input. 0 = up,  1 = down"""
        self.cmd[index] = 1

    def unset_cmd(self, index):
        """Clear a command. 0 = up,  1 = down"""
        self.cmd[index] = 0

    def clear_cmd(self):
        """Clear all commands currently set."""
        for i in range(0, len(self.cmd)):
            self.cmd[i] = 0

    def update(self):
        dy = (self.cmd[1] - self.cmd[0]) * self.speed
        self.rect.move_ip(0, dy)
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > MAX_Y:
            self.rect.bottom = MAX_Y

    def get_score_img(self):
        return img

#---- class: Ball --------------------------------------------------------
class Ball(pygame.sprite.Sprite):

    def __init__(self, vel = None, pos = None):
        pygame.sprite.Sprite.__init__(self)
        if pos == None:
            pos = [MAX_X/2, MAX_Y/2]
        self.pos = pos
        if vel == None:
            vel = [3, 4]
        self.vel = vel
        self.load_sprite()

    def load_sprite(self):
        self.image = pygame.Surface((16, 16))
        self.image.fill(BGCOLOR)
        self.image.set_colorkey(BGCOLOR)
        pygame.draw.circle(self.image, RED, (8, 8), 8)
        self.rect = self.image.get_rect()

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.rect.center = self.pos


#---- class: Game --------------------------------------------------------
class Game():

    def __init__(self, display):
        self.display = display


def terminate():
    pygame.quit()
    sys.exit()

def advance_frame():
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def handle_events():
    pass

#### main ################################################################
def main():
    pygame.init()
    CLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((MAX_X, MAX_Y))
    FONT1 = pygame.font.SysFont('courier', 45)
    pygame.display.set_caption('pyGame Template')
    random.seed()

    player1 = Paddle((20, MAX_Y/2), BLUE)
    player2 = Paddle((MAX_X-20, MAX_Y/2), GREEN)
    players = pygame.sprite.RenderPlain(player1, player2)

    balls = pygame.sprite.RenderPlain( Ball() )
    arena = pygame.Rect(0, 0, MAX_X, MAX_Y)
    allsprites = pygame.sprite.Group(players, balls)

    while True:
        #event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            #TODO should this check be made within Paddle?
            elif event.type == KEYDOWN:
                if event.key == K_UP:     player2.set_cmd(0)
                elif event.key == K_DOWN: player2.set_cmd(1)
                elif event.key == K_w:    player1.set_cmd(0)
                elif event.key == K_s:    player1.set_cmd(1)

            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_UP:   player2.unset_cmd(0)
                elif event.key == K_DOWN: player2.unset_cmd(1)
                elif event.key == K_w:    player1.unset_cmd(0)
                elif event.key == K_s:    player1.unset_cmd(1)

        # update game state
        players.update()
        balls.update()


        # detect ball colliding with walls or endzones
        for b in balls:
            if b.rect.top < 0 or b.rect.bottom > MAX_Y:
                b.vel[1] = -b.vel[1]

            if b.rect.right < 0:
                player2.score += 1
                b.kill()
                balls.add(Ball([4, 5]))

            if b.rect.left > MAX_X:
                player1.score += 1
                b.kill()
                balls.add(Ball([-4, 5]))

        # detect collision with paddles
        for b in pygame.sprite.spritecollide(player1, balls, 0):
            b.vel[0] = -b.vel[0]
        for b in pygame.sprite.spritecollide(player2, balls, 0):
            b.vel[0] = -b.vel[0]


        # draw frame
        DISPLAY.fill(BGCOLOR)

        players.draw(DISPLAY)
        balls.draw(DISPLAY)

        p1_img = FONT1.render("%d"%(player1.score), True, GRAY, BGCOLOR)
        p1_img_pos = ( MAX_X/4-p1_img.get_width(), 10 )
        DISPLAY.blit(p1_img, p1_img_pos )

        p2_img = FONT1.render("%d"%(player2.score), True, GRAY, BGCOLOR)
        p2_img_pos = ( MAX_X*3/4-p2_img.get_width(), 10 )
        DISPLAY.blit(p2_img, p2_img_pos )

        pygame.draw.line(DISPLAY, GRAY, (MAX_X/2, 0), (MAX_X/2, MAX_Y))

        pygame.display.update()
        CLOCK.tick(FPS)

    terminate()

if __name__ == '__main__':
    main()





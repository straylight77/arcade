import pygame, sys, math, random
from pygame.locals import *

FPS = 30
MAX_X = 800
MAX_Y = 600

WHITE     = (255, 255, 255)
GRAY      = (128, 128, 128)
DARKGRAY  = ( 40,  40,  40)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
ORANGE    = (255, 128,   0)
YELLOW    = (255, 255,   0)
GREEN     = (40,  255,   0)
BLUE      = ( 0,    0, 255)
VIOLET    = (255,   0, 255)
BGCOLOR = BLACK

#---- class: Spritesheet -------------------------------------------------
class Spritesheet():
    """
    Helper class to manage loading sprite sheet image files, slicing
    them up into frames.  Ensures only one copy exists in memory.
    """

    sprites = { }
    sheet1 = None
    sheet2 = None

    def __init__(self):
        self.load_asteroid_sprites()
        self.load_explosion_sprites()

    def load_asteroid_sprites(self):
        self.sheet1 = pygame.image.load('assets/asteroid2.png')
        images = []
        s = 64
        for y in range(0,6):
            for x in range (0, 5):
                img = self.sheet1.subsurface((x*s, y*s, s, s))
                images.append(img)
        self.sprites['asteroid'] = images


    def load_explosion_sprites(self):
        self.sheet2 = pygame.image.load('assets/explosion1_64x64.png')
        images = []
        s = 64
        for y in range(0, 5):
            for x in range (0, 5):
                img = self.sheet2.subsurface((x*s, y*s, s, s))
                images.append(img)
        self.sprites['explosion'] = images

    def get_sprites(self, name):
        return self.sprites[name]



#---- class: AnimatedSprite ----------------------------------------------
class AnimatedSprite(pygame.sprite.Sprite):

    frames = None  #list of ordered images used for animation
    repeat = True  #loop through frames or stop at the last one?

    @classmethod
    def set_frames(cls, frame_images):
        cls.frames = frame_images

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect()

    def advance_frame(self, increment = 1):
        self.index += increment
        max_index = len(self.frames)-1
        if self.index > max_index:
            if self.repeat:
                self.index = 0
            else:
                self.index = max_index

    def is_done(self):
        return not self.repeat and self.index >= len(self.frames)-1

    def update(self, frames = 1):
        self.advance_frame(frames)
        self.image = self.frames[self.index]
        if self.is_done():
            self.kill()


#---- class: Asteroid ----------------------------------------------------
class Asteroid(AnimatedSprite):

    def __init__(self, pos = [0,0], index = 0):
        AnimatedSprite.__init__(self)
        self.pos = pos
        self.index = index
        self.vel = [0, 0]

    def update(self):
        AnimatedSprite.update(self)
        self.rect.center = self.pos


#---- class: Explosion ---------------------------------------------------
class Explosion(AnimatedSprite):

    def __init__(self, pos):
        AnimatedSprite.__init__(self)
        self.repeat = False
        self.pos = pos
        self.rect.center = pos


#---- class: Game --------------------------------------------------------
class Game():

    max_x = 0
    max_y = 0
    gameover = False
    display = None
    clock = None

    def __init__(self, display, clock):
        self.display = display
        self.clock = clock

        self.sheet = Spritesheet()
        Asteroid.set_frames( self.sheet.sprites['asteroid'] )
        Explosion.set_frames( self.sheet.get_sprites('explosion') )

        self.grp = pygame.sprite.RenderPlain()
        self.create_level()

    def create_level(self):
        self.grp.add( Asteroid([MAX_X/2, MAX_Y/2]) )
        self.grp.add( Asteroid([MAX_X/2+65, MAX_Y/2], 15) )
        self.grp.add( Explosion([MAX_X/2, MAX_Y/2+65]) )


    def main_loop(self):
        while not self.gameover:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def update(self):
        self.grp.update()

    def draw(self):
        self.display.fill(BGCOLOR)
        self.grp.draw(self.display)
        pygame.display.update()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    #terminate()
                    self.gameover = True


##### functions ##########################################################
def terminate():
    pygame.quit()
    sys.exit()


def init(max_x, max_y, title = 'pyGame Template'):
    pygame.init()
    clk = pygame.time.Clock()
    disp = pygame.display.set_mode((max_x, max_y))
    pygame.display.set_caption(title)
    random.seed()
    return disp, clk



#---- main() -------------------------------------------------------------
def main():
    #init pygame

    DISPLAY, CLOCK = init(MAX_X, MAX_Y)
    FONT1 = pygame.font.SysFont('courier', 15)

    #main game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_SPACE:
                    g = Game(DISPLAY, CLOCK)
                    g.main_loop()

        # draw main screen
        DISPLAY.fill(BGCOLOR)
        pygame.display.update()
        CLOCK.tick(FPS)


    terminate()

####
if __name__ == '__main__':
    main()




import pygame
pygame.init()

LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
JOM = pygame.mixer.Sound("VineBoom.mp3")



class Player:
    def __init__(self, left, right, up):
        print("New player made!")
        self.xpos = 500  # xpos of player
        self.ypos = 200  # ypos of player
        self.vx = 0  # x velocity of player
        self.vy = 0.2  # y velocity of player
        # this list holds whether each key has been pressed
        self.keys = [False, False, False, False]
        # this variable stops gravity from pulling you down more when on a platform
        self.isOnGround = False
        self.friction = 1
        self.leftKey = left
        self.rightKey = right
        self.upKey = up


    def move(self, gameEvents):

        for event in gameEvents:  # quit game if x is pressed in top corner
            if event.type == pygame.KEYDOWN:  # keyboard input
                if event.key == self.leftKey:
                    self.keys[LEFT] = True

                elif event.key == self.rightKey:
                    self.keys[RIGHT] = True

                elif event.key == self.upKey:
                    self.keys[UP] = True
            elif event.type == pygame.KEYUP:
                if event.key == self.leftKey:
                    self.keys[LEFT] = False

                elif event.key == self.upKey:
                    self.keys[UP] = False

                elif event.key == self.rightKey:
                    self.keys[RIGHT] = False

        # physics section--------------------------------------------------------------------
        # LEFT MOVEMENT
        if self.keys[LEFT] == True:
            self.vx = -3
            direction = LEFT

        elif self.keys[RIGHT] == True:
            self.vx = +3
            direction = RIGHT

        # turn off velocity
        else:
            if abs(self.vx) > 0:
                self.vx -= (self.vx / abs(self.vx)) * self.friction

            # JUMPING
        if self.keys[UP] == True and self.isOnGround == True:  # only jump when on the ground
            self.vy = -8
            self.isOnGround = False
            direction = UP

        # stop falling if on bottom of game screen
        if self.ypos > 760:
            self.isOnGround = True
            self.vy = 0
            self.ypos = 760

        # gravity
        if self.isOnGround == False:
            self.vy += .2  # notice this grows over time, aka ACCELERATION
                
        # update player position
        self.xpos += self.vx
        self.ypos += self.vy
        print (self.xpos, self.ypos, self.isOnGround, self.vy)


    def draw(self, screen):
        pygame.draw.rect(screen, (100, 200, 100), (self.xpos, self.ypos, 20, 40))
import pygame
pygame.init()

NONE = -1
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
JOM = pygame.mixer.Sound("VineBoom.mp3")
SIZE_X = 40
SIZE_Y = 80
GRAVITY_ITERATION = .15
HOVER_TOLERANCE = 5
JUMP_CONTROL = 0.2
COLLISION_TOLERANCE = 10


class Player:
    def __init__(self, left, right, up, color):
        print("New player made!")
        self.xpos = 500  # xpos of player
        self.ypos = 200  # ypos of player
        self.vx = 0  # x velocity of player
        self.vy = 0.2  # y velocity of player
        # this list holds whether each key has been pressed
        self.keys = [False, False, False, False]
        self.colliding = [False, False, False, False]
        # this variable stops gravity from pulling you down more when on a platform
        self.isOnGround = False
        self.leftKey = left
        self.rightKey = right
        self.upKey = up
        self.color = color
        self.gravity = 0
        self.friction = 0.05 
        self.moveSpeed = 6
        self.jumpDirection = NONE
        self.rect = pygame.Rect((self.xpos, self.ypos), (SIZE_X,SIZE_Y))
        self.jumpHeight = 22
        self.ground = 800

    def move(self, gameEvents, platforms):
        startingVx = self.vx

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
            self.vx -= self.moveSpeed
            self.vx = pygame.math.clamp(self.vx, -self.moveSpeed, self.moveSpeed)
            direction = LEFT

        elif self.keys[RIGHT] == True:
            self.vx += self.moveSpeed
            self.vx = pygame.math.clamp(self.vx, -self.moveSpeed, self.moveSpeed)
            direction = RIGHT

        # turn off velocity
        else:
            direction = NONE
            self.vx = pygame.math.lerp(self.vx, 0, self.friction)

        self.touchGround()

            # JUMPING
        if self.keys[UP] == True and self.isOnGround == True:  # only jump when on the ground
            self.vy -= self.jumpHeight
            self.vx *= 1.5
            self.isOnGround = False
            self.jumpDirection = direction 
        if not self.keys[UP] and not self.isOnGround and self.vy < 0:
             self.vy = pygame.math.lerp(self.vy, 0, JUMP_CONTROL)

        # gravity
        if self.isOnGround == False: # I fixed it - Tess. You forgot to add an == False here dumb dumb.
            self.friction = 1
            self.gravity += GRAVITY_ITERATION
            if abs(self.vy) > HOVER_TOLERANCE:
                self.vy += self.gravity
            else: self.vy += self.gravity/2
            if self.jumpDirection == LEFT:
                self.vx -= 0.1
            elif self.jumpDirection == RIGHT:
                self.vx += 0.1
                
        for platform in platforms:
            self.collide(platform.getRect())
            self.predictedRect = pygame.Rect(pygame.Rect((self.xpos + self.vx, self.ypos + self.vy), (SIZE_X,SIZE_Y)))
        
        if self.colliding[UP] and self.vy < 0 or self.colliding[DOWN] and self.vy > 0:
            self.ypos -= self.vy
            self.vy = 0
        if self.colliding[LEFT] and self.vx < 0 or self.colliding[RIGHT] and self.vx > 0:
            self.xpos -= self.vx
            self.vx = 0
                
        # update player position
        self.xpos += self.vx
        self.ypos += self.vy
        self.rect = pygame.Rect(pygame.Rect((self.xpos, self.ypos), (SIZE_X,SIZE_Y)))
        
    def touchGround(self):
        if self.ypos + SIZE_Y + self.vy > self.ground or self.isOnGround:
            self.isOnGround = True
            self.vy = 0
            self.ypos = self.ground - SIZE_Y
            self.gravity = 0


    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
    
    def collide(self, otherRect):
        if not pygame.Rect.colliderect(self.rect, otherRect):
            self.colliding = [False, False, False, False]
            return
        self.colliding[LEFT] = abs(self.predictedRect.left - otherRect.right) < COLLISION_TOLERANCE
        self.colliding[RIGHT] = abs(self.predictedRect.right - otherRect.left) < COLLISION_TOLERANCE
        self.colliding[UP] = abs(self.predictedRect.top - otherRect.bottom) < COLLISION_TOLERANCE
        self.colliding[DOWN] = abs(self.predictedRect.bottom - otherRect.top) < COLLISION_TOLERANCE
        if self.colliding[DOWN] or self.colliding == [False, False, False, False]:
            self.ground = otherRect.top
        else:
            self.ground = 800
        if self.colliding[LEFT]:
            self.xpos = otherRect.right
        if self.colliding[RIGHT]:
            self.xpos = otherRect.left - SIZE_X
        if self.colliding[UP]:
            self.ypos = otherRect.bottom 
        print(self.colliding)
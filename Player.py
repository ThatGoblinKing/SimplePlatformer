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
COLLISION_TOLERANCE = 15
SPRITE_SHEET = pygame.transform.scale(pygame.image.load('RunningSpriteSheetFull.png'), (161 * 4, 46 * 4))
FRAME_WIDTH = 92
FRAME_HEIGHT = 92
RUN_CYCLE_LENGTH = 875
FRAME_HOLD_LENGTH = 125
SPRITE_OFFSET_X = 25
SPRITE_OFFSET_Y = 12
INVINCIBILITY_TIME = 500

class Player:
    def __init__(self, left, right, up, color):
        print("New player made!")
        self.rowNum = 0
        self.frameNum = 0
        self.ticker = 0
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
        self.jumpHeight = 16
        self.ground = 800
        self.platformLeft = 0
        self.platformRight = 0
        self.health = 3
        self.nextDamageFrame = 0
        
    def animate(self):
        if self.vx < 0:
            frameNum = int((pygame.time.get_ticks() % RUN_CYCLE_LENGTH) / FRAME_HOLD_LENGTH)
            self.rowNum = 1
        elif self.vx > 0:
            frameNum = int((pygame.time.get_ticks() % RUN_CYCLE_LENGTH) / FRAME_HOLD_LENGTH)
            self.rowNum = 0
        else: frameNum = 0
        self.spriteProperties = (FRAME_WIDTH * frameNum, self.rowNum * FRAME_HEIGHT, FRAME_WIDTH, FRAME_HEIGHT)
            

    def move(self, gameEvents, platforms, enemies):

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
                
        self.predictedRect = pygame.Rect(pygame.Rect((self.xpos + self.vx, self.ypos + self.vy), (SIZE_X,SIZE_Y)))
            
        for platform in platforms:
            self.collide(platform.getRect())
            
        for enemy in enemies:
            self.collideEnemy(enemy.getRect())
            

        
        if self.colliding[UP] and self.vy < 0 or self.colliding[DOWN] and self.vy > 0:
            self.vy = 0
        else: self.ypos += self.vy
        if self.colliding[LEFT] and self.vx < 0 or self.colliding[RIGHT] and self.vx > 0:
            self.vx = 0
        else: self.xpos += self.vx
                
        # update player position
        self.animate()
        self.rect = pygame.Rect(pygame.Rect((self.xpos, self.ypos), (SIZE_X,SIZE_Y)))
        
    def touchGround(self):
        if self.xpos + SIZE_X < self.platformLeft or self.xpos > self.platformRight: 
            self.ground = 800
        if self.ypos + SIZE_Y + self.vy > self.ground or self.isOnGround:
            self.isOnGround = True
            self.vy = 0
            self.ypos = self.ground - SIZE_Y
            self.gravity = 0


    def draw(self, screen):
        #pygame.draw.rect(screen, (255,255,255), self.predictedRect)
        #pygame.draw.rect(screen, (0, 255, 0), self.rect, 5)
        screen.blit(SPRITE_SHEET, (self.xpos - SPRITE_OFFSET_X, self.ypos - SPRITE_OFFSET_Y), self.spriteProperties)
    
    def collide(self, otherRect):
        if not pygame.Rect.colliderect(self.predictedRect, otherRect):
            self.colliding = [False, False, False, False]
            return
        
        
        self.platformLeft = otherRect.left
        self.platformRight = otherRect.right
        print(self.isOnGround)
        print("Collision attempted")

        self.colliding[LEFT] = abs(self.predictedRect.left + self.vx - otherRect.right) < COLLISION_TOLERANCE
        self.colliding[RIGHT] = abs(self.predictedRect.right + self.vx - otherRect.left) < COLLISION_TOLERANCE
        self.colliding[UP] = abs(self.predictedRect.top + self.vy - otherRect.bottom) < COLLISION_TOLERANCE
        self.colliding[DOWN] = abs(self.predictedRect.bottom + self.vy - otherRect.top) < COLLISION_TOLERANCE
        if self.colliding == [True, False, False, False]:
            self.xpos = otherRect.right
            # print("Left")
        elif self.colliding == [False, True, False, False]:
            self.xpos = otherRect.left - SIZE_X
            # print("Right")
        elif self.colliding == [False, False, True, False]:
            self.ypos = otherRect.bottom 
            # print("Top")
        elif self.colliding == [False, False, False, True]:
            self.ground = otherRect.top
            print(self.ground)
            # print("Bottom")
            return
        else:
            # print("Had to go to secondary check")
            centerDistanceY = self.predictedRect.height / 2 - otherRect.height / 2
            centerDistanceX = self.predictedRect.width / 2 - otherRect.width / 2
            
            if abs(centerDistanceY) > COLLISION_TOLERANCE and centerDistanceY > centerDistanceX:
                if centerDistanceY < 0:
                    self.colliding[DOWN] = True
                    self.ground = otherRect.top
                    self.ypos = otherRect.top + SIZE_Y
                    self.isOnGround = True
                    print("down")
                else:
                    self.colliding[UP] = True
                    self.ypos = otherRect.bottom
                    print("up")
                    print(self.colliding)
                return
            elif abs(centerDistanceX) > COLLISION_TOLERANCE:
                if centerDistanceX > 0:
                    self.colliding[RIGHT] = True
                    self.xpos = otherRect.left
                    print("Right")
                else:
                    self.colliding[LEFT] = True
                    self.xpos = otherRect.right
                    print("left")
                    
    def collideEnemy(self, enemyRect):
        if not pygame.Rect.colliderect(self.predictedRect, enemyRect):
            return
        time = pygame.time.get_ticks()
        if time > self.nextDamageFrame:
            self.health -= 1
            self.nextDamageFrame = time + INVINCIBILITY_TIME
        

    def getHealth(self):
        return self.health
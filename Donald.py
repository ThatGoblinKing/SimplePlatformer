import pygame
class Enemy:

    SIZE_X = 40
    SIZE_Y = 40
    SPEED = 3
    

    def __init__(self, startingX, startingY):
        self.x = startingX
        self.y = startingY
        self.rect = pygame.Rect((self.x, self.y), (Enemy.SIZE_X, Enemy.SIZE_Y))
        
    def update(self):
        pass

    def moveBy(self, x, y):
        self.x += x
        self.y += y
    
    def moveTo(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self):
        pass
    
    def getRect(self):
        return self.rect
    
class Donald(Enemy):
    def __init__(self, startingX, startingY, cycle):
        self.cycle = cycle
        self.nextCycleTime = 0
        self.direction = 1
        Enemy.__init__(self, startingX, startingY)
        
    def update(self):
        time = pygame.time.get_ticks()
        if time > self.nextCycleTime:
            self.nextCycleTime += self.cycle
            self.direction *= -1
        self.moveBy(Enemy.SPEED * self.direction, 0)
        self.rect = pygame.Rect((self.x, self.y), (Enemy.SIZE_X, Enemy.SIZE_Y))
        
        
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
import pygame
import Player
import Platform
import math
pygame.init()
pygame.display.set_caption("easy platformer")  # sets the window title
screen = pygame.display.set_mode((800, 800))  # creates game screen
screen.fill((0, 0, 0))
clock = pygame.time.Clock()  # set up clock
gameover = False  # variable to run our game loop


# player variables
xpos = 500  # xpos of player
ypos = 200  # ypos of player
vx = 0  # x velocity of player
vy = 0  # y velocity of player
# this list holds whether each key has been pressed
keys = [False, False, False, False]
# this variable stops gravity from pulling you down more when on a platform
isOnGround = False
isOnBouncePad = False
friction = 1

player1 = Player.Player(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP)
player2 = Player.Player(pygame.K_a, pygame.K_d, pygame.K_w)


platforms = [Platform.Platform((400, 700), (500, 760), (255, 69, 169)), Platform.Platform(
    (0, 800), (800, 825), (0, 0, 0))]
boing = Platform.BouncePad((500, 750), (600, 800), (255, 255, 255), 1)


while not gameover:  # GAME LOOP############################################################
    clock.tick(60)  # FPS
    gameEvents = pygame.event.get()
    # Input Section------------------------------------------------------------
    for event in gameEvents:  # quit game if x is pressed in top corner
        if event.type == pygame.QUIT:
            gameover = True

    player1.move(gameEvents)
    player2.move(gameEvents)

    # RENDER Section--------------------------------------------------------------------------------

    screen.fill((0, 0, 0))  # wipe screen so it doesn't smear

    for platform in platforms:
        platform.draw(screen)
    boing.draw(screen)
    player1.draw(screen)
    player2.draw(screen)

    pygame.display.flip()  # this actually puts the pixel on the screen

# end game loop------------------------------------------------------------------------------
pygame.quit()

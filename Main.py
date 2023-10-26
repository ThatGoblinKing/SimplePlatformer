import pygame
import Player
import Platform
pygame.init()
pygame.display.set_caption("easy platformer")  # sets the window title
screen = pygame.display.set_mode((800, 800))  # creates game screen
screen.fill((0, 0, 0))
clock = pygame.time.Clock()  # set up clock
gameover = False  # variable to run our game loop

player1 = Player.Player(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, (0,0,255))
player2 = Player.Player(pygame.K_a, pygame.K_d, pygame.K_w, (255,0,0))

platforms = [Platform.Platform((0, 700), (100, 760), (255, 255, 255))]


while not gameover:  # GAME LOOP############################################################
    clock.tick(60)  # FPS
    gameEvents = pygame.event.get()
    # Input Section------------------------------------------------------------
    for event in gameEvents:  # quit game if x is pressed in top corner
        if event.type == pygame.QUIT:
            gameover = True

    player1.move(gameEvents, platforms)
    player2.move(gameEvents, platforms)

    # RENDER Section--------------------------------------------------------------------------------

    screen.fill((0, 0, 0))  # wipe screen so it doesn't smear

    player1.draw(screen)
    player2.draw(screen)
    for platform in platforms:
        platform.draw(screen)

    pygame.display.flip()  # this actually puts the pixel on the screen

# end game loop------------------------------------------------------------------------------
pygame.quit()

import pygame
import Player
import Donald
import Platform
pygame.init()
pygame.display.set_caption("easy platformer")  # sets the window title
screen = pygame.display.set_mode((800, 800))  # creates game screen
screen.fill((0, 0, 0))
clock = pygame.time.Clock()  # set up clock
gameover = False  # variable to run our game loop

player1 = Player.Player(pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, (0,0,255))
player2 = Player.Player(pygame.K_a, pygame.K_d, pygame.K_w, (255,0,0))

#platforms = [Platform.Platform((0, 200), (100, 800), (255, 255, 255)), Platform.Platform((350, 670), (450, 720), (255, 255, 255))]
platforms = []
enemies = [Donald.Donald(400, 760, 2000)]

while not gameover:  # GAME LOOP############################################################
    ticks = clock.get_time()
    clock.tick(60)  # FPS
    gameEvents = pygame.event.get()
    # Input Section------------------------------------------------------------
    for event in gameEvents:  # quit game if x is pressed in top corner
        if event.type == pygame.QUIT:
            gameover = True

    player1.move(gameEvents, platforms, enemies)
    health = player1.getHealth()
    player2.move(gameEvents, platforms, enemies)
    for enemy in enemies:
        enemy.update()

    # RENDER Section--------------------------------------------------------------------------------a

    screen.fill((0, 0, 0))  # wipe screen so it doesn't smear

    player1.draw(screen)
    player2.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    for platform in platforms:
        platform.draw(screen)
    font = pygame.font.SysFont(None, 64)
    img = font.render(f"{health}", True, (255, 255, 255))
    screen.blit(img, (0, 0))

    pygame.display.flip()  # this actually puts the pixel on the screen
    
    if health <= 0:
        gameover = True

# end game loop------------------------------------------------------------------------------
pygame.quit()

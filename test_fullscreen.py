import pygame

pygame.init()
pygame.display.set_mode((640, 480))
modes = pygame.display.list_modes()
# pygame.display.set_mode(modes[0], pygame.FULLSCREEN)
FULLSCREEN = False

notdone = True
while notdone:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            notdone = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                notdone = False
            elif event.key == pygame.K_f:
                if not FULLSCREEN:
                    pygame.display.set_mode(modes[0], pygame.FULLSCREEN)
                else:
                    pygame.display.set_mode((640, 480))
                FULLSCREEN = not FULLSCREEN

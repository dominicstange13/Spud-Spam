import pygame

pygame.init()

screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
mousepos = pygame.mouse.get_pos()

quitbutton = pygame.rect.Rect((1870,0),(50,50))

running = True

while running:
    mousepos = pygame.mouse.get_pos()
    pygame.draw.rect(screen, "Red", quitbutton)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and quitbutton.collidepoint(mousepos):
            running = False
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
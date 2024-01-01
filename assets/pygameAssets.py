
def basic_gun(pygame, screen, x, y):
    pygame.draw.rect(screen, (0, 255, 0), (x, y, 35, 35), 2)
    pygame.draw.line(screen, (0, 255, 0), ((x + 35), y), (x, (y + 35)), 2)
    return pygame



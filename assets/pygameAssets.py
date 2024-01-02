
def basic_gun(pygame, screen, x, y):
    pygame.draw.rect(screen, (0, 255, 0), (x, y, 35, 35), 2)
    pygame.draw.line(screen, (0, 255, 0), ((x + 35), y), (x, (y + 35)), 2)
    return pygame

def basic_enemy(pygame, screen, x, y):
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 35, 35), 2)
    pygame.draw.line(screen, (255, 0, 0), ((x + 35), y), (x, (y + 35)), 2)
    pygame.draw.line(screen, (255, 0, 0), (x, (y + 35)), ((x + 35), y), 2)
    return pygame

def basic_bullet(pygame, screen, x, y, r):
    pygame.draw.circle(screen, (0,0,255), (x,y), r)
    return pygame



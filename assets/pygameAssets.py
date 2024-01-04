

def basic_gun(pygame, screen, x, y, health):
    font = pygame.font.Font(None, 18)
    text_surface = font.render(str(health), True, (255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.center = (x + 17.5, y + 40)
    screen.blit(text_surface, text_rect)

    pygame.draw.rect(screen, (0, 255, 0), (x, y, 35, 35), 2)
    pygame.draw.line(screen, (0, 255, 0), ((x + 35), y), (x, (y + 35)), 2)
    return pygame

def basic_enemy(pygame, screen, x, y, health):
    font = pygame.font.Font(None, 18)
    text_surface = font.render(str(health), True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (x + 17.5, y + 40)
    screen.blit(text_surface, text_rect)
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 35, 35), 2)
    pygame.draw.line(screen, (255, 0, 0), ((x + 35), y), (x, (y + 35)), 2)
    pygame.draw.line(screen, (255, 0, 0), (x, (y + 35)), ((x + 35), y), 2)
    return pygame

def basic_bullet(pygame, screen, x, y, r):
    pygame.draw.circle(screen, (0,0,255), (x,y), r)
    return pygame



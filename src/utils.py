import pygame
from global_vars import Screen, Color

def perc_heigth(perc):
    return (Screen.SCREEN_HEIGTH * perc/100)

def perc_width(perc):
    return (Screen.SCREEN_WIDTH * perc/100)

def setup_game():

    pygame.init()

    screen = pygame.display.set_mode([
        Screen.SCREEN_WIDTH, Screen.SCREEN_HEIGTH
    ])

    pygame.display.set_caption('Snake AI')
    myfont = pygame.font.SysFont("times new roman", 24)
    
    return screen, myfont

def update_score_text(screen, myfont, msg):
        # Score Text
        score_surface = myfont.render(msg, True, Color.DARKGREEN)
        score_rect = score_surface.get_rect(
            topleft=(perc_width(3), perc_heigth(1))
        )
        screen.blit(score_surface, score_rect)

def update_highest_score_text(screen, myfont, msg):
        # Highest Score Text
        highest_score_surface = myfont.render(msg, True, Color.DARKGREEN)
        highest_score_rect = highest_score_surface.get_rect(
            topleft=(perc_width(65), perc_heigth(1))
        )
        screen.blit(highest_score_surface, highest_score_rect)


def update_epoch_text(screen, myfont, msg):
        # EPoch Text and Trainging time
        epoch_surface = myfont.render(msg, True, Color.YELLOW)
        epoch_rect = epoch_surface.get_rect(
            bottomleft=(perc_width(20), perc_heigth(98))
        )
        screen.blit(epoch_surface, epoch_rect)
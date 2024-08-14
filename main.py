import pygame
import sys
from game import Game

pygame.init()

FPS = 60

WHITE = (255, 255, 255)
DARK_GREEN = (0, 100, 0)
BUTTON_COLOR = (200, 0, 0)
BUTTON_HOVER_COLOR = (150, 0, 0)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Tycoon")

clock = pygame.time.Clock()

BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
BUTTON_X = screen.get_width() - BUTTON_WIDTH - 20
BUTTON_Y = screen.get_height() - BUTTON_HEIGHT - 20
button_rect = pygame.Rect(BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)

def draw_pass_button(surface):
    mouse_pos = pygame.mouse.get_pos()
    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(surface, BUTTON_HOVER_COLOR, button_rect)
    else:
        pygame.draw.rect(surface, BUTTON_COLOR, button_rect)

    font = pygame.font.SysFont(None, 36)
    text = font.render("Pass", True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)
    surface.blit(text, text_rect)

def main():
    game = Game(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    game.pass_turn()
                else:
                    game.handle_click(event.pos)

        if game.current_player != 'player':
            game.play_turn()

        screen.fill(DARK_GREEN)
        game.draw_cards()
        draw_pass_button(screen) 
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

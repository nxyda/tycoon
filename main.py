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

def draw_button(surface, rect, color, hover_color, text):
    mouse_pos = pygame.mouse.get_pos()
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(surface, hover_color, rect)
    else:
        pygame.draw.rect(surface, color, rect)

    font = pygame.font.SysFont(None, 36)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def main():
    game = Game(screen)

    screen_width, screen_height = screen.get_size()
    BUTTON_WIDTH = 150
    BUTTON_HEIGHT = 50

    pass_button_rect = pygame.Rect(screen_width - BUTTON_WIDTH - 20, screen_height - BUTTON_HEIGHT - 20, BUTTON_WIDTH, BUTTON_HEIGHT)
    accept_button_rect = pygame.Rect(20, screen_height - BUTTON_HEIGHT - 20, BUTTON_WIDTH, BUTTON_HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pass_button_rect.collidepoint(event.pos):
                    game.pass_turn()
                elif accept_button_rect.collidepoint(event.pos):
                    game.handle_button_click(event.pos)
                else:
                    game.handle_click(event.pos)

        if game.animation.card_moving:
            game.animation.move_card()

        if game.current_player != 'player':
            game.play_turn()

        screen.fill(DARK_GREEN)
        game.draw_cards()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

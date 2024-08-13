import pygame
import sys
from game import Game

pygame.init()

FPS = 60

WHITE = (255, 255, 255)
DARK_GREEN = (0, 100, 0)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Tycoon")

clock = pygame.time.Clock()

def main():
    game = Game(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(event.pos)


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

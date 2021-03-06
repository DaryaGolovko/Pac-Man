import pygame
from game import Game, DB

WIDTH = 800
HEIGHT = 576
FPS = 60


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PAC-MAN")
    clock = pygame.time.Clock()

    game = Game()

    DB.draw_field()

    running = True
    while running:
        running = game.process_events()
        game.run_logic()
        game.display_frame(screen)
        clock.tick(FPS)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()

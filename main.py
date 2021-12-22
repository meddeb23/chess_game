import pygame
from gameGraphic import GameGraphics
pygame.init()

# Define some colors
BLACK = (125, 125, 125)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FPS = 60


class GameState():
    def __init__(self) -> None:
        self.state = [
            ["bR", "bN", "bB", "bQ", "bk", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wk", "wB", "wN", "wR"],
        ]
        self.selectedSq = None
        self.playerSelections = []  # track the user's squar selection history
        self.isWhiteTurn = True


def main():
    gameGraphic = GameGraphics()
    gameState = GameState()
    isRunning = True
    clock = pygame.time.Clock()

    while isRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                sqCoord = gameGraphic.getPieceIndex(pygame.mouse.get_pos())
                if sqCoord != None:
                    print(
                        f"Selected piece: {gameState.state[sqCoord[0]][sqCoord[1]]}, coord ({sqCoord[0]},{sqCoord[1]})")

        gameGraphic.screen.fill(WHITE)
        gameGraphic.render(gameState.state)
        # board_surface = drawSquars(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


main()

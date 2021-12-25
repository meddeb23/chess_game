import pygame

from gameGraphic import GameGraphics
from gameState import GameState
pygame.init()

# Define some colors
BLACK = (125, 125, 125)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FPS = 60


def main():
    gameGraphic = GameGraphics()
    gameState = GameState()
    isRunning = True
    clock = pygame.time.Clock()

    while isRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                sqCoord = gameGraphic.getPieceIndex(pygame.mouse.get_pos())
                if sqCoord != None:
                    gameState.selectPiece(sqCoord)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    gameState.undoMove()
        gameGraphic.screen.fill(WHITE)
        gameGraphic.render(gameState.state, gameState.selectedSq)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


main()

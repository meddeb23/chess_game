import pygame

from gameGraphic import GameGraphics
from gameState import GameState
from components.button import Button
from components.startMenu import StartMenu
from components.text import Text

pygame.init()

# Define some colors
BLACK = (125, 125, 125)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FPS = 60


startMenu = StartMenu(title="Start Menu", dimension=(800, 500))


def main():
    gameGraphic = GameGraphics()
    gameState = GameState()
    isRunning = True
    clock = pygame.time.Clock()
    playGame = True
    while isRunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if playGame:
                    sqCoord = gameGraphic.getPieceIndex(pygame.mouse.get_pos())
                    if sqCoord != None:
                        gameState.selectPiece(sqCoord)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    if playGame:
                        gameState.undoMove()

        gameGraphic.screen.fill(WHITE)
        # pawnSq = gameState.checkPawnPromotion()
        # if pawnSq:
        #     print("Pawn promotion graphic handler")
        #     gameGraphic.promotionListRender()
        if playGame:
            gameGraphic.render(gameState.state, gameState.selectedSq)
        else:
            startMenu.render(gameGraphic.screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


main()

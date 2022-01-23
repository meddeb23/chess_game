import pygame

from gameGraphic import GameGraphics
from gameState import GameState
import ChessAi

pygame.init()

# Define some colors
BLACK = (125, 125, 125)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FPS = 60
DEPTH = 2


def main():
    gameGraphic = GameGraphics()
    gameState = GameState()
    isRunning = True
    clock = pygame.time.Clock()
    player_one = True  # for white : True => Human , False => AI
    player_two = False  # for black : True => Human , False => AI
    move_undone = False
    move_made = False

    while isRunning:
        human_turn = (gameState.isWhiteTurn and player_one) or (not gameState.isWhiteTurn and player_two)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not gameState.isgameover and human_turn:
                    sqCoord = gameGraphic.getPieceIndex(pygame.mouse.get_pos())
                    if sqCoord != None:
                        gameState.selectPiece(sqCoord)
                        move_made = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    gameState.undoMove()
                    move_made = True
                    move_undone = True

        # AI
        if not gameState.isgameover and not human_turn and not move_undone:
            aimove = ChessAi.getBestMove(gameState, gameState.getAllPossibleValidMoves(gameState.isWhiteTurn))
            if aimove is None:
                aimove = ChessAi.getRandomMove(gameState.getAllPossibleValidMoves(gameState.isWhiteTurn))
            gameState.makeMove(aimove)
            move_made = True

        if move_made:
            move_made = False
            move_undone = False

        if gameState.checkmate:
            gameState.isgameover = True
        if gameState.stalemate:
            gameState.isgameover = True

        gameGraphic.screen.fill(WHITE)
        # pawnSq = gameState.checkPawnPromotion()
        # if pawnSq:
        #     print("Pawn promotion graphic handler")
        #     gameGraphic.promotionListRender()
        gameGraphic.render(gameState.state, gameState.selectedSq)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


main()

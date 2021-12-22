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
        self.logs = []

    def selectPiece(self, coord):
        player = ["b", "w"][self.isWhiteTurn]
        selectedPiece = self.state[coord[0]][coord[1]]
        print(
            f"""----------------------
    Player: {player}
    Selected piece: {selectedPiece}
    Coord ({coord[0]},{coord[1]})
----------------------""")
        if len(self.playerSelections) == 0:
            if selectedPiece[0] == player:
                self.selectedSq = coord
                self.playerSelections.append(coord)
        else:
            if selectedPiece == "--":
                self.state[coord[0]][coord[1]
                                     ] = self.state[self.selectedSq[0]][self.selectedSq[1]]
                self.state[self.selectedSq[0]][self.selectedSq[1]] = "--"
                self.selectedSq = None
                self.playerSelections.pop()
                self.isWhiteTurn = not self.isWhiteTurn
            elif selectedPiece == self.state[self.selectedSq[0]][self.selectedSq[1]]:
                self.selectedSq = None
                self.playerSelections.pop()


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
                    gameState.selectPiece(sqCoord)

        gameGraphic.screen.fill(WHITE)
        gameGraphic.render(gameState.state, gameState.selectedSq)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


main()

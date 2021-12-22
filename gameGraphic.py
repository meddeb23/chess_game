import pygame


class GameGraphics():
    def __init__(self, boardDimension=8, caption="Chess Game", screenHeight=500, screenWidth=800, ) -> None:
        self.DIMENSION = boardDimension  # number of squars
        self.HEIGHT = screenHeight
        self.WIDTH = screenWidth
        # Dimiension of a Squar
        self.SQ_SIZE = min(screenHeight, screenWidth) // boardDimension
        self.selectedSq = None
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(caption)

    def __drawSquars(self):
        BLACK = (125, 125, 125)
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)
        boardSize = self.SQ_SIZE * self.DIMENSION
        temp_surface = pygame.Surface((boardSize, boardSize))
        colors = [WHITE, BLACK]
        for r in range(self.DIMENSION):
            for c in range(self.DIMENSION):
                color = colors[(r+c) % 2]
                if self.selectedSq == (r, c):
                    color = RED
                squar = pygame.Surface((self.SQ_SIZE, self.SQ_SIZE))
                squar.fill(color)
                temp_surface.blit(squar, (r*self.SQ_SIZE, c*self.SQ_SIZE))
        return temp_surface

    def __loadImages(self):
        piecesImages = {}
        piecesList = ["bB", "bk", "bN", "bp", "bQ",
                      "bR", "wB", "wk", "wN", "wp", "wQ", "wR"]
        for i in piecesList:
            piecesImages[i] = pygame.image.load(
                f"./images/{i}.png").convert_alpha()

        return piecesImages

    def __drawPieces(self, screen, gameState):
        piecesImage = self.__loadImages()
        boardSize = self.SQ_SIZE * self.DIMENSION
        # temp_surface.fill(WHITE)
        for r in range(self.DIMENSION):
            for c in range(self.DIMENSION):
                piece = gameState[r][c]
                if piece != "--":
                    screen.blit(
                        piecesImage[piece],
                        (c*self.SQ_SIZE, r*self.SQ_SIZE)
                    )
        return screen

    def getPieceIndex(self, coord):
        (x, y) = coord
        if x < self.DIMENSION * self.SQ_SIZE and y < self.DIMENSION * self.SQ_SIZE:
            return (y // self.SQ_SIZE, x // self.SQ_SIZE)
        return None

    def render(self, gameState):
        boardSurface = self.__drawSquars()
        boardSurface = self.__drawPieces(boardSurface, gameState)
        self.screen.blit(boardSurface, (0, 0))

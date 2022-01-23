import pygame
from components.menus.endGameMenu import EndGameMenu

from gameState import GameState
from styles.colors import Colors

import ChessAi


class GameScreen():
    def __init__(self, game, boardDimension=8, screenHeight=500, screenWidth=800, ) -> None:
        self.DIMENSION = boardDimension  # number of squars
        self.WIDTH, self.HEIGHT = screenWidth, screenHeight
        # Dimiension of a Squar
        self.SQ_SIZE = min(screenHeight, screenWidth) // boardDimension
        self.screen = game.screen
        self.selectedPiece = ()
        self.gameState = GameState()
        self.gameOverMenu = EndGameMenu(
            game, "Game Over", (game.WIDTH, game.HEIGHT), [self.restartGame, game.setMainMenu])
        self.layers = []
        self.player_one = True  # for white : True => Human , False => AI
        self.player_two = False  # for black : True => Human , False => AI
        self.move_undone = False
        self.move_made = False
        self.DEPTH = 2

    def __drawSquars(self, selectedSq):
        boardSize = self.SQ_SIZE * self.DIMENSION
        temp_surface = pygame.Surface((boardSize, boardSize))
        colors = [Colors.LIGHT, Colors.GREEN]
        for r in range(self.DIMENSION):
            for c in range(self.DIMENSION):
                color = colors[(r+c) % 2]
                if selectedSq == (c, r):
                    color = Colors.RED
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

    def __drawPieces(self, screen):
        piecesImage = self.__loadImages()
        for r in range(self.DIMENSION):
            for c in range(self.DIMENSION):
                piece = self.gameState.state[r][c]
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

    def restartGame(self):
        self.gameState = GameState()
        self.layers = []

    def render(self):

        if not self.gameState.isgameover and not self.human_turn and not self.move_undone:
            aimove = ChessAi.getBestMove(
                self.gameState, self.gameState.getAllPossibleValidMoves(self.gameState.isWhiteTurn))
            if aimove is None:
                aimove = ChessAi.getRandomMove(
                    self.gameState.getAllPossibleValidMoves(self.gameState.isWhiteTurn))
            self.gameState.makeMove(aimove)
            move_made = True

        if move_made:
            move_made = False
            move_undone = False

        boardSurface = self.__drawSquars(self.selectedPiece)
        boardSurface = self.__drawPieces(boardSurface)
        self.screen.blit(boardSurface, (0, 0))
        for layer, pos in self.layers:
            # layer.render(self.screen)
            layer(self.screen)

    def isGameOver(self):
        return not self.gameState.checkmate and not self.gameState.stalemate

    def isHumainTurn(self):
        return (self.gameState.isWhiteTurn and self.player_one) or (not self.gameState.isWhiteTurn and self.player_two)

    def eventHandler(self, event):
        if self.gameState.checkmate:
            self.layers.append((self.gameOverMenu.render, (100, 100)))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.isGameOver() and self.isHumainTurn():
                sqCoord = self.getPieceIndex(pygame.mouse.get_pos())
                if sqCoord != None:
                    self.selectedPiece = self.gameState.selectPiece(sqCoord)
                    self.move_made = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                if self.isGameOver():
                    self.gameState.undoMove()
                    self.move_made = True
                    self.move_undone = True
        # pawnSq = self.gameState.checkPawnPromotion()
        # if pawnSq:
        #     print("Pawn promotion graphic handler")
        #     self.promotionListRender()

    def promotionListRender(self):
        temp_surface = pygame.Surface((100, 100))
        temp_surface.fill((255, 0, 0))
        self.screen.blit(temp_surface, (self.WIDTH - 100, 0))

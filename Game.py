import pygame

from gameGraphic import GameGraphics
from components.menus.startMenu import StartMenu
from styles.colors import Colors


class Game:
    def __init__(self, caption="Chess Game", screenHeight=500, screenWidth=800, FPS=60) -> None:
        self.WIDTH, self.HEIGHT = screenWidth, screenHeight
        """
            Pygame setup
        """
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(caption)
        """
            game settings
        """
        self.isRunning = True
        self.FPS = FPS

        """
            Screens
        """
        self.mainMenu = StartMenu(
            self, title="Chess game", dimension=(self.WIDTH, self.HEIGHT))
        self.gameGraphic = GameGraphics(self, )
        self.currentScreen = self.mainMenu

    """
        Close Game
    """

    def close(self):
        self.isRunning = False
    """
        Start new Game
    """

    def startGame(self):
        self.currentScreen = self.gameGraphic

    """
        render Graphics
    """

    def render(self):
        self.screen.fill(Colors.DARK)
        self.currentScreen.render()

    """
        main method
    """

    def main(self):
        clock = pygame.time.Clock()
        while self.isRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.isRunning = False
                else:
                    self.currentScreen.eventHandler(event)
            self.render()
            pygame.display.flip()
            clock.tick(self.FPS)

        pygame.quit()
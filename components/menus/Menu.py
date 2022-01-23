from styles.colors import Colors
from typing import Text


class Menu:
    def __init__(self, game, title, dimension) -> None:
        self.game = game
        self.screen = game.screen
        self.MID_WIDTH, self.MID_HIGHT = dimension[0]//2, dimension[1]//2
        self.title = Text(title, color=Colors.LIGHT, fontSize=50)

    def eventHandler(self, event):
        pass

    def render(self) -> None:
        pass

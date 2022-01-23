from tkinter import Menu
from components.text import Text
from components.button import Button
from styles.colors import Colors


class EndGameMenu(Menu):
    def __init__(self, game, title, dimension) -> None:
        super().__init__(game, title, dimension)
        self.listItmes = [
            Button(130, 160, "start new game", color=Colors.LIGHT,
                   size=20, action=game.startGame),
            Button(130, 220, "settings", color=Colors.LIGHT,
                   size=20, action=lambda: print("Setting")),
            Button(130, 280, "Quit game", color=Colors.LIGHT,
                   size=20, action=game.close)
        ]

    def render(self) -> None:
        self.title.render(self.screen, 200, 50)
        for item in self.listItmes:
            item.render(self.screen)

    def render(self, screen) -> None:
        self.title.render(screen, 200, 50)
        for item in self.listItmes:
            item.render(screen)

from components.text import Text
from components.button import Button
from styles.colors import Colors


class StartMenu():
    def __init__(self, game, title, dimension) -> None:
        self.game = game
        self.screen = game.screen
        self.MID_WIDTH, self.MID_HIGHT = dimension[0]//2, dimension[1]//2
        self.title = Text(title, color=Colors.LIGHT, fontSize=50)

        self.listItmes = [
            Button(130, 160, "start new game", color=Colors.LIGHT,
                   size=20, action=game.startGame),
            Button(130, 220, "settings", color=Colors.LIGHT,
                   size=20, action=lambda: print("Setting")),
            Button(130, 280, "Quit game", color=Colors.LIGHT,
                   size=20, action=game.close)
        ]

    def eventHandler(self, event):
        pass

    def render(self) -> None:
        self.title.render(self.screen, 200, 50)
        for item in self.listItmes:
            item.render(self.screen)

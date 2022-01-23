import pygame
from components.menus.Menu import Menu
from components.text import Text
from components.button import Button
from styles.colors import Colors


class EndGameMenu(Menu):
    def __init__(self, game, title, dimension, actions=[]) -> None:
        super().__init__(game, title, dimension)
        self.Width, self.height = (300, 300)
        self.title = Text(title, color=Colors.LIGHT, fontSize=30)
        self.listItmes = [
            Button(50, 130, "start new game", color=Colors.LIGHT,
                   size=20, action=actions[0]),
            Button(50, 170, "Quit game", color=Colors.LIGHT,
                   size=20, action=actions[1])
        ]

    def render(self) -> None:
        self.title.render(self.screen, 200, 50)
        for item in self.listItmes:
            item.render(self.screen)

    def render(self, screen) -> None:
        temp_surface = pygame.Surface((self.Width, self.height))
        temp_surface.fill(Colors.RED)
        self.title.render(temp_surface, 100, 50)
        for item in self.listItmes:
            item.render(temp_surface, (self.MID_WIDTH - self.Width //
                                       2, self.MID_HIGHT - self.height//2))
        screen.blit(temp_surface, (self.MID_WIDTH - self.Width //
                    2, self.MID_HIGHT - self.height//2))

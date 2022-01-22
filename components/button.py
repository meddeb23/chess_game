from pygame import font, mouse
from components.text import Text


class Button:
    def __init__(self, x, y, text, size=40, color=(0, 0, 0), action=lambda: print("button Clicked")) -> None:
        self.font = font.Font("fonts/Roboto-Medium.ttf", size)
        # self.titleSurface = self.font.render(text, False, color)
        self.titleSurface = Text(
            text, color, size, "fonts/Roboto-Medium.ttf").getSurface()
        self.titleRect = self.titleSurface.get_rect(topleft=(x, y))
        self.clicked = False
        self.action = action

    def render(self, surface):
        pos = mouse.get_pos()

        if self.titleRect.collidepoint(pos):
            if mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.action()
            if mouse.get_pressed()[0] == 0:
                self.clicked = False

        surface.blit(self.titleSurface, self.titleRect)

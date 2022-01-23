from pygame import font, mouse, image, transform
from components.text import Text


class MenuButton:
    def __init__(self) -> None:
        pass


class Button:
    def __init__(self, x, y, text, size=40, color=(0, 0, 0), action=lambda: print("button Clicked")) -> None:
        self.x, self.y = x, y
        self.font = font.Font("fonts/Roboto-Medium.ttf", size)
        # self.titleSurface = self.font.render(text, False, color)
        self.titleSurface = Text(
            text, color, size, "fonts/Roboto-Medium.ttf").getSurface()
        self.titleRect = self.titleSurface.get_rect(topleft=(x, y))
        self.clicked = False
        self.action = action
        self.hover = False
        self.listStyle = image.load(
            f"./images/right-arrow.png").convert_alpha()
        self.listStyle = transform.scale(self.listStyle, (13, 13))

    def render(self, surface):
        pos = mouse.get_pos()

        if self.titleRect.collidepoint(pos):
            surface.blit(self.listStyle, (self.x - 20, self.y + 7))
            if mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                self.action()
            if mouse.get_pressed()[0] == 0:
                self.clicked = False

        surface.blit(self.titleSurface, self.titleRect)

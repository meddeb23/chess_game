from pygame import font


class Text:
    def __init__(self, text, color=(0, 0, 0), fontSize=40, fontFamily=None) -> None:
        self.font = font.Font("fonts/Roboto-Medium.ttf", fontSize)
        self.title = self.font.render(text, False, color)

    def getSurface(self):
        return self.title

    def render(self, screen, x, y):
        screen.blit(self.title, ((x) - (self.title.get_width() // 2), y))

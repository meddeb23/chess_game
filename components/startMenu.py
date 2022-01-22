from components.text import Text
from components.button import Button


class StartMenu:
    def __init__(self, title, dimension) -> None:
        self.MID_WIDTH, self.MID_HIGHT = dimension[0]/2, dimension[1]/2
        self.title = Text(title).getSurface()
        self.listItmes = [Button(80, 120, "Start game", size=20, action=lambda: print("start Game")), Button(
            80, 160, "exit", size=20, action=lambda: print("Exit game"))]

    def render(self, screen) -> None:
        screen.blit(
            self.title, ((self.WIDTH//2) - (self.title.get_width() // 2), 50))
        for i in self.listItmes:
            i.render(screen)

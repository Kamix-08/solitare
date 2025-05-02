from .Menu import Menu
from .Renderer import AsciiText, Renderer

class Scene:
    def __init__(self) -> None:
        self.content:list[str|Menu|AsciiText] = []
        self.menus:list[Menu] = []

    def __iadd__(self, element:str|Menu|AsciiText):
        self.content.append(element)
        if type(element) == Menu:
            self.menus.append(element)
        return self

    def __str__(self) -> str:
        res:str = Renderer.get_clear()

        for element in self.content:
            res += str(element)

        return res
    
    def start(self) -> None:
        self.start_menus()

    def start_menus(self) -> None:
        for menu in self.menus:
            menu.start()
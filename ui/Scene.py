from .Menu import Menu
from .Renderer import AsciiText, Button, Renderer

ALLOWED = str|Menu|AsciiText|Button

class Scene:
    def __init__(self) -> None:
        self.content:list[ALLOWED] = []
        self.menus:list[Menu] = []

    def __iadd__(self, element:ALLOWED):
        if type(element) == str:
            element += '\n'

        elif type(element) == Menu:
            self.content.append('\n')
            self.menus.append(element)

        self.content.append(element)
            
        return self

    def __str__(self) -> str:
        res:str = Renderer.get_clear()
        # res:str = ""

        for element in self.content:
            res += str(element)

        return res
    
    def start(self) -> None:
        self.start_menus()

    def stop(self) -> None:
        self.stop_menus()

    def start_menus(self) -> None:
        for menu in self.menus:
            menu.start()

    def stop_menus(self) -> None:
        for menu in self.menus:
            menu.stop()
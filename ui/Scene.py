from .Menu import Menu
from .Renderer import AsciiText, Renderer

class Scene:
    def __init__(self) -> None:
        self.content:list[str|Menu|AsciiText] = []

    def __iadd__(self, element:str|Menu|AsciiText):
        self.content.append(element)
        return self

    def __str__(self) -> str:
        res:str = Renderer.get_clear()

        for element in self.content:
            res += str(element)

        return res
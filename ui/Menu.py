from .InputHandler import InputHandler, keyboard, Callable, KeyLike
from .Colors import Colors

class Menu:
    def __init__(self, update:Callable, highlight:str|tuple[int, int, int], text:list[tuple[str, Callable]], moving:list[KeyLike|None], sumbit:KeyLike = keyboard.Key.enter, cancel:tuple[KeyLike, Callable]|None = None) -> None:
        assert len(text) != 0
        assert len(moving) == 2

        self.idx:int = 0
        self.color:str|tuple[int, int, int] = highlight
        self.options:list[tuple[str, Callable]] = text
        self.update:Callable = update

        self.ih:InputHandler = InputHandler()
        self.ih.add_list({
            moving[0]: lambda: self.change_selection(-1),
            moving[1]: lambda: self.change_selection( 1),
            sumbit:    lambda: self.sumbit()
        })

        if cancel is not None:
            self.ih.add(cancel[0], lambda: self.call(cancel[1]))

        self.ih.start()

    def __str__(self) -> str:
        res:str = ""
        
        for i, (text, _) in enumerate(self.options):
            if i == self.idx:
                res += Colors.get_color(self.color)

            res += text + '\n'

            if i == self.idx:
                res += Colors.get_prev_color()

        return res

    def change_selection(self, change:int) -> None:
        self.idx = (self.idx + change) % len(self.options)
        self.update()

    def call(self, callback:Callable) -> None:
        self.ih.stop()
        callback()

    def sumbit(self) -> None:
        self.call(self.options[self.idx][1])
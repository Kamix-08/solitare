from .InputHandler import InputHandler, keyboard, Callable
from .Colors import Colors

class Menu:
    def update(self):
        for i, (text, _) in enumerate(self.options):
            if i == self.idx:
                Colors.set_color(self.color)

            print(text)

            if i == self.idx:
                Colors.prev_color()

    def change_selection(self, change:int):
        self.idx = (self.idx + change) % len(self.options)
        self.update()

    def call(self, callback:Callable):
        self.ih.stop()
        callback()

    def sumbit(self):
        self.call(self.options[self.idx])

    def __init__(self, highlight:str|tuple[int, int, int], text:list[tuple[str, Callable]], moving:list[keyboard.KeyCode|str|None], sumbit:keyboard.KeyCode|str = keyboard.Key.enter, cancel:tuple[keyboard.KeyCode|str|None, Callable|None] = (keyboard.Key.esc, None)):
        assert len(text) != 0
        assert len(moving) == 2

        self.idx:int = 0
        self.color:str|tuple[int, int, int] = highlight
        self.options:list[tuple[str, Callable]] = text

        self.ih:InputHandler = InputHandler()
        self.ih.add_list({
            moving[0]: lambda: self.change_selection(-1),
            moving[1]: lambda: self.change_selection( 1),
            sumbit:    lambda: self.sumbit()
        })

        if cancel[0] is not None and cancel[1] is not None:
            self.ih.add(cancel[0], lambda: self.cancel(cancel[1]))

        self.ih.start()
        self.update()
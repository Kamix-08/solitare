from .InputHandler import InputHandler, keyboard, Callable, KeyLike
from .Colors import Colors
from .Renderer import Button
from typing import Any

class BaseMenu:
    def __init__(self, 
            update:Callable, 
            highlight:str|tuple[int,int,int], 
            text:list[tuple[Any,Callable]], 
            moving:list[KeyLike|None], 
            sumbit:KeyLike=keyboard.Key.enter, 
            cancel:tuple[KeyLike,Callable]|None=None,
            other:dict[KeyLike,Callable]|None=None) -> None:
                
        self.idx:int = 0
        self.options:list[tuple[Any,Callable]] = text
        self.update:Callable = update
        self.color:str|tuple[int, int, int] = highlight

        self.ih:InputHandler = InputHandler()
        self.ih.add_list({
            moving[0]: lambda: self.change_selection(-1),
            moving[1]: lambda: self.change_selection( 1),
            sumbit:    lambda: self.submit()
        })
        
        if other is not None:
            self.ih.add_list(other)

        if cancel is not None:
            self.ih.add(cancel[0], lambda: self.call(cancel[1]))

    def change_selection(self, change:int) -> None:
        self.idx = (self.idx + change) % len(self.options)
        self.update()

    def call(self, callback:Callable) -> None:
        callback()
        self.ih.stop()

    def submit(self) -> None:
        self.call(self.options[self.idx][1])

    def start(self) -> None:
        self.ih.start()

    def stop(self) -> None:
        self.ih.stop()

class Menu(BaseMenu):
    def __init__(self, 
            update:Callable, 
            highlight:str|tuple[int, int, int], 
            text:list[tuple[str, Callable]], 
            moving:tuple[KeyLike,KeyLike] = (keyboard.Key.up, keyboard.Key.down), 
            sumbit:KeyLike = keyboard.Key.enter, 
            cancel:tuple[KeyLike, Callable]|None = None) -> None:
        
        assert len(text) != 0

        self.buttons:list[Button] = Button.get_buttons([x.strip() for x, _ in text])
        super().__init__(update, highlight, [(('\n' if t[0] == '\n' else '') + str(self.buttons[i]) + ('\n' if t[-1] == '\n' else ''), f) for i, (t, f) in enumerate(text)], [x for x in moving], sumbit, cancel)

    def __str__(self) -> str:
        res:str = ""
        
        for i, (text, _) in enumerate(self.options):
            if i == self.idx:
                res += Colors.get_color(self.color)

            res += text + '\n'

            if i == self.idx:
                res += Colors.get_prev_color()

        return res

class HorizontalMenu(BaseMenu):
    def __init__(self, 
            update:Callable, 
            highlight:tuple[str|tuple[int,int,int], str|tuple[int,int,int]],
            get_structure:Callable[[], list[int]],
            execute:Callable[[tuple[int,int]], Any],
            moving:list[KeyLike] = [keyboard.Key.left, keyboard.Key.right, keyboard.Key.up, keyboard.Key.down], 
            sumbit:KeyLike = keyboard.Key.enter,
            cancel:tuple[KeyLike,Callable]|None = None) -> None:

        assert len(moving) == 4

        super().__init__(update, highlight[0], [], moving[:2], sumbit, other={
            moving[2]: lambda: self.change_secondary_selection(-1),
            moving[3]: lambda: self.change_secondary_selection( 1)
        })

        self.get_struct:Callable[[], list[int]] = get_structure
        self.execute:Callable[[tuple[int,int]], Any] = execute
        self.idxs:list[int] = [0] * len(self.get_struct())
        self.color_secondary:str|tuple[int,int,int] = highlight[1]

        if cancel is not None:
            self.ih.add(cancel[0], lambda: (cancel[1](), self.update()))

    def change_selection(self, change:int, update:bool = True) -> None:
        self.idx = (self.idx + change) % len(self.get_struct())

        if update:
            self.update()

    def change_secondary_selection(self, change:int) -> None:
        i1, i2 = self.get_highlight()
        n:int = self.get_struct()[i1]
        if n != 0: self.idxs[i1] = (i2 + change) % n
        self.update()

    def submit(self) -> None:
        self.execute(self.get_highlight())
        self.update()

    def get_highlight(self) -> tuple[int,int]:
        return (self.idx, self.idxs[self.idx])
from pynput import keyboard
from typing import Callable

Key = keyboard.Key|keyboard.KeyCode|None
KeyLike = Key|str

class InputHandler():
    def __init__(self) -> None:
        self.callbacks:dict[Key, list[Callable]] = {}
        self.listener:keyboard.Listener|None = None
        self.active:bool = False

    @staticmethod
    def call(callbacks:list[Callable]) -> None:
        for callback in callbacks:
            callback()

    def callback(self, key:Key) -> None:
        if key in self.callbacks:
            InputHandler.call(self.callbacks[key])

    def add(self, key:KeyLike, callback:Callable) -> None:
        parsed_key:Key = None

        if isinstance(key, str):
            parsed_key = keyboard.KeyCode.from_char(key)
        elif isinstance(key, (keyboard.Key, keyboard.KeyCode)):
            parsed_key = key

        if parsed_key not in self.callbacks:
            self.callbacks[parsed_key] = []
        self.callbacks[parsed_key].append(callback)

    def add_list(self, callbacks:dict[KeyLike|None, Callable]) -> None:
        for key, callback in callbacks.items():
            if key is not None:
                self.add(key, callback)

    def start(self) -> None:
        assert not self.active
        assert self.listener is None
        
        self.active = True
        self.listener = keyboard.Listener(on_release=self.callback)
        self.listener.start()
        self.listener.join()

    def stop(self) -> None:
        assert self.active
        assert self.listener is not None

        self.active = False
        self.listener.stop()
        self.listener = None
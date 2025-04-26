from pynput import keyboard
from typing import Callable

class InputHandler():
    def __init__(self):
        self.callbacks:dict[keyboard.KeyCode|str, list[Callable]] = {}
        self.listener:keyboard.Listener|None = None

    @staticmethod
    def call(callbacks:list[Callable]):
        for callback in callbacks:
            callback()

    def callback(self, key:keyboard.KeyCode|str):
        if key in self.callbacks:
            InputHandler.call(self.callbacks[key])
        elif hasattr(key, 'char') and key.char in self.callbacks:
            InputHandler.call(self.callbacks[key.char])

    def add(self, key:keyboard.KeyCode|str, callback:Callable):
        self.callbacks[key].append(callback)

    def add_list(self, callbacks:dict[keyboard.KeyCode|str, Callable]):
        for key, callback in callbacks:
            self.add(key, callback)

    def start(self):
        assert self.listener is None

        self.listener = keyboard.Listener(on_release=self.callback)
        self.listener.start()

    def stop(self):
        assert self.listener is not None

        self.listener.stop()
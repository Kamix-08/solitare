from .GameManager import GameManager

def init_game(mode:bool) -> GameManager:
    return GameManager(mode)
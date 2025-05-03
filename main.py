from game import __init__ as game_init
from game.scenes import *

from ui import __init__ as ui_init
from ui.Renderer import Renderer

def main() -> None:
    ui_init()
    use_scene(scene_main())
    gameManager = game_init(get_gamemode())

if __name__ == "__main__":
    main()
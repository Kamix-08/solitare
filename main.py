from game import __init__ as game_init

from ui import __init__ as ui_init
from ui.Renderer import Renderer, AsciiText
from ui.Scene import Scene
from ui.Colors import Colors
from ui.Menu import Menu

def main() -> None:
    ui_init()

    main_scene:Scene = Scene()

    main_scene += Colors.get_color('blue')
    main_scene += AsciiText("Solitare")
    main_scene += Colors.get_color('default')

    main_menu:Menu = Menu(
        update=lambda: print(main_scene), 
        highlight='green', 
        text=[('New Game', lambda: print("new game selected"))],
        moving=[None, None]
    )

    main_scene += main_menu

    print(main_scene)

    gameManager = game_init(True)

if __name__ == "__main__":
    main()
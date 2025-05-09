from game.init import init_game
from game.scenes import use_scene, scene_main, get_gamemode

from ui.init import init_ui

def main() -> None:
    init_ui()
    use_scene(scene_main())

    mode:bool|None = get_gamemode()
    if mode is None: return
    
    gameManager = init_game(mode)
    print(gameManager)
    gameManager.menu.start()

if __name__ == "__main__":
    main()
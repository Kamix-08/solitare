from game.init import init_game
from game.scenes import use_scene, scene_main, get_gamemode

from ui.init import init_ui
from ui.Renderer import Renderer

def main() -> None:
    init_ui()
    use_scene(scene_main())
    
    gameManager = init_game(get_gamemode())
    Renderer.clear()
    print(gameManager)

if __name__ == "__main__":
    main()
from ui.Scene import Scene
from ui.Renderer import AsciiText, Renderer
from ui.Menu import Menu
from ui.Colors import Colors
from game.init import init_game
import time

game_mode:bool|None = None
scenes:list[Scene] = []

def start(mode:bool) -> None:
    gameManager = init_game(mode)
    print(gameManager)
    gameManager.menu.start()

    use_scene(scene_end(
        gameManager.won, 
        gameManager.moves,
        time.time() - gameManager.time
    ))

def use_scene(scene:Scene) -> None:
    print(scene)
    scene.start()
    scenes.append(scene)

def exit_game() -> None:
    for scene in scenes:
        scene.stop()

def scene_main() -> Scene:
    scene:Scene = Scene()
    scene += AsciiText("Solitare", 'blue')

    menu:Menu = Menu(
        update=lambda: print(scene), 
        highlight='green', 
        text=[
            ('New Game', lambda: use_scene(scene_game_mode())),
            ('Info',     lambda: use_scene(scene_info())),
            ('\nExit',   lambda: exit_game())
        ]
    )

    scene += menu
    return scene

def scene_game_mode() -> Scene:
    scene:Scene = Scene()
    scene += AsciiText("Difficulty", 'blue')

    menu:Menu = Menu(
        update=lambda: print(scene),
        highlight='green',
        text=[
            ('Easy',   lambda: start(True)),
            ('Hard',   lambda: start(False)),
            ('\nBack', lambda: use_scene(scene_main()))
        ]
    )

    scene += menu
    return scene

def scene_info() -> Scene:
    scene:Scene = Scene()
    scene += AsciiText("Info", 'blue')

    scene += f"This solitare game has been made by Kamil Pawłowski ({Colors.get_color('cyan')}https://github.com/Kamix-08{Colors.get_prev_color()})."
    scene += "The program has been developed as a part of the Gigathon 2025 competition."
    scene += "\nThe game is a simple solitare game, featuring two difficulty modes:"
    scene += "Easy allows for drawing one card at a time, while hard only allows three cards at a time."

    menu:Menu = Menu(
        update=lambda: print(scene),
        highlight='green',
        text=[
            ('Back', lambda: use_scene(scene_main()))
        ]
    )

    scene += menu
    return scene

def scene_end(won:bool, moves:int, time:float) -> Scene:
    scene:Scene = Scene()
    scene += AsciiText("You won!" if won else "You lost...", 'blue' if won else 'red')

    scene += f"Moves: {moves}"
    scene += f"Time : {Renderer.format_seconds(time)}"

    menu:Menu = Menu(
        update=lambda: print(scene), 
        highlight='green',
        text=[
            ('Play Again',  lambda: use_scene(scene_game_mode())),
            ('Main Menu',   lambda: use_scene(scene_main())),
            ('\nExit',      lambda: exit_game())
        ]
    )

    scene += menu
    return scene
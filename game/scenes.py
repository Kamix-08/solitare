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
        mode,
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
            ('New Game',    lambda: use_scene(scene_game_mode())),
            ('Leaderboard', lambda: use_scene(scene_leaderboard())),
            ('Info',        lambda: use_scene(scene_info())),
            ('\nExit',      lambda: exit_game())
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

def scene_end(mode:bool, won:bool, moves:int, time:float) -> Scene:
    scene:Scene = Scene()
    scene += AsciiText("You won!" if won else "You lost...", 'blue' if won else 'red')

    scene += f"Mode : {"easy" if mode else "hard"}"
    scene += f"Moves: {moves}"
    scene += f"Time : {Renderer.format_seconds(time)}"

    menu:Menu = Menu(
        update=lambda: print(scene), 
        highlight='green',
        text=[
            ('Play Again',  lambda: use_scene(scene_game_mode())),
            ('Leaderboard', lambda: use_scene(scene_leaderboard(mode))),
            ('Main Menu',   lambda: use_scene(scene_main())),
            ('\nExit',      lambda: exit_game())
        ]
    )
    
    if won:
        with open('leaderboard.txt', 'a') as f:
            f.write(f"{'e' if mode else 'h'}{moves}\n")

    scene += menu
    return scene

def format_table(data:list[list[str]], headers:list[str]) -> list[str]:
    print(data, headers)
    assert all([len(x) == len(headers) for x in data])
    
    def get_line(elements:list[str]) -> str:
        return ' ' + ' | '.join(elements) + ' '
    
    def center(element:str, width:int) -> str:
        n:int = (width - len(element)) // 2
        return ' ' * n + element + ' ' * (width - n - len(element))
    
    widths:list[int] = [max([len(headers[i])] + [len(x[i]) for x in data]) for i in range(len(headers))]
    
    res:list[str] = [get_line([center(x, widths[i]) for i, x in enumerate(line)]) for line in [headers] + data]
    
    for i in range(len(res) - 1):
        res[i] += f"\n{'-' * len(res[i])}"
    
    return res

def scene_leaderboard(mode:bool|None = None) -> Scene:
    scene:Scene = Scene()
    scene += AsciiText("Leaderboard", 'blue')
    
    flag:str = 'e' if mode else 'h'
    
    with open('leaderboard.txt', 'r') as f:
        entries:list[str] = f.readlines()
    
    data:tuple[list[int],list[int]] = ([],[])
    
    def parse_entry(entry:str) -> tuple[int,bool]:
        return int(entry[1:]), entry[0] == 'h'
    
    for entry in entries:
        if mode is not None and entry[0] != flag:
            continue
        
        v, _i = parse_entry(entry)
        data[_i].append(v)
        
    for x in data:
        x.sort()
    
    table:list[list[str]] = []
    for i in range(max([len(x) for x in data])):
        line:list[str] = [f"{i+1}."]
        
        for x in data:
            if len(x) == 0 and mode is not None: continue
            line.append(str(x[i]) if i < len(x) else '-')
        
        table.append(line)
        
    for _line in format_table(table, ["#"] + (["Easy", "Hard"] if mode is None else ["Moves"])):
        scene += _line
        
    menu:Menu = Menu(
        update=lambda: print(scene),
        highlight='green',
        text=[
            ('Back', lambda: use_scene(scene_main()))
        ]
    )
    
    scene += menu
    return scene
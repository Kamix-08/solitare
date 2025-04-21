from game import __init__ as game_init
from ui import __init__ as ui_init

def main():
    renderer = ui_init()
    gameManager = game_init(True)

    renderer.ascii_print("lorem")

if __name__ == "__main__":
    main()
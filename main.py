from game.scenes import use_scene, scene_main

from ui.init import init_ui
from ui.Renderer import Renderer

import sys
import os

def main() -> None:
    init_ui()
    use_scene(scene_main())

if __name__ == "__main__":
    main()

    if os.name == 'nt':
        import msvcrt
        while msvcrt.kbhit():   # type: ignore[attr-defined]
            msvcrt.getch()      # type: ignore[attr-defined]
    else:
        import termios
        termios.tcflush(sys.stdin.fileno(), termios.TCIFLUSH)

    Renderer.clear()
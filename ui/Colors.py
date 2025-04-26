class Colors:
    FOREGROUND_COLORS:dict[str, str] = {
        "black": "\x1b[30m",
        "red": "\x1b[31m",
        "green": "\x1b[32m",
        "yellow": "\x1b[33m",
        "blue": "\x1b[34m",
        "magenta": "\x1b[35m",
        "cyan": "\x1b[36m",
        "white": "\x1b[37m",
        "default": "\x1b[39m",
        "clear": "\x1b[0m"
    }

    stack:list[str] = []

    @staticmethod
    def set_color(color:str|tuple[int, int, int], append:bool = True):
        esc_code:str = ""

        if type(color) == str:
            assert color in Colors.FOREGROUND_COLORS
            esc_code = Colors.FOREGROUND_COLORS[color]

        else:
            assert all([0 <= v <= 255 for v in color])
            esc_code = f"\x1b[38;2;{color[0]};{color[1]};{color[2]}m"

        print(esc_code, end='')
        if append:
            Colors.stack.append(esc_code)

    @staticmethod
    def prev_color():
        if len(Colors.stack < 2):
            print(Colors.FOREGROUND_COLORS['clear'], end='')
            return
        
        Colors.stack.pop()
        print(Colors.stack[-1], end='')

    @staticmethod
    def clear():
        print(Colors.FOREGROUND_COLORS['clear'], end='')
        Colors.stack = []
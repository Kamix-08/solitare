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
    def get_color(color:str|tuple[int, int, int]) -> str:
        if color == "":
            return ""
        
        esc_code:str = ""

        if type(color) == str:
            assert color in Colors.FOREGROUND_COLORS
            esc_code = Colors.FOREGROUND_COLORS[color]

        elif type(color) == tuple[int, int, int]:
            assert all([0 <= v <= 255 for v in color])
            esc_code = f"\x1b[38;2;{color[0]};{color[1]};{color[2]}m"

        return esc_code

    @staticmethod
    def set_color(color:str|tuple[int, int, int], append:bool = True) -> None:
        esc_code:str = Colors.get_color(color)
        print(esc_code, end='')
        if append:
            Colors.stack.append(esc_code)

    @staticmethod
    def get_prev_color(pop:bool = True) -> str:
        if len(Colors.stack) < 2:
            return Colors.get_color('clear')
        
        if pop:
            Colors.stack.pop()
            
        return Colors.stack[-1]

    @staticmethod
    def prev_color() -> None:
        print(Colors.get_prev_color(), end='')

    @staticmethod
    def clear() -> None:
        Colors.get_color('clear')
        Colors.stack = []
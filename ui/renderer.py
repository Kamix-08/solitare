from .Colors import Colors

class Renderer:
    ascii_font:dict[str,list[str]]|None = None

    @staticmethod
    def init_ascii_font() -> None:
        assert Renderer.ascii_font is None

        with open("./font.txt") as f:
            lines = [line[:-1] for line in f.readlines()]
            assert len(lines) > 0

        charset = lines[0]
        Renderer.ascii_font = dict[str, list[str]]()

        for i, char in enumerate(charset):
            char_lines = []
            max_chars = -1

            for j in range(6):
                temp_line = lines[i * 6 + j + 1]
                char_lines.append(temp_line)

                temp_line = temp_line.rstrip()
                if len(temp_line) > max_chars:
                    max_chars = len(temp_line)

            if char != ' ':
                char_lines = [(line[:max_chars] + ' ' * max(max_chars - len(line), 0)) for line in char_lines]
            Renderer.ascii_font[char] = char_lines

    @staticmethod
    def get_ascii_text(text:str) -> str:
        assert Renderer.ascii_font is not None
        res:str = ""

        for i in range(6):
            for char in text:
                res += Renderer.ascii_font[char][i]
            res += '\n'

        return res

    @staticmethod
    def get_clear() -> str:
        return "\x1b[2J\x1b[2H"

    @staticmethod
    def clear() -> None:
        print(Renderer.get_clear())

    @staticmethod
    def init() -> None:
        Renderer.init_ascii_font()

class AsciiText:
    def __init__(self, text:str, color:str|tuple[int,int,int] = "") -> None:
        self.text:str = text
        self.color:str|tuple[int,int,int] = color

    def __str__(self) -> str:
        return Colors.get_color(self.color) + Renderer.get_ascii_text(self.text) + Colors.get_prev_color()
    
class Button:
    PADDING_Y:int = 1

    def __init__(self, text:str, width:int) -> None:
        self.text:str = text
        self.width:int = width

    def __str__(self):
        l_pad:int = (self.width - len(self.text))//2
        line:str = '+' + '-' * self.width + '+\n'
        empty:str = ('|' + ' ' * self.width + '|\n') * Button.PADDING_Y

        return line + empty + '|' + ' ' * l_pad + self.text + ' ' * (self.width - len(self.text) - l_pad) + '|\n' + empty + line[:-1]
    
    @staticmethod
    def get_buttons(texts:list[str], pad:int=2) -> list["Button"]:
        max_len:int = max([len(x) for x in texts]) + 2 * pad
        return [Button(t, max_len) for t in texts]
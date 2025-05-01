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
    def __init__(self, text:str) -> None:
        self.text:str = text

    def __str__(self) -> str:
        return Renderer.get_ascii_text(self.text)
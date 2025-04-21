class Renderer:
    ascii_font:dict[str,list[str]]|None = None

    def init_ascii_font(self):
        assert self.ascii_font is None

        with open("./font.txt") as f:
            lines = [line[:-1] for line in f.readlines()]
            assert len(lines) > 0

        charset = lines[0]
        self.ascii_font = dict[str, list[str]]()

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
            self.ascii_font[char] = char_lines

    def __init__(self):
        self.init_ascii_font()

    def ascii_print(self, text:str):
        for i in range(6):
            for char in text:
                print(self.ascii_font[char][i], end='')
            print()
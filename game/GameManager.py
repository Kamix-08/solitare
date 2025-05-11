from .Pile import *
from ui.Menu import HorizontalMenu, keyboard
from ui.Renderer import Renderer

class GameManager:
    def init_cards(self) -> None:
        assert len(self.all_cards) == 0
        self.current_card = 0

        for suit in Suit:
            if suit == Suit.NONE: continue
            for value in Value:
                if value == Value.NONE: continue
                self.all_cards.append(Card(value, suit))

        random.shuffle(self.all_cards)

    def get_next_card(self) -> Card:
        assert len(self.all_cards) > 0
        assert self.current_card < len(self.all_cards)

        self.current_card += 1
        return self.all_cards[self.current_card - 1]

    def init_game_piles(self) -> None:
        assert len(self.game_piles) == 0

        for i in range(1, 8):
            current_pile = GamePile()
            current_pile.hidden = i - 1

            for _ in range(i):
                current_pile.add(self.get_next_card(), _force=True)

            self.game_piles.append(current_pile)

    def __init__(self, easy_mode:bool) -> None:
        self.all_cards:list[Card] = []
        self.game_piles:list[GamePile] = []
        self.final_piles:list[FinalPile] = []
        self.reserve_pile:tuple[ReservePile,GamePile]

        self.mode:bool = easy_mode
        self.won:bool = False
        self.escs:int = 0

        self.init_cards()
        self.init_piles(easy_mode)

        self.selected:tuple[int,int]|None = None
        self.menu:HorizontalMenu = HorizontalMenu(
            lambda: print(self),
            ('blue', 'magenta'),
            self.get_structure,
            lambda x: self.execute(x),
            other={
                keyboard.Key.esc: self.handle_esc,
                keyboard.Key.tab: self.solve
            }
        )

    def init_final_piles(self) -> None:
        assert len(self.final_piles) == 0

        for suit in Suit:
            if suit == Suit.NONE: continue
            self.final_piles.append(FinalPile(suit))

    def init_reserve_pile(self, mode:bool) -> None:
        target:GamePile = GamePile()
        self.reserve_pile = (ReservePile(mode, target), target)

        while self.current_card < len(self.all_cards):
            self.reserve_pile[0].add(self.get_next_card(), _force=True)

    def init_piles(self, mode:bool) -> None:
        self.init_game_piles()
        self.init_final_piles()
        self.init_reserve_pile(mode)

    def get_structure(self) -> list[int]:
        return [
            1 + int(len(self.reserve_pile[1]) != 0),
            *[len(pile) for pile in self.game_piles], # unpacking
            len(self.final_piles)
        ]
    
    def execute(self, choice:tuple[int,int]) -> None:
        i:int = choice[1]

        match choice[0]:
            case 0: # reserve
                if self.selected is not None: return # do nothing
                if len(self.reserve_pile[i]) == 0: return # do nothing
                if i == 0: # draw
                    for _ in range(1 if self.mode else max(1, min(3, len(self.reserve_pile[0]) - 1))):
                        self.move_card(-1, self.reserve_pile[0], self.reserve_pile[1], True)
                else: self.selected = choice # select
            case 8: # final
                if self.selected is None:
                    if len(self.final_piles[i]) != 0: self.selected = choice # select
                else:
                    self.move_selected(self.final_piles[i]) # move
            case _: # game
                i1:int = choice[0] - 1
                if i < self.game_piles[i1].hidden: 
                    self.selected = None
                    return # do nothing
                if self.selected is None and len(self.game_piles[i1]) != 0: self.selected = choice # select
                elif self.selected is not None:
                    self.move_selected(self.game_piles[i1]) # move

    def move_card(self, i:int, _from:Pile, _to:Pile, force:bool = False) -> bool:
        if len(_from) == 0: return False
        
        if not force:
            if len(_to) == 0 and not _to.can_add_to_empty(_from[i]):    return False
            if len(_to) != 0 and not _to.can_stack(_from[i], _to[-1]):  return False

        last:bool = _from[i] == _from[-1]
        
        _to.add(_from.pop(i), _force=force)

        _from.on_move(_removed=True)
        _to.on_move(_removed=False)

        if not last:
            self.move_card(i, _from, _to, force)

        if type(_to) != FinalPile:
            return True
        
        for pile in self.final_piles:
            if len(pile) == 0 or pile[-1].value != Value.KING:
                return True
            
        self.end()
        return True
    
    def move_selected(self, _to:Pile) -> bool:
        assert self.selected is not None
        i1, i2 = self.selected

        _from:Pile

        match i1:
            case 0: _from = self.reserve_pile[1]
            case 8: _from = self.final_piles[i2]
            case _: _from = self.game_piles[i1 - 1]

        res:bool = self.move_card(-1 if i1 == 0 or i1 == 8 else i2, _from, _to)
        if res: _from.hidden = min(_from.hidden, len(_from) - 1)

        self.menu.idxs[self.selected[0]] = 0
        self.selected = None

        return res
    
    def handle_esc(self) -> None:
        if self.selected is not None:
            self.selected = None
            self.escs = 0
            return
        
        self.escs += 1
        if self.escs >= 2:
            self.end(False)
        else:
            print("Press ESC again to exit...")

    def end(self, won:bool = True) -> None:
        self.won = won
        self.menu.stop()

    def solve(self) -> bool:
        for pile in self.game_piles:
            if pile.hidden > 0:
                return False
        
        self.end()
        return True
    
    def __str__(self) -> str:
        text:list[str] = []

        objects_unflattened:list[list[list[str]]] = []
        objects:list[list[str]] = []

        objects_unflattened.append([self.reserve_pile[0]._str(), self.reserve_pile[1]._str(3, outline=False)]) # reserve
        objects_unflattened += [[x._str()] for x in self.game_piles] # normal
        objects_unflattened.append([x._str() for x in self.final_piles]) # final

        def add_color(color:str|tuple[int,int,int], pos:tuple[int,int]) -> None:
            i1, i2 = pos

            def get_line(_line:str) -> str:
                code:str = Colors.get_color(color)
                return code + Colors.get_color('bold',False) + Colors.regex().sub(code, _line) + Colors.get_color('clear',False) + Colors.get_prev_color()

            match i1:
                case 0 | 8:
                    if i1 == 0 and i2 == 1:
                        for j in range(len(objects_unflattened[0][1]) - Card.HEIGHT - 2, len(objects_unflattened[0][1])):
                            _line = objects_unflattened[0][1][j]
                            objects_unflattened[0][1][j] = get_line(_line)
                    else:
                        for j, _line in enumerate(objects_unflattened[i1][i2]):
                            objects_unflattened[i1][i2][j] = get_line(_line)
                case _:
                    for j in range(i2*2, len(objects_unflattened[i1][0]) if i2 == len(self.game_piles[i1-1]) - 1 or len(self.game_piles[i1-1]) == 0 else (i2+1)*2):
                        _line = objects_unflattened[i1][0][j]
                        objects_unflattened[i1][0][j] = get_line(_line)

        if self.selected is not None: add_color(self.menu.color_secondary, self.selected)
        add_color(self.menu.color, self.menu.get_highlight())

        objects = [sum(arr, []) for arr in objects_unflattened] # flat down

        for n in range(max([len(x) for x in objects])):
            line:str = ""

            for i, obj in enumerate(objects):
                if i == 1 or i == len(objects) - 1:
                    line += ' ' * 6
                elif i != 0:
                    line += ' '

                if len(obj) <= n:
                    line += ' ' * (Card.WIDTH + 2)
                    continue

                line += obj[n]

            text.append(line)

        # return '\n'.join(text)
        return Renderer.get_clear() + '\n'.join(text)
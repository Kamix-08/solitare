from .Pile import *
from ui.Menu import HorizontalMenu
from ui.Renderer import Renderer
import random

class GameManager:
    all_cards:list[Card] = []
    game_piles:list[GamePile] = []
    final_piles:list[FinalPile] = []
    reserve_pile:tuple[ReservePile,GamePile]

    def init_cards(self) -> None:
        assert len(self.all_cards) == 0
        self.current_card = 0

        for suit in Suit:
            for value in Value:
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

    def init_final_piles(self) -> None:
        assert len(self.final_piles) == 0

        for suit in Suit:
            self.final_piles.append(FinalPile(suit))

    def init_reserve_pile(self, mode:bool) -> None:
        self.reserve_pile = (ReservePile(mode), GamePile())

        while self.current_card < len(self.all_cards):
            self.reserve_pile[0].add(self.get_next_card(), _force=True)

    def init_piles(self, mode:bool) -> None:
        self.init_game_piles()
        self.init_final_piles()
        self.init_reserve_pile(mode)

    def __init__(self, easy_mode:bool) -> None:
        self.mode:bool = easy_mode

        self.init_cards()
        self.init_piles(easy_mode)

        self.selected:tuple[int,int]|None = None
        self.menu:HorizontalMenu = HorizontalMenu(
            lambda: print(self),
            ('blue', 'magenta'),
            self.get_structure,
            lambda x: self.execute(x)
        )

    def get_structure(self) -> list[int]:
        return [
            len(self.reserve_pile),
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
                    for _ in range(1 if self.mode else 3):
                        self.move_card(-1, self.reserve_pile[0], self.reserve_pile[1], True)
                else: self.selected = choice # select
            case 8: # final
                if self.selected is None:
                    if len(self.final_piles[i]) == 0: return # do nothing
                    self.selected = choice # select
                else:
                    self.move_selected(self.final_piles[i]) # move
            case _: # game
                if i < self.game_piles[i].hidden: return # do nothing
                if self.selected is None: self.selected = choice # select
                else: self.game_piles[choice[0] - 1] # move

    def move_card(self, i:int, _from:Pile, _to:Pile, force:bool = False) -> bool:
        if len(_from) == 0: return False
        
        if not force:
            if len(_to) == 0 and not _to.can_add_to_empty(_from[i]): return False
            if not _to.can_stack(_from[i], _to[-1]): return False
        
        _to.add(_from.pop(i), _force=force)

        _from.on_move(_removed=True)
        _to.on_move(_removed=False)

        return True
    
    def move_selected(self, _to:Pile) -> bool:
        assert self.selected is not None

        _from:Pile

        match self.selected[0]:
            case 0: _from = self.reserve_pile[1]
            case 8: _from = self.final_piles[self.selected[1]]
            case _: _from = self.game_piles[self.selected[0] - 1]

        return self.move_card(-1 if self.selected[0] == 8 else self.selected[1], _from, _to)
    
    def __str__(self) -> str:
        print(f"highligh: {self.menu.get_highlight()}")

        text:list[str] = []

        objects_unflattened:list[list[list[str]]] = []
        objects:list[list[str]] = []

        objects_unflattened.append([self.reserve_pile[0]._str(), self.reserve_pile[1]._str(3)]) # reserve
        objects_unflattened += [[x._str()] for x in self.game_piles] # normal
        objects_unflattened.append([x._str() for x in self.final_piles]) # final

        def add_color(color:str|tuple[int,int,int], pos:tuple[int,int]) -> None:
            i1, i2 = pos

            def get_line(_line:str) -> str:
                return Colors.get_color(color) + _line.replace(Colors.get_color('default'), Colors.get_color(color)) + Colors.get_prev_color()

            match i1:
                case 0 | 8:
                    for j, _line in enumerate(objects_unflattened[i1][i2]):
                        objects_unflattened[i1][i2][j] = get_line(_line)
                case _:
                    for j in range(i2*2, len(objects_unflattened[i1][0]) if i2 == len(self.game_piles[i1-1]) - 1 else (i2+1)*2):
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

        return '\n'.join(text)
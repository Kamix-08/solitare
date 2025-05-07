from .Pile import *
import random

class GameManager:
    all_cards:list[Card] = []
    game_piles:list[GamePile] = []
    final_piles:list[FinalPile] = []
    reserve_pile:tuple[ReservePile,GamePile]|None = None

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

    def init_reserve_pile(self) -> None:
        assert self.reserve_pile is None
        self.reserve_pile = (ReservePile(self.mode), GamePile())

        while self.current_card < len(self.all_cards):
            self.reserve_pile[0].add(self.get_next_card(), _force=True)

    def init_piles(self) -> None:
        self.init_game_piles()
        self.init_final_piles()
        self.init_reserve_pile()

    def __init__(self, easy_mode:bool) -> None:
        self.mode = easy_mode

        self.init_cards()
        self.init_piles()

    def move_card(self, i:int, _from:Pile, _to:Pile) -> bool:
        if not _to.can_stack(_from[i], _to[-1]):
            return False
        
        _to.add(_from.pop(i))

        _from.on_move(_removed=True)
        _to.on_move(_removed=False)

        return True
    
    def __str__(self) -> str:
        text:list[str] = []
        objects:list[list[str]] = []

        # reserve piles
        objects.append(self.reserve_pile[0]._str() + self.reserve_pile[1]._str(3))

        # normal piles
        for pile in self.game_piles:
            objects.append(pile._str())

        # final piles
        tmp:list[str] = []
        for pile in self.final_piles:
            tmp += pile._str()
        objects.append(tmp)

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
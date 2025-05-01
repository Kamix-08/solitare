from .Pile import *
import random

class GameManager:
    all_cards:list[Card] = []
    game_piles:list[GamePile] = []
    final_piles:list[FinalPile] = []
    reserve_pile:ReservePile|None = None

    def init_cards(self) -> None:
        assert len(self.all_cards) == 0
        self.current_card = 0

        for suit in Suit:
            for value in Value:
                self.all_cards.append(Card(suit, value))

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

            for _ in range(i):
                current_pile.add(self.get_next_card(), _force=True)

            self.game_piles.append(current_pile)

    def init_final_piles(self) -> None:
        assert len(self.final_piles) == 0

        for suit in Suit:
            self.final_piles.append(FinalPile(suit))

    def init_reserve_pile(self) -> None:
        assert self.reserve_pile is None
        self.reserve_pile = ReservePile(self.mode)

        while self.current_card < len(self.all_cards):
            self.reserve_pile.add(self.get_next_card(), _force=True)

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
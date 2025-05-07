from abc import ABC, abstractmethod
from .Card import *

class Pile(ABC):
    def __init__(self) -> None:
        self.pile:list[Card] = []
        self.hidden:int = -1

    def __len__(self) -> int:
        return len(self.pile)
    
    def __getitem__(self, index:int) -> Card:
        return self.pile[index]
    
    @staticmethod
    @abstractmethod
    def can_stack(a:Card, b:Card) -> bool:
        pass

    def can_add_to_empty(self, a:Card) -> bool:
        return True
    
    def add(self, card:Card, _force:bool = False) -> bool:
        if _force:
            self.pile.append(card)
            return True

        if self.count() == 0:
            if not self.can_add_to_empty(card):
                return False
        
            self.pile.append(card)
            return True
        
        if not self.can_stack(card, self[-1]):
            return False
        
        self.pile.append(card)
        return True
    
    def find(self, card:Card) -> int:
        try: return self.pile.index(card)
        except ValueError: return -1
        
    def pop(self, i:int = -1) -> Card:
        return self.pile.pop(i)
    
    def on_move(self, _removed:bool) -> None:
        pass

    def _str(self, count:int = -1, hidden:bool = True) -> list[str]:
        assert count > 0 or count == -1

        res:list[str] = []
        n:int = len(self)

        for i, card in enumerate(self.pile, 0 if count == -1 else max(0, n - count)):
            is_hidden:bool = hidden and i < self.hidden

            if i == n - 1:
                res += Card._get_back() if is_hidden else card.get_full()
                continue
            
            res += Card._get_back_header() if is_hidden else card.get_header()

        return res
    
    def get_last(self, outline:bool = True, hidden:bool = True) -> list[str]:
        if hidden and self.hidden >= len(self): return Card._get_back()
        if len(self) == 0: return Card._get_full() if outline else []
        return self[-1].get_full()
    
class GamePile(Pile):
    @staticmethod
    def can_stack(a, b) -> bool:
        return (
            (a.value.value + 1 == b.value.value) and 
            (a.suit.is_red ^ b.suit.is_red)
        )
    
    def can_add_to_empty(self, a) -> bool:
        return a.value == Value.KING
    
class FinalPile(Pile):
    def __init__(self, suit:Suit) -> None:
        self.suit = suit
        super().__init__()

    @staticmethod
    def can_stack(a, b) -> bool:
        return (
            (a.value.value == b.value.value + 1) and
            (a.suit == b.suit)
        )
    
    def can_add_to_empty(self, a) -> bool:
        return (
            (a.value == Value.ACE) and
            (a.suit == self.suit)
        )
    
    def _str(self) -> list[str]:
        return self.get_last()
    
class ReservePile(Pile):
    def __init__(self, mode:bool) -> None:
        self.mode = mode
        self.current_card = 0
        super().__init__()

    @staticmethod
    def can_stack(a, b) -> bool:
        return False

    def can_add_to_empty(self, a) -> bool:
        return False
    
    def on_move(self, _removed = False) -> None:
        if _removed and self.current_card > 0:
            self.current_card -= 1

    def _str(self) -> list[str]:
        return Card._get_back()
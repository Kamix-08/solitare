from abc import ABC, abstractmethod
from .Card import *

class Pile(ABC):
    def __init__(self) -> None:
        self.pile = []

    def count(self) -> int:
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
        try:
            return self.pile.index(card)
        except ValueError:
            return -1
        
    def pop(self, i:int = -1) -> Card:
        return self.pile.pop(i)
    
    def on_move(self, _removed:bool = False) -> None:
        pass
    
class GamePile(Pile):
    @staticmethod
    def can_stack(a, b) -> bool:
        return (
            a.value.value + 1 == b.value.value and 
            a.suit.is_red() ^ b.suit.is_red()
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
            a.value.value == b.value.value + 1 and
            a.suit == b.suit
        )
    
    def can_add_to_empty(self, a) -> bool:
        return (
            a.value == Value.ACE and
            a.suit == self.suit
        )
    
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
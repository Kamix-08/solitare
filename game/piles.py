from .cards import *

class Pile:
    def __init__(self):
        self.pile = []

    def count(self) -> int:
        return len(self.pile)
    
    def __getitem__(self, index:int) -> Card:
        return self.pile[index]
    
    @staticmethod
    def can_stack(a:Card, b:Card) -> bool:
        return (
            a.value.value + 1 == b.value.value and 
            a.suit.is_red() ^ b.suit.is_red()
        )
    
    def add(self, card:Card) -> bool:
        if self.count() == 0:
            if card.value != Value.KING:
                return False
            
            self.pile.append(card)
            return True
        
        if not Pile.can_stack(card, self[-1]):
            return False
        
        self.pile.append(card)
        return True
from enum import Enum

class Value(Enum):
    ACE  = 1; TWO = 2;  THREE = 3;  FOUR  = 4
    FIVE = 5; SIX = 6;  SEVEN = 7;  EIGHT = 8
    NINE = 9; TEN = 10; JACK  = 11; QUEEN = 12
    KING = 13

    symbols = {
        ACE: 'A',
        JACK: 'J',
        QUEEN: 'Q',
        KING: 'K'
    }

    def __str__(self) -> str:
        return self.symbols.get(self.value, str(self.value))

class Suit(Enum):
    SPADES = 0; CLUBS = 1
    HEARTS = 2; DIAMONDS = 3

    symbols = {
        SPADES: "♠",
        CLUBS: "♣",
        HEARTS: "♥",
        DIAMONDS: "♦"
    }

    def __str__(self) -> str:
        return self.symbols[self.value]
    
    def is_red(self) -> bool:
        return self.value == Suit.HEARTS or self.value == Suit.DIAMONDS
    
class Card:
    def __init__(self, value:Value, suit:Suit) -> None:
        self.value = value
        self.suit = suit

    def __str__(self) -> str:
        return f"{self.value}{self.suit}"
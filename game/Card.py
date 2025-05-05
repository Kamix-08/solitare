import math
from enum import Enum
from ui.Colors import Colors

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
    WIDTH :int = 4
    HEIGHT:int = 3

    def __init__(self, value:Value, suit:Suit) -> None:
        self.value = value
        self.suit = suit

    def __str__(self) -> str:
        return f"\
            {Colors.get_color('red') if self.suit.is_red() else ''}\
            {self.value}{self.suit}\
            {Colors.get_prev_color() if self.suit.is_red() else ''}\
        "
    
    @staticmethod
    def get_top() -> str:
        return '+' + '-' * Card.WIDTH + '+'
    
    @staticmethod
    def get_normal(text:str='') -> str:
        return '|' + text[:Card.WIDTH] + ' ' * (max(0, Card.WIDTH - len(text))) + '|'
    
    @staticmethod
    def _get_header(text:str='') -> list[str]:
        return [Card.get_top(), Card.get_normal(text)]
    
    @staticmethod
    def _get_full(text:str='') -> list[str]:
        # temp solution
        # the pattern is missing
        return [Card.get_top(), Card.get_normal(text)] + [Card.get_normal()] * (Card.HEIGHT - 1) + [Card.get_top()]
    
    @staticmethod
    def get_back_header() -> list[str]:
        return Card.get_header('* ' * math.ceil(Card.WIDTH/2))

    @staticmethod
    def get_back() -> list[str]:
        return [Card.get_top()] + ([Card.get_normal('* ' * math.ceil(Card.WIDTH/2)), Card.get_normal(' *' * math.ceil(Card.WIDTH/2))] * math.ceil(Card.HEIGHT/2))[:Card.HEIGHT] + [Card.get_top()]

    def get_header(self) -> list[str]:
        return Card._get_header(str(self))
    
    def get_full(self) -> list[str]:
        return Card._get_full(str(self))
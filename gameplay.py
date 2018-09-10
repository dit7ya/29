from typing import Dict, Any

from cards import Card
from operator import attrgetter
import numpy as np

deck = [Card('Ace', 'Spades', 3, 1, 1),
        Card('King', 'Spades', 5, 0, 2),
        Card('Queen', 'Spades', 6, 0, 3),
        Card('Jack', 'Spades', 1, 3, 4),
        Card('10', 'Spades', 4, 1, 5),
        Card('9', 'Spades', 2, 2, 6),
        Card('8', 'Spades', 8, 0, 7),
        Card('7', 'Spades', 7, 0, 8),

        Card('Ace', 'Clubs', 3, 1, 9),
        Card('King', 'Clubs', 5, 0, 10),
        Card('Queen', 'Clubs', 6, 0, 11),
        Card('Jack', 'Clubs', 1, 3, 12),
        Card('10', 'Clubs', 4, 1, 13),
        Card('9', 'Clubs', 2, 2, 14),
        Card('8', 'Clubs', 8, 0, 15),
        Card('7', 'Clubs', 7, 0, 16),

        Card('Ace', 'Hearts', 3, 1, 17),
        Card('King', 'Hearts', 5, 0, 18),
        Card('Queen', 'Hearts', 6, 0, 19),
        Card('Jack', 'Hearts', 1, 3, 20),
        Card('10', 'Hearts', 4, 1, 21),
        Card('9', 'Hearts', 2, 2, 22),
        Card('8', 'Hearts', 8, 0, 23),
        Card('7', 'Hearts', 7, 0, 24),

        Card('Ace', 'Diamonds', 3, 1, 25),
        Card('King', 'Diamonds', 5, 0, 26),
        Card('Queen', 'Diamonds', 6, 0, 27),
        Card('Jack', 'Diamonds', 1, 3, 28),
        Card('10', 'Diamonds', 4, 1, 29),
        Card('9', 'Diamonds', 2, 2, 30),
        Card('8', 'Diamonds', 8, 0, 31),
        Card('7', 'Diamonds', 8, 0, 32)
        ]


def decision_logic(card1, card2, card3, card4, trump_suit, trump_revealed):
    running_suit = card1.get_suit()
    cards = [card1, card2, card3, card4]
    cards_less = []
    trump_cards = []

    for card in cards:
        if card.get_suit() == trump_suit:
            trump_cards.append(card)

    if len(trump_cards) != 0 and trump_revealed == True:
        lowest_trump = min(trump_cards, key=attrgetter('rank'))

        winner = lowest_trump

    else:
        for card in cards:
            if card.get_suit() == running_suit:
                cards_less.append(card)
        lowest_card = min(cards_less, key=attrgetter('rank'))
        winner = lowest_card
    return winner


def deal_cards():
    cards_shuffled = np.random.choice(deck, 32, replace=False)
    # print(cards_shuffled)
    cards_distribution = {1: cards_shuffled[:8],
                          2: cards_shuffled[8:16],
                          3: cards_shuffled[16:24],
                          4: cards_shuffled[24:]
                          }

    return cards_distribution


def points_in_trick(card1: Card, card2: Card, card3: Card, card4: Card):
    points: int = card1.get_point() + card2.get_point() + card3.get_point() + card4.get_point()
    return points

agent1 =
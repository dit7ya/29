from cards import *
from gameplay import points_in_trick
import numpy as np


def bid_and_trump(card1, card2, card3, card4):
    bid = 15

    if points_in_trick(card1, card2, card3, card4)>= 6:
        bid = 17

    cards = [card1, card2, card3, card4]

    trump_suit = None
    for i in cards:
        if i.get_name() == 'Jack':
            bid += 1.5
            trump_suit = i.get_suit()
        elif i.get_name() == '9':
            bid += .75
            if trump_suit is None:
                trump_suit = i.get_suit()

        elif i.get_name() == 'Ace' or i.get_name() == '10':
            bid += 0.25

    bid = np.ceil(bid)

    return bid, trump_suit

#print(deck[10], deck[5], deck[15], deck[29])

#print(estimate_bid(deck[10], deck[5], deck[15], deck[29]))
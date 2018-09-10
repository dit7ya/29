from typing import Dict, Any

from cards import Card
from operator import attrgetter
import numpy as np

from cards import deck


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


def convert_ID(list_cards):
    list_IDs = []
    for card in list_cards:
        list_IDs.append(card.get_ID())

    return list_IDs


def trick(agents, public_info, private_infos, trump_info, last_winner, states, points_dict):
    first_player = agents[last_winner]
    second_player = agents[last_winner % 4 + 1]
    third_player = agents[((last_winner % 4) + 1) % 4 + 1]
    fourth_player = agents[(((last_winner % 4) + 1) % 4 + 1) % 4 + 1]

    # first player plays

    card1, public_info, private_infos, trump_info, states, running_suit = first_player.play_card(public_info,
                                                                                                 private_infos,
                                                                                                 trump_info, states,
                                                                                                 running_suit=0)

    # second player playes

    card2, public_info, private_infos, trump_info, states, running_suit = second_player.play_card(public_info,
                                                                                                  private_infos,
                                                                                                  trump_info, states,
                                                                                                  running_suit)

    # third player playes

    card3, public_info, private_infos, trump_info, states, running_suit = third_player.play_card(public_info,
                                                                                                 private_infos,
                                                                                                 trump_info, states,
                                                                                                 running_suit)

    # fourth player plays

    card4, public_info, private_infos, trump_info, states, running_suit = fourth_player.play_card(public_info,
                                                                                                  private_infos,
                                                                                                  trump_info, states,
                                                                                                  running_suit)

    trump_suit = trump_info[1]

    # winner card decided
    winning_card = decision_logic(card1, card2, card3, card4, trump_suit, trump_revealed=False)

    if winning_card == card1:
        winner = last_winner
    elif winning_card == card2:
        winner = last_winner % 4 + 1

    elif winning_card == card3:
        winner = ((last_winner % 4) + 1) % 4 + 1

    elif winning_card == card4:
        winner = (((last_winner % 4) + 1) % 4 + 1) % 4 + 1

    # points dict is updated

    points_dict[winner] += points_in_hand(card1, card2, card3, card4)

    return public_info, private_infos, trump_info, winner, states, points_dict


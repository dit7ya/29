from typing import List, Any
import numpy as np
from cards import deck

from keras.models import load_model

model = load_model('my_model.h5')


def get_card(ID, deck):
    card = deck[(int(ID) - 1)]

    return card


def get_legal_actions(private_info, running_suit):
    legal_cards = []
    can_play_trump = False

    for ID in private_info:
        if ID != 0:
            card = get_card(ID, deck)
            if card.get_suit() == running_suit:
                legal_cards.append(ID)
            else:
                pass
        else:
            pass

    if legal_cards == [] or legal_cards == private_info:
        can_play_trump = True
        for ID in private_info:
            if ID != 0:
                legal_cards.append(ID)

    return legal_cards, can_play_trump


def reveal_trump(trump_info):
    trump_info[0] = 1
    # print('Trump has been revealed. It is: ', trump_info[1])
    return trump_info

def suit_map(suit):
  if suit == 'Spades':
    num = 1
  elif suit == 'Clubs':
    num = 2
  elif suit == 'Hearts':
    num = 3
  else:
    num = 4
  return num



def get_state(public_info, private_info, trump_info):
    if trump_info[0] == 1:

        state = [np.concatenate((public_info, private_info, [suit_map(trump_info[1])]))]
    else:
        state = [np.concatenate((public_info, private_info, [0]))]
    return state


def write_state_that_was_used(state, states):
    states.append(state)
    return states


def update_private_info(private_info, played_card_ID):
    private_info.remove(played_card_ID)
    private_info.append(0)
    return private_info


def update_public_info(public_info, played_card_ID):
    # public_info = public_info.tolist().remove(0)
    # public_info = public_info.tolist().append(played_card_ID)

    public_info[np.flatnonzero(public_info == 0)[0]] = played_card_ID
    return public_info


def choose_card(public_info, private_info, trump_info, running_suit, epsilon=0.1):
    # state = self.get_state(public_info, private_info, trump_info)

    legal_actions, can_play_trump = get_legal_actions(private_info, running_suit)

    if can_play_trump == True and trump_info[0] == 0 and np.random.rand() > 0.9:
        trump_info = reveal_trump(trump_info)

    # print(a)
    Q_state = {}
    for action in legal_actions:  # calculate Q(state, action)

        private_info_temp = private_info.copy()
        public_info_temp = public_info.copy()
        possible_private_info = update_private_info(private_info_temp, played_card_ID=action)
        possible_public_info = update_public_info(public_info_temp, played_card_ID=action)

        possible_state = get_state(possible_public_info, possible_private_info, trump_info)

        Q_state[action] = np.float(model.predict(np.array(possible_state)))

        # Q_state[action] = np.linalg.norm(state)*action # just for testing
    # print(Q_state)
    best_action = max(Q_state.items(), key=lambda x: x[1])[0]
    if np.random.rand() > epsilon:
        card_ID = best_action
    else:
        card_ID = np.random.choice(legal_actions)

    card = get_card(card_ID, deck)

    return card, trump_info

def get_cards_from_IDs(IDs):
    cards = []
    card_names = {}
    for ID in IDs:
        cards.append(get_card(ID, deck))
        card_names[ID] = get_card(ID, deck).__str__()
    return cards, card_names


class Agent:
    name: str
    private_info: list

    def __init__(self, name, agent_num, private_info):
        self.name = name
        self.agent_num = agent_num
        self.partner_num = (self.agent_num % 4 + 1) % 4 + 1
        self.private_info = private_info

    def __str__(self):
        return "%s" % self.name

    def get_name(self):
        return self.name

    def get_agent_num(self):
        return self.agent_num

    def get_private_info(self):
        return self.private_info

    def get_partner_num(self):
        return self.partner_num


class Bot(Agent):

    def play_card(self, public_info, private_infos, trump_info, states, running_suit=0):
        private_info = private_infos[self.agent_num]
        player_state = get_state(public_info, private_info, trump_info)
        states = write_state_that_was_used(player_state, states)
        card, trump_info = choose_card(public_info, private_info, trump_info, running_suit, epsilon=0.2)
        private_infos[self.agent_num] = update_private_info(private_info, played_card_ID=card.get_ID())
        public_info = update_public_info(public_info, played_card_ID=card.get_ID())
        running_suit = card.get_suit()
        return card, public_info, private_infos, trump_info, states, running_suit


class Human(Agent):

    def play_card(self, public_info, private_infos, trump_info, states, running_suit=0):
        private_info = private_infos[self.agent_num]
        player_state = get_state(public_info, private_info, trump_info)
        states = write_state_that_was_used(player_state, states)
        legal_actions, can_play_trump = get_legal_actions(private_info, running_suit)
        _, legal_cards = get_cards_from_IDs(legal_actions)
        print('It is your turn,', self.get_name(), '.', 'Legal moves are: ', legal_cards)

        if can_play_trump:
            trump_choice = input('Do you want to reveal/play Trump? 1/0')
            if trump_choice == 1:
                trump_info = reveal_trump(trump_info)

        # cards = [get_card(ID, deck) for ID in private_info]
        # print('You have the cards, ', cards)
        #print()
        card_ID = input('Enter the card_ID you want to play.')

        card = get_card(card_ID, deck)

        private_infos[self.agent_num] = update_private_info(private_info, played_card_ID=card.get_ID())
        public_info = update_public_info(public_info, played_card_ID=card.get_ID())
        running_suit = card.get_suit()
        return card, public_info, private_infos, trump_info, states, running_suit

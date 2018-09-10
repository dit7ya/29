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

    def get_partner_num(self):
        return self.partner_num
    
    def get_legal_actions(self, running_suit):
        legal_cards = []
        can_play_trump = False

        for ID in self.private_info:
            if ID != 0:
                card = get_card(ID, deck)
                if card.get_suit() == running_suit:
                    legal_cards.append(ID)
                else:
                    pass
            else:
                pass

        if legal_cards == []:
            can_play_trump = True
            for ID in private_info:
                if ID != 0:
                    legal_cards.append(ID)

        return legal_cards, can_play_trump

    def reveal_trump(self, trump_info, can_play_trump):
        assert isinstance(can_play_trump, int)
        if can_play_trump:
            trump_info[0] = 1
        return trump_info

    def get_state(self, public_info, private_info, trump_info):
        if trump_info[0] == 1:

            state = [np.concatenate((public_info, private_info, [suit_map(trump_info[1])]))]
        else:
            state = [np.concatenate((public_info, private_info, [0]))]
        return state

    def write_state_that_was_used(self, state, states):
        states.append(state)
        return states

    def choose_card(self, public_info, private_info, trump_info, running_suit, epsilon=0.1):

        # state = self.get_state(public_info, private_info, trump_info)

        legal_actions, can_play_trump = self.get_legal_actions(private_info, running_suit)

        if can_play_trump == True and trump_info[0] == 0:
            if np.random.rand() > 0.4:
                trump_info = self.reveal_trump(trump_info, can_play_trump)

        # print(a)
        Q_state = {}
        for action in legal_actions:  # calculate Q(state, action)

            ### it has to look ahead one step with new public and private info 
            ## and estimate Q for different state, action pairs

            private_info_temp = private_info.copy()
            public_info_temp = public_info.copy()
            possible_private_info = self.update_private_info(private_info_temp, played_card_ID=action)
            possible_public_info = self.update_public_info(public_info_temp, played_card_ID=action)

            possible_state = self.get_state(possible_public_info, possible_private_info, trump_info)

            Q_state[action] = model.predict(np.array(possible_state))

            # Q_state[action] = np.linalg.norm(state)*action # just for testing
        # print(Q_state)
        best_action = max(Q_state.items(), key=lambda x: x[1])[0]
        if np.random.rand() > epsilon:
            card_ID = best_action
        else:
            card_ID = np.random.choice(legal_actions)

        card = get_card(card_ID, deck)

        return card, trump_info

    ## Both Public and Private Info are just list of Card IDs

    # Method for updating private_info

    def update_private_info(self, private_info, played_card_ID):
        private_info.remove(played_card_ID)
        private_info.append(0)
        return private_info

    # Method for updating public_info

    def update_public_info(self, public_info, played_card_ID):
        # public_info = public_info.tolist().remove(0)
        # public_info = public_info.tolist().append(played_card_ID)

        public_info[np.flatnonzero(public_info == 0)[0]] = played_card_ID
        return public_info

    def play_card(self, public_info, private_infos, trump_info, states, running_suit=0):

        private_info = private_infos[self.agent_ID]
        player_state = self.get_state(public_info, private_info, trump_info)
        states = self.write_state_that_was_used(player_state, states)
        card, trump_info = self.choose_card(public_info, private_info, trump_info, running_suit, epsilon=0.2)
        private_infos[self.agent_ID] = self.update_private_info(private_info, played_card_ID=card.get_ID())
        public_info = self.update_public_info(public_info, played_card_ID=card.get_ID())
        running_suit = card.get_suit()
        return card, public_info, private_infos, trump_info, states, running_suit

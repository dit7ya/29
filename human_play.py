from agents import *
from gameplay import *

cards_distribution = deal_cards()



players = {1: Human('Sayan', 1, convert_ID(cards_distribution[1])),
          2: Bot('Bot2', 2, convert_ID(cards_distribution[2])),
          3: Human('JohnDoe', 3, convert_ID(cards_distribution[3])),
          4: Bot('Bot4', 4, convert_ID(cards_distribution[4]))
          }


def trick_human(agents, public_info, private_infos, trump_info, last_winner, states, points_dict):
    first_player = agents[last_winner]
    second_player = agents[last_winner % 4 + 1]
    third_player = agents[((last_winner % 4) + 1) % 4 + 1]
    fourth_player = agents[(((last_winner % 4) + 1) % 4 + 1) % 4 + 1]

    # first player plays

    card1, public_info, private_infos, trump_info, states, running_suit = first_player.play_card(public_info,
                                                                                                 private_infos,
                                                                                                 trump_info, states,
                                                                                                 running_suit=0)
    print(first_player, 'has played the card', card1)

    # second player plays

    card2, public_info, private_infos, trump_info, states, running_suit = second_player.play_card(public_info,
                                                                                                  private_infos,
                                                                                                  trump_info, states,
                                                                                                  running_suit)
    print(second_player, 'has played the card', card2)

    # third player plays

    card3, public_info, private_infos, trump_info, states, running_suit = third_player.play_card(public_info,
                                                                                                 private_infos,
                                                                                                 trump_info, states,
                                                                                                 running_suit)
    print(third_player, 'has played the card', card3)
    # fourth player plays

    card4, public_info, private_infos, trump_info, states, running_suit = fourth_player.play_card(public_info,
                                                                                                  private_infos,
                                                                                                  trump_info, states,
                                                                                                  running_suit)
    print(fourth_player, 'has played the card', card4)

    trump_suit = trump_info[1]
    trump_revealed = trump_info[0]

    # winner card decided
    winning_card = decision_logic(card1, card2, card3, card4, trump_suit, trump_revealed)

    if winning_card == card1:
        winner = last_winner
    elif winning_card == card2:
        winner = last_winner % 4 + 1

    elif winning_card == card3:
        winner = ((last_winner % 4) + 1) % 4 + 1

    elif winning_card == card4:
        winner = (((last_winner % 4) + 1) % 4 + 1) % 4 + 1

    # points dict is updated

    points_dict[winner] += points_in_trick(card1, card2, card3, card4)

    return public_info, private_infos, trump_info, winner, states, points_dict


def play_human_game(agents):
    public_info = np.zeros(32)
    private_infos = {1: agents[1].get_private_info(),
                     2: agents[2].get_private_info(),
                     3: agents[3].get_private_info(),
                     4: agents[4].get_private_info()}

    print(private_infos)

    trump_info = [0, np.random.choice(['Spades', 'Clubs', 'Hearts', 'Diamonds'])]
    print('Trump suit is', trump_info[1])

    last_winner = np.random.randint(1, 5)
    print('The game begins with', agents[last_winner])
    states = []
    points_dict = {1: 0, 2: 0, 3: 0, 4: 0}

    reward_list = []
    for i in range(8):
        public_info, private_infos, trump_info, winner, states, points_dict = trick_human(agents, public_info, private_infos,
                                                                                    trump_info, last_winner, states,
                                                                                    points_dict)
        print('Winner from the previous hand is: ', agents[winner])
        reward_list = points_dict_to_reward_list(points_dict, reward_list)
        last_winner = winner

    G = calculate_G(reward_list, gamma=0.9)
    final_states = np.reshape(states, (32, 41))
    final_G = np.reshape(G, (32, 1))
    print('Points for this game is:', points_dict)

    return final_states, final_G


final_states, final_G = play_human_game(players)

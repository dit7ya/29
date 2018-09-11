from agents import Bot
from keras.models import load_model
from gameplay import *

num_games = 1000


def play_m_games(m):
    states = np.zeros((m, 32, 41))
    Gs = np.zeros((m, 32, 1))
    for i in range(m):
        cards_distribution = deal_cards()

        agents = {1: Bot('Bot1', 1, convert_ID(cards_distribution[1])),
                  2: Bot('Bot2', 2, convert_ID(cards_distribution[2])),
                  3: Bot('Bot3', 3, convert_ID(cards_distribution[3])),
                  4: Bot('Bot4', 4, convert_ID(cards_distribution[4]))
                  }

        final_states, final_G = play_one_game(agents)
        states[i] = final_states
        Gs[i] = final_G

    states_flatten, Gs_flatten = np.reshape(states, (m * 32, 41)), np.reshape(Gs, (m * 32, 1))

    return states_flatten, Gs_flatten


states, Gs = play_m_games(num_games)

model = load_model('my_model.h5')
model.fit(states, Gs, epochs=100)
model.save('my_model.h5')  # creates a HDF5 file 'my_model.h5'


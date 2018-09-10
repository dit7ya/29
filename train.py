from agents import Bot
from keras.models import load_model
from gameplay import play_m_games, deal_cards, convert_ID

num_games = 1000

cards_distribution = deal_cards()

agents = [Bot('Bot1', 1, convert_ID(cards_distribution[0])),
          Bot('Bot2', 2, convert_ID(cards_distribution[1])),
          Bot('Bot3', 3, convert_ID(cards_distribution[2])),
          Bot('Bot4', 4, convert_ID(cards_distribution[3]))
          ]

states, Gs = play_m_games(num_games)


model = load_model('my_model.h5')
model.fit(states, Gs, epochs = 20)
model.save('my_model.h5')  # creates a HDF5 file 'my_model.h5'

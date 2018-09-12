from keras.models import Sequential
from keras.layers import Dense

# create model

model = Sequential()
model.add(Dense(128, input_shape = (41,), activation='relu', kernel_initializer = 'he_normal'))
model.add(Dense(64, activation='relu', kernel_initializer = 'he_normal', bias_initializer='zeros'))
model.add(Dense(32, activation='relu', kernel_initializer = 'he_normal', bias_initializer='zeros'))
model.add(Dense(16, activation = 'relu'))
model.add(Dense(1, activation='linear', kernel_initializer = 'he_normal'))

# Compile model

model.compile(loss='mse', optimizer='adam')
model.summary()

model.save('third_model.h5')
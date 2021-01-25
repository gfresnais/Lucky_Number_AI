import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from collections import deque

from App.src.JoueurIA import JoueurIA


class trainer:

    def __init__(self, name=None, joueur=None, learning_rate=0.001, epsilon_decay=0.9999, batch_size=30, memory_size=3000):
        self.state_size = 17
        self.action_size = 16
        self.gamma = 0.9
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = epsilon_decay
        self.learning_rate = learning_rate
        self.memory = deque(maxlen=memory_size)
        self.batch_size = batch_size

        self.name = name
        if name is not None :
            model = keras.load_model("App/res/Assets/Model-" + name)
        else:
            model = keras.Sequential()
            model.add(layers.Dense(64, input_dim=self.state_size, activation='relu'))
            model.add(layers.Dense(64, activation='relu'))
            model.add(layers.Dense(32, activation='relu'))
            model.add(layers.Dense(self.action_size, activation='linear'))
            model.compile(loss='mse', optimizer=keras.Adam(lr=self.learning_rate))

        self.model = model

        if joueur is not None :
            self.Joueur = joueur
        else:
            self.joueur = JoueurIA()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append([state, action, reward, next_state, done])
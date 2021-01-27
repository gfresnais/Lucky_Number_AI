import time

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from collections import deque
import random
import numpy as np

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

    def randomAction(self):
        return random.randrange(self.action_size)

    def bestAction(self, state, rand=True):

        self.epsilon *= self.epsilon_decay

        if rand and random.rand() <= self.epsilon:
            # The agent acts randomly
            return random.randrange(self.action_size)

        # Predict the reward value based on the given state
        act_values = self.model.predict(np.array([state]))

        # Pick the action based on the predicted reward
        action = np.argmax(act_values[0])
        return action

    def replay(self, batch_size):
        batch_size = min(batch_size, len(self.memory))

        minibatch = random.sample(self.memory, batch_size)

        inputs = np.zeros((batch_size, self.state_size))
        outputs = np.zeros((batch_size, self.action_size))

        for i, (state, action, reward, next_state, done) in enumerate(minibatch):
            target = self.model.predict(state)[0]
            print("DEBUG : " + target)
            if done:
                target[action] = reward
            else:
                target[action] = reward + self.gamma * np.max(self.model.predict(next_state))

            inputs[i] = state
            outputs[i] = target

        return self.model.evaluate(inputs, outputs, batch_size=batch_size, verbose=0)

    def save(self, id=None, overwrite=False):
        name = 'model'
        if self.name:
            name += '-' + self.name
        else:
            name += '-' + str(time.time())
        if id:
            name += '-' + id
        self.model.save(name, overwrite=overwrite)
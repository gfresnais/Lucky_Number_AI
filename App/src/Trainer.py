import time

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from collections import deque
import random
import numpy as np


class Trainer:

    def __init__(self, name=None, learning_rate=0.001, epsilon_decay=0.9999, batch_size=64, memory_size=3000):
        # paramètre du reseaux de neurones
        self.state_size = 17 # taille de l'entrée du reseaux de neurones
        self.action_size = 16 # taille de sortie du reseaux de neurones
        self.gamma = 0.9 # ?
        self.epsilon = 1.0 #variable de chance d'exploration (aléatoire)
        self.epsilon_min = 0.01 # taux d'aléatoire min
        self.epsilon_decay = epsilon_decay # taux de reduction de l'aléatoire
        self.learning_rate = learning_rate # ?
        self.memory = deque(maxlen=memory_size) # taille de la mémoire d'apprentissage
        self.batch_size = batch_size # taible des échantillons donnés en entrainement
        self.name = name
        if name is not None : # il a un nom on charge le reseau nommé
            model = keras.models.load_model("../res/Assets/model-" + name)
        else: # sinon on en créé un nouveau
            model = keras.Sequential() # type de model
            # couche cachée
            model.add(layers.Dense(16, input_dim=self.state_size, activation='relu'))
            model.add(layers.Dense(16, activation='relu'))
            # couche de sortie
            model.add(layers.Dense(self.action_size, activation='linear'))
            #compilateur
            model.compile(loss='mse', optimizer=keras.optimizers.Adam(lr=self.learning_rate))
        self.model = model

    # sauvegarde les infos dans la mémoire d'apprentissage
    def remember(self, state, action, reward):
        self.memory.append([state, action, reward])

    #retourn une position du plateau aléatoire
    def randomAction(self):
        return random.randrange(self.action_size)

    #reduit l'epsilon
    def actu_epsilon(self):
        self.epsilon *= self.epsilon_decay

    # retourne une position du plateau en fonction de son etat et du jeton pioché
    def bestAction(self, state, rand=True):

        if rand and random.random() <= self.epsilon: # pourcentage de chance(epsilon) de faire de l'exploration
            # The agent acts randomly
            return self.randomAction()

        # Predict the reward value based on the given state
        act_values = self.model.predict(np.array([state]))

        # Pick the action based on the predicted reward
        action = np.argmax(act_values[0]) # position de la plus grande valeur du vecteur de prediction
        return action

    # recupere un echantillon dans la mémoire d'aprantissage et le donne au reseau pour s'entrainer
    def replay(self, batch_size):
        batch_size = min(batch_size, len(self.memory)) #recuperation de la taille de l'echantillon

        minibatch = random.sample(self.memory, batch_size) # recuperation de l'echantillon

        # creation des jeux de données
        inputs = np.zeros((batch_size, self.state_size))
        outputs = np.zeros((batch_size, self.action_size))

        #traitement de chaque echantillon
        for i, (state, action, reward) in enumerate(minibatch):
            target = self.model.predict(state)[0]
            target[action] = reward

            inputs[i] = state
            outputs[i] = target

        return self.model.evaluate(inputs, outputs, batch_size=batch_size, verbose=0) # entrainement

    # sauvegarde le model de reseau de neurones
    def save(self, id=None, overwrite=False):
        name = 'model'
        if self.name:
            name += '-' + self.name
        else:
            name += '-' + str(time.time())
        if id:
            name += '-' + id
        self.model.save(name, overwrite=overwrite)

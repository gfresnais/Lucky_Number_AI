# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 14:53:05 2021

@author: vallee
"""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

import numpy as np

from App.src import Pioche

from collections import deque

class JoueurIA:
    OLD_PLATEAU = np.eye(4, 4, int())
    JETON = 0

    def __init__(self,
                 firstNumber,
                 secondNumber,
                 thirdNumber,
                 fourthNumber):
        setDeJeton = np.array([firstNumber, secondNumber, thirdNumber, fourthNumber])
        setDeJeton.sort()
        self.OLD_PLATEAU[0, 0] = setDeJeton[0]
        self.OLD_PLATEAU[1, 1] = setDeJeton[1]
        self.OLD_PLATEAU[2, 2] = setDeJeton[2]
        self.OLD_PLATEAU[3, 3] = setDeJeton[3]

    def verification(self, newPlateau):
        for colone in range(4):
            for ligne in range(4):
                if self.OLD_PLATEAU[colone, ligne] != newPlateau[colone, ligne]:
                    number = newPlateau[colone, ligne]
                    if colone != 0:
                        if number <= newPlateau[colone - 1, ligne]:
                            return False
                    if ligne != 0:
                        if number <= newPlateau[colone, ligne - 1]:
                            return False
                    if colone != 3:
                        if number <= newPlateau[colone + 1, ligne]:
                            return False
                    if ligne != 3:
                        if number <= newPlateau[colone, ligne + 1]:
                            return False
                    self.OLD_PLATEAU = newPlateau
                    return True

    def getState(self, pioche):
        plateau = self.plateau
        jeton = self.JETON
        state = []

        for i in range(4):
            state.append(plateau[i])

        state.append(jeton)

        return state

    def pioche(self, pioche):
        self.JETON = pioche.piocheJeton()


class trainer:

    def __init__(self,
                 learning_rate=0.001,
                 epsilon_decay=0.9999,
                 batch_size=30,
                 memory_size=3000):
        self.state_size = 17
        self.action_size = 16
        self.gamma = 0.9
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = epsilon_decay
        self.learning_rate = learning_rate
        self.memory = deque(maxlen=memory_size)
        self.batch_size = batch_size

        model = Sequential()
        model.add(Dense(32, input_dim=self.state_size, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))

        self.model = model

        self.pioche = Pioche()
        self.joueur = JoueurIA(self.pioche.pioche(),
                               self.pioche.pioche(),
                               self.pioche.pioche(),
                               self.pioche.pioche())

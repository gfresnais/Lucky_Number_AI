# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 14:53:05 2021

@author: vallee
"""
import numpy as np

from App.src.Game import Game


class JoueurIA:
    
    PLATEAU = np.eye(4, 4, int())
    JETON = 0
    
    def __init__(self, firstNumber, secondNumber, thirdNumber, fourthNumber):
        setDeJeton = np.array([firstNumber,secondNumber,thirdNumber,fourthNumber])
        setDeJeton.sort()
        self.PLATEAU[0, 0] = setDeJeton[0]
        self.PLATEAU[1, 1] = setDeJeton[1]
        self.PLATEAU[2, 2] = setDeJeton[2]
        self.PLATEAU[3, 3] = setDeJeton[3]
    
    
    def verification(self, newPlateau):
        for colone in range(4):
            for ligne in range(4):
                if self.PLATEAU[colone, ligne] != newPlateau[colone, ligne]:
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
                    self.PLATEAU = newPlateau
                    return True

    def getState(self):
        state = []

        for i in range(4):
            state.append(self.PLATEAU[i])

        state.append(self.JETON)

        return state

    def newJeton(self, jeton):
        self.JETON = jeton

    def poseJeton(self, jeton, position):
        newPlateau = self.PLATEAU
        ligne = position // 4
        colonne = position % 4
        newPlateau[ligne, colonne] = jeton
        if self.verification(newPlateau):
            if self.checkWin(newPlateau):
                return newPlateau, 10, True, True
            else:
                return newPlateau, 1, False, True
        else:
            return newPlateau, -1, False, False

    def reset(self, firstNumber, secondNumber, thirdNumber, fourthNumber):
        plateau = np.eye(4, 4, int())
        plateau[0, 0] = firstNumber
        plateau = secondNumber
        plateau = thirdNumber
        plateau = fourthNumber
        self.PLATEAU = plateau
        return plateau

#WIP
    def train(self, episodes, trainer, collecting=False, snapshot=5000):
        batch_size = 32
        game = Game()
        pioche = game.pioche
        scores = []
        global_counter = 0
        losses = [0]
        epsilons = []

        # we start with a sequence to collect information, without learning
        if collecting:
            collecting_steps = 10000
            print("Collecting game without learning")
            steps = 0
            while steps < collecting_steps:
                state = self.reset(pioche.piocheJeton(), pioche.piocheJeton(), pioche.piocheJeton(), pioche.piocheJeton())
                done = False
                while not done:
                    steps += 1
                    jeton = self.newJeton(pioche.piocheJeton())
                    position = self.randomAction()
                    check = False
                    while check:
                        next_state, reward, done, check = self.poseJeton(jeton, position)
                        trainer.remember(state, position, reward, next_state, done)
                    state = next_state

        print("Starting training")
        global_counter = 0
        for e in range(episodes + 1):
            state = self.reset()
            state = np.reshape(state, [1, 16])
            score = 0
            done = False
            steps = 0
            while not done:
                steps += 1
                global_counter += 1
                action = trainer.bestAction(state)

                check = False
                while check:
                    next_state, reward, done, check = g.move(action)
                    next_state = np.reshape(next_state, [1, 16])
                    score += reward
                    trainer.remember(state, action, reward, next_state, done)

                state = next_state

                if global_counter % 100 == 0:
                    l = trainer.replay(batch_size)  # ici on lance le 'replay', c'est un entrainement du réseau
                    losses.append(l.history['loss'][0])

                if done:
                    scores.append(score)
                    epsilons.append(trainer.epsilon)

                if steps > 200:
                    break
            if e % 200 == 0:
                print("episode: {}/{}, moves: {}, score: {}, epsilon: {}, loss: {}"
                      .format(e, episodes, steps, score, trainer.epsilon, losses[-1]))

            if e > 0 and e % snapshot == 0:
                trainer.save(id='iteration-%s' % e)

        return scores, losses, epsilons


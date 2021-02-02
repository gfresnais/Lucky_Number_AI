# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 14:53:05 2021

@author: vallee
"""
import numpy as np
import copy

from App.src.Jeton import Jeton
from App.src.Pioche import Pioche
from App.src.Trainer import Trainer


class JoueurIA:
    
    def __init__(self, firstJeton, secondJeton, thirdJeton, fourthJeton):
        setDeJeton = [firstJeton, secondJeton, thirdJeton, fourthJeton]
        plateau = []
        for i in range(4):
            ligne = []
            for j in range(4):
                ligne.append(Jeton())
            plateau.append(ligne)
        setDeJeton.sort(key=lambda Jeton: Jeton.number)
        plateau[0][0] = setDeJeton[0]
        plateau[1][1] = setDeJeton[1]
        plateau[2][2] = setDeJeton[2]
        plateau[3][3] = setDeJeton[3]
        self.plateau = plateau
        self.jeton = 0

    #TODO
    def verification(self, newPlateau):
        for ligne in range(4):
            for colone in range(4):
                if self.plateau[ligne][colone] != newPlateau[ligne][colone]:
                    number = newPlateau[ligne][colone].number

                    if ligne != 0:
                        for testLigne in range(ligne):
                            if number <= newPlateau[testLigne][colone].number != 0:
                                return False

                    if colone != 0:
                        for testColone in range(colone):
                            if number <= newPlateau[ligne][testColone].number != 0:
                                return False

                    if ligne != 3:
                        for testLigne in range(ligne+1, 4):
                            if number <= newPlateau[testLigne][colone].number != 0:
                                return False

                    if colone != 3:
                        for testColone in range(colone + 1, 4):
                            if number <= newPlateau[ligne][testColone].number != 0:
                                return False
                    self.plateau = newPlateau
                    return True

    def getState(self):
        state = []
        for i in range(4):
            for j in range(4):
                state.append(self.plateau[i][j].number)
        state.append(self.jeton)
        state = np.reshape(state, [1, 17])
        return state

    def newJeton(self, jeton):
        self.jeton = jeton
        return jeton

    def checkWin(self, plateau):
        for i in range(4):
            for j in range(4):
                if plateau[i][j].number == 0:
                    return False
        return True

    def poseJeton(self, jeton, position):
        newPlateau = copy.deepcopy(self.plateau)
        ligne = position // 4
        colonne = position % 4
        newPlateau[ligne][colonne] = jeton
        if self.verification(newPlateau):
            if self.checkWin(newPlateau):
                return newPlateau, 10, True, True, self.plateau[ligne][colonne]
            else:
                return newPlateau, 1, False, True, self.plateau[ligne][colonne]
        else:
            return newPlateau, -1, False, False, Jeton() #faux jeton

    def reset(self, firstJeton, secondJeton, thirdJeton, fourthJeton):
        setDeJeton = [firstJeton, secondJeton, thirdJeton, fourthJeton]
        plateau = []
        for i in range(4):
            ligne = []
            for j in range(4):
                ligne.append(Jeton())
            plateau.append(ligne)
        setDeJeton.sort(key=lambda Jeton: Jeton.number)
        plateau[0][0] = setDeJeton[0]
        plateau[1][1] = setDeJeton[1]
        plateau[2][2] = setDeJeton[2]
        plateau[3][3] = setDeJeton[3]
        self.plateau = plateau
        self.jeton = Jeton()

    def set_plateau(self, NewState):
        index = 0
        for i in range(4):
            for j in range(4):
                self.plateau[i][j] = NewState[0][index]
                index += 1

    def aff_plateau(self):
        for i in range(4):
            ligne = self.plateau[i]
            print("" + str(ligne[0].number) + " " + str(ligne[1].number) + " " + str(ligne[2].number) + " " + str(ligne[3].number))


#WIP
    def train(self, episodes, trainer, collecting=False, snapshot=5000):
        batch_size = 32
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
                pioche = Pioche()
                self.reset(pioche.piocheJeton(), pioche.piocheJeton(), pioche.piocheJeton(), pioche.piocheJeton())
                done = False
                while not done:
                    steps += 1
                    jeton = self.newJeton(pioche.piocheJeton())
                    state = self.getState()
                    self.aff_plateau()
                    print('jeton :' + str(jeton.number))
                    check = False
                    while not check:
                        position = trainer.randomAction()
                        print(str(position))
                        next_state, reward, done, check, defausse = self.poseJeton(jeton, position)
                        next_state = np.reshape(next_state, [1, 16])
                        trainer.remember(state, position, reward, next_state, done)
                        if check:
                            if defausse.number != 0:
                                pioche.DefausseJeton(defausse)
                            self.set_plateau(next_state)
                    if len(pioche.PIOCHE) == 0:
                        done = True
                self.aff_plateau()

        print("Starting training")
        global_counter = 0
        for e in range(episodes + 1):
            pioche = Pioche()
            self.reset(pioche.piocheJeton(), pioche.piocheJeton(), pioche.piocheJeton(), pioche.piocheJeton())
            score = 0
            done = False
            steps = 0
            while not done:
                global_counter += 1
                jeton = self.newJeton(pioche.piocheJeton())
                state = self.getState()
                check = False
                while not check:
                    steps += 1
                    position = trainer.bestAction(state)
                    next_state, reward, done, check, defausse = self.poseJeton(jeton, position)
                    next_state = np.reshape(next_state, [1, 16])
                    score += reward
                    trainer.remember(state, position, reward, next_state, done)
                    if check:
                        if defausse.number != 0:
                            pioche.DefausseJeton(defausse)
                        self.set_plateau(next_state)
                trainer.actu_epsilon()

                if len(pioche.PIOCHE) == 0:
                    done = True

                if global_counter % 100 == 0:
                    l = trainer.replay(batch_size)
                    losses.append(l)

                if done:
                    scores.append(score)
                    epsilons.append(trainer.epsilon)

            if e % 200 == 0:
                print("episode: {}/{}, moves: {}, score: {}, epsilon: {}, loss: {}"
                      .format(e, episodes, steps, score, trainer.epsilon, losses[-1]))
                self.aff_plateau()

            if e > 0 and e % snapshot == 0:
                trainer.save(id='iteration-%s' % e)

        return scores, losses, epsilons

pioche = Pioche()
joueur = JoueurIA(pioche.piocheJeton(), pioche.piocheJeton(), pioche.piocheJeton(), pioche.piocheJeton())
trainer = Trainer(learning_rate=0.001, epsilon_decay=0.9999999995)
scores, losses, epsilons = joueur.train(35000, trainer, True, snapshot=2500)
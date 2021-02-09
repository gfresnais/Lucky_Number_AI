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
        self.jeton = Jeton()
        self.trainer = Trainer(learning_rate=0.001, epsilon_decay=0.9999995)

    def play_random(self, new_jeton):
        return self.play(new_jeton, True)

    def play(self, new_jeton, random=True):
        self.newJeton(new_jeton)
        check = False
        if random :
            while not check:
                position = self.trainer.randomAction()
                newPlateau, _, _, check, defausse = self.poseJeton(self.jeton, position)
            self.plateau = newPlateau
        else:
            while not check:
                plateau = self.getState()
                position = self.trainer.bestAction(plateau, False)
                newPlateau, _, _, check, defausse = self.poseJeton(self.jeton, position)
            self.plateau = newPlateau
        return defausse

    def get_plateau(self):
        return self.plateau

    def verification(self, newPlateau, ligne, colonne):
        number = newPlateau[ligne][colonne].number
        if ligne != 0:
            for testLigne in range(ligne):
                if newPlateau[testLigne][colonne].number != 0:
                    if number <= newPlateau[testLigne][colonne].number:
                        return False

        if colonne != 0:
            for testColone in range(colonne):
                if newPlateau[ligne][testColone].number != 0:
                    if number <= newPlateau[ligne][testColone].number:
                        return False

        if ligne != 3:
            for testLigne in range(ligne+1, 4):
                if newPlateau[testLigne][colonne].number != 0:
                    if number >= newPlateau[testLigne][colonne].number:
                        return False

        if colonne != 3:
            for testColone in range(colonne + 1, 4):
                if newPlateau[ligne][testColone].number != 0:
                    if number >= newPlateau[ligne][testColone].number:
                        return False
        return True

    def getState(self, getJeton=True):
        state = []
        for i in range(4):
            for j in range(4):
                state.append(self.plateau[i][j].number)
        if getJeton:
            state.append(self.jeton.number)
            state = np.reshape(state, (-1,17))
        else:
            state = np.reshape(state, (-1,16))
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
        if self.verification(newPlateau, ligne, colonne):
            if self.checkWin(newPlateau):
                return newPlateau, 50, True, True, self.plateau[ligne][colonne]
            else:
                return newPlateau, 2, False, True, self.plateau[ligne][colonne]
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
                self.plateau[i][j] = NewState[index]
                index += 1

    def aff_plateau(self):
        for i in range(4):
            ligne = self.plateau[i]
            print("" + str(ligne[0].number) + " " + str(ligne[1].number) + " " + str(ligne[2].number) + " " + str(ligne[3].number))


#WIP
    def train(self, episodes, collecting=False, snapshot=5000):
        batch_size = 32
        scores = []
        global_counter = 0
        losses = [0]
        epsilons = []
        trainer = self.trainer

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
                    jeton = self.newJeton(pioche.piocheJetonIA())
                    state = self.getState()
                    # self.aff_plateau()
                    # print('jeton :' + str(jeton.number))
                    check = False
                    while not check:
                        position = trainer.randomAction()
                        # print(str(position))
                        newPlateau, reward, done, check, _ = self.poseJeton(jeton, position)
                        trainer.remember(state, position, reward)
                    self.plateau = newPlateau
                    if len(pioche.PIOCHE) == 0:
                        done = True
                #affichage
                # self.aff_plateau()
                # print("============================")

        print("Starting training")
        global_counter = 0
        for e in range(episodes + 1):
            pioche = Pioche()
            self.reset(pioche.piocheJeton(), pioche.piocheJeton(), pioche.piocheJeton(), pioche.piocheJeton())
            score = 0
            done = False
            steps = 0
            play = 0
            while not done:
                global_counter += 1
                jeton = self.newJeton(pioche.piocheJetonIA())
                state = self.getState()
                check = False
                while not check:
                    steps += 1
                    position = trainer.bestAction(state)
                    newPlateau, reward, done, check, defausse = self.poseJeton(jeton, position)
                    score += reward
                    trainer.remember(state, position, reward)
                self.plateau = newPlateau
                trainer.actu_epsilon()
                pioche.DefausseJeton(defausse)
                play += 1

                if global_counter % 100 == 0:
                    l = trainer.replay(batch_size)
                    losses.append(l)

                if done:
                    scores.append(score)
                    epsilons.append(trainer.epsilon)

            if e % 10 == 0:
                print("episode: {}/{}, moves: {}, play: {}, score: {}, epsilon: {}, loss: {}"
                      .format(e, episodes, steps, play, score, trainer.epsilon, losses[-1]))
                self.aff_plateau()
                print("===============")

            if e > 0 and e % snapshot == 0:
                trainer.save(id='iteration-%s' % e)

        return scores, losses, epsilons
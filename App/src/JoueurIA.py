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
    
    def __init__(self, firstJeton, secondJeton, thirdJeton, fourthJeton, name=None):
        #recuperation des jeton de debut de jeu du joueur
        setDeJeton = [firstJeton, secondJeton, thirdJeton, fourthJeton]
        #creation d'un plateau vide
        plateau = []
        for i in range(4):
            ligne = []
            for j in range(4):
                ligne.append(Jeton())
            plateau.append(ligne)
        # tri des jetons par ordre croissant
        setDeJeton.sort(key=lambda Jeton: Jeton.number)
        # position des jetons sur le plateau
        plateau[0][0] = setDeJeton[0]
        plateau[1][1] = setDeJeton[1]
        plateau[2][2] = setDeJeton[2]
        plateau[3][3] = setDeJeton[3]
        self.plateau = plateau
        self.jeton = Jeton()
        self.trainer = Trainer(name, learning_rate=0.001, epsilon_decay=0.999999)

    # appel de la fonction play avec le random activé
    def play_random(self, new_jeton):
        return self.play(new_jeton, True)

    # fait entierement joué l'IA juste en lui donnant un jeton en entrée
    def play(self, new_jeton, random=False):
        self.newJeton(new_jeton)
        check = False
        done = False
        if random :
            while not check:
                position = self.trainer.randomAction()
                newPlateau, _, done, check, defausse = self.poseJeton(self.jeton, position)
            self.plateau = newPlateau
        else:
            while not check:
                plateau = self.getState()
                position = self.trainer.bestAction(plateau, False)
                newPlateau, _, done, check, defausse = self.poseJeton(self.jeton, position)
            self.plateau = newPlateau
        return done, defausse

    # retourne le plateau du joueur
    def get_plateau(self):
        return self.plateau

    # vérifie le jeton sur la position donnée sur le plateau si il est conforme au regle
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

    # recupère l'etat du plateau et du jeton(choix) sous la forme d'un vecteur
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

    # change le jeton du joueur par celui piocher
    def newJeton(self, jeton):
        self.jeton = jeton
        return jeton

    # verifie si le joueur a gagner par son plateau
    def checkWin(self, plateau):
        for i in range(4):
            for j in range(4):
                if plateau[i][j].number == 0:
                    return False
        return True

    # pose le jeton sur une copie du plateau du joueur verifie avec vérification
    def poseJeton(self, jeton, position):
        newPlateau = copy.deepcopy(self.plateau)
        ligne = position // 4
        colonne = position % 4
        newPlateau[ligne][colonne] = jeton
        # différente sortie dependant des resultat pour recompenser une IA en entrainement
        if self.verification(newPlateau, ligne, colonne):
            if self.checkWin(newPlateau):
                return newPlateau, 50, True, True, self.plateau[ligne][colonne]
            else:
                return newPlateau, 2, False, True, self.plateau[ligne][colonne]
        else:
            return newPlateau, -1, False, False, Jeton() #faux jeton

    #reset le plateu du joueur et son jeton actuel avec un nouveau jeu
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

    # change le plateau actuel avec un nouveau plateau donné sous la forme de vecteur.
    def set_plateau(self, NewState):
        index = 0
        for i in range(4):
            for j in range(4):
                self.plateau[i][j] = NewState[index]
                index += 1

    #affichage du plateau du joueur dans la console
    def aff_plateau(self):
        for i in range(4):
            ligne = self.plateau[i]
            print("" + str(ligne[0].number) + " " + str(ligne[1].number) + " " + str(ligne[2].number) + " " + str(ligne[3].number))


    # entrainement de l'IA
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
                # nouvelle partie
                pioche = Pioche()
                self.reset(pioche.piocheJeton(), pioche.piocheJeton(), pioche.piocheJeton(), pioche.piocheJeton())
                done = False
                while not done: # tant que la partie n'est pas finie
                    steps += 1
                    jeton = self.newJeton(pioche.piocheJetonIA())
                    state = self.getState()
                    # self.aff_plateau()
                    # print('jeton :' + str(jeton.number))
                    check = False
                    while not check:#tant que le coup n'est pas bon
                        position = trainer.randomAction()
                        # print(str(position))
                        newPlateau, reward, done, check, _ = self.poseJeton(jeton, position)
                        trainer.remember(state, position, reward)
                    self.plateau = newPlateau
                #affichage
                # self.aff_plateau()
                # print("============================")

        # meme chose mais avec entrainement
        print("Starting training")
        global_counter = 0
        for e in range(episodes + 1): # un episode par partie
            #Creatiion des composants de la partie
            pioche = Pioche()
            self.reset(pioche.piocheJeton(), pioche.piocheJeton(), pioche.piocheJeton(), pioche.piocheJeton())
            score = 0
            done = False
            steps = 0
            play = 0
            while not done: # tant que la partie n'est pas finie
                global_counter += 1
                jeton = self.newJeton(pioche.piocheJetonIA())
                state = self.getState()
                check = False
                while not check: #tant que le coup n'est pas bon
                    steps += 1
                    position = trainer.bestAction(state)
                    newPlateau, reward, done, check, defausse = self.poseJeton(jeton, position)
                    score += reward
                    trainer.remember(state, position, reward)
                self.plateau = newPlateau
                trainer.actu_epsilon()
                pioche.DefausseJeton(defausse)
                play += 1

                if global_counter % 100 == 0:#entrainement toute les 100 parties
                    l = trainer.replay(batch_size)
                    losses.append(l)

                if done:#sauvegarde des scores
                    scores.append(score)
                    epsilons.append(trainer.epsilon)

            if e % 10 == 0:# affichage pour suivi des parties
                print("episode: {}/{}, moves: {}, play: {}, score: {}, epsilon: {}, loss: {}"
                      .format(e, episodes, steps, play, score, trainer.epsilon, losses[-1]))
                self.aff_plateau()
                print("===============")

            if e > 0 and e % snapshot == 0: # sauvegarde pendant l'entrainement parce que on ne sais jamais (j'ai eu une maj windows)
                trainer.save(id='iteration-%s' % e)

        return scores, losses, epsilons
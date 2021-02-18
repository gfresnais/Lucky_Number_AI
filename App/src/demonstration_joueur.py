from App.src.JoueurIA import JoueurIA
from App.src.Pioche import Pioche


def playing():
    #inittialisation des composant de la partie
    pioche = Pioche()
    joueur_random = JoueurIA(pioche.piocheJeton(), pioche.piocheJeton(), pioche.piocheJeton(), pioche.piocheJeton())#joueur qui joue totalement de facon aleatoire
    joueurIA = JoueurIA(pioche.piocheJeton(), pioche.piocheJeton(), pioche.piocheJeton(), pioche.piocheJeton(), "L3000")#joueur utilisnt le model de reseaux de neronne entrainé L3000


#Affichage des plateau de début du jeu des 2 joueurs
    print("Joueur Random :")
    for i in range(4):
        ligne = joueur_random.plateau[i]
        print("" + str(ligne[0].number) + " " + str(ligne[1].number) + " " + str(ligne[2].number) + " " + str(
            ligne[3].number))
    print("==========================================================")
    print("\t\t\t\t\tJoueur IA :")
    for i in range(4):
        ligne = joueurIA.plateau[i]
        print("\t\t\t\t\t" + str(ligne[0].number) + " " + str(ligne[1].number) + " " + str(
            ligne[2].number) + " " + str(
            ligne[3].number))
    print("==========================================================")

    #initialisation des variables utils
    switch = 0 # variable indiquant quel joueur joue
    done = False # variable pour indiquer la fin de partie

    # VAriable pour connaitre le taux de coup aléatoire joué par l'IA
    r_count = 0 # conteur de coup aléatoire pour l'IA joueuse
    count = 0   #conteur de coup pour l'IA Joueuse

    while not done:
        # on utilise la variable joueur pour manipuler les 2 joueurs
        if switch == 0: # 0 = joueur random
            joueur = joueur_random
        else:   # sinon 1 = joueur IA
            joueur = joueurIA

        jeton = joueur.newJeton(pioche.piocheJetonIA()) # tirage d'un nouveau jeton

        if switch == 0:
            done, defausse = joueur.play_random(jeton) # coup random
        else:
            # coup joué par l'IA
            check = False # le coup a-t-il bien été joué
            random = False # le coup est-il aléatoire

            while not check:
                state = joueur.getState() #recuperation du vecteur d'entrée
                if not random: #premiere tentative par réponse du reseau
                    position = joueur.trainer.bestAction(state)
                    newPlateau, _, done, check, defausse = joueur.poseJeton(joueur.jeton, position)
                else:# autre tentative par l'aleatoire
                    position = joueur.trainer.randomAction()
                    newPlateau, _, done, check, defausse = joueur.poseJeton(joueur.jeton, position)
                if not check: # si le coup n'est pas bon on passe en aleatoire
                    random = True
            joueur.plateau = newPlateau

            # Une fois que le coup est bon
            if random: #si il est random
                r_count += 1
            count += 1 # tout les cas

        pioche.DefausseJeton(defausse) # on recupère le jeton remplacé par le nouveau et on le rentre dans la defausse

        #affichage du plateau
        if switch == 0:
            print("Joueur Random :")
            for i in range(4):
                ligne = joueur.plateau[i]
                print("" + str(ligne[0].number) + " " + str(ligne[1].number) + " " + str(ligne[2].number) + " " + str(
                    ligne[3].number))
            print("==========================================================")
        else:
            print("\t\t\t\t\tJoueur IA :")
            for i in range(4):
                ligne = joueur.plateau[i]
                print("\t\t\t\t\t" + str(ligne[0].number) + " " + str(ligne[1].number) + " " + str(ligne[2].number) + " " + str(
                    ligne[3].number))
            print("==========================================================")

        # changement de joueur
        if switch == 0:
            switch = 1
        else:
            switch = 0

    # affichage du vainqueur
    if joueur == joueur_random:
        print("LE JOUEUR RANDOM REMPORTE LA PARTIE")
    else:
        print("LE JOUEUR IA REMPORTE LA PARTIE")
    # calcul du taux d'aléatoire
    taux_random = (100/count)*r_count
    print("taux de coup random joué : " + str(taux_random) + " %")

playing() #lancement de la partie de demonstration
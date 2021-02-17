from App.src.JoueurIA import JoueurIA
from App.src.Pioche import Pioche


def affiche(joueur):

    pass


def playing():
    pioche = Pioche()
    joueur_random = JoueurIA(pioche.piocheJeton(), pioche.piocheJeton(), pioche.piocheJeton(), pioche.piocheJeton())
    joueurIA = JoueurIA(pioche.piocheJeton(), pioche.piocheJeton(), pioche.piocheJeton(), pioche.piocheJeton(), "L3000")


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

    switch = 0
    done = False

    while not done:
        if switch == 0:
            joueur = joueur_random
        else:
            joueur = joueurIA

        jeton = joueur.newJeton(pioche.piocheJetonIA())

        if switch == 0:
            done, defausse = joueur.play_random(jeton)
        else:
            joueur.trainer.epsilon = 0.39954
            joueur.newJeton(jeton)
            check = False
            while not check:
                plateau = joueur.getState()
                position = joueur.trainer.bestAction(plateau)
                newPlateau, _, done, check, defausse = joueur.poseJeton(joueur.jeton, position)
            joueur.plateau = newPlateau
        pioche.DefausseJeton(defausse)

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

        if switch == 0:
            switch = 1
        else:
            switch = 0

    if joueur == joueur_random:
        print("LE JOUEUR RANDOM REMPORTE LA PARTIE")
    else:
        print("LE JOUEUR IA REMPORTE LA PARTIE")

playing()
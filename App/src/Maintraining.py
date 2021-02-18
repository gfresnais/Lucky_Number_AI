from App.src.JoueurIA import JoueurIA
from App.src.Pioche import Pioche

pioche = Pioche()#Création d'un pioche pour init le joueur
joueur = JoueurIA(pioche.piocheJeton(), pioche.piocheJeton(), pioche.piocheJeton(), pioche.piocheJeton())#Création du joueur
joueur.trainer.model.summary()# Affichage sommaire de la structure du model de reseaux de neuronne
scores, losses, epsilons = joueur.train(5000, True, snapshot=1000)  #Entrainement de l'IA
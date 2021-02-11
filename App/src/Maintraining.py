from App.src.JoueurIA import JoueurIA
from App.src.Pioche import Pioche

pioche = Pioche()
joueur = JoueurIA(pioche.piocheJeton(), pioche.piocheJeton(), pioche.piocheJeton(), pioche.piocheJeton())
joueur.trainer.model.summary()
scores, losses, epsilons = joueur.train(5000, True, snapshot=1000)
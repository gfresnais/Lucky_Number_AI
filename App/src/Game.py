from App.src.Jeton import Jeton
from App.src.Joueur import Joueur
from App.src.JoueurIA import JoueurIA
from App.src.Pioche import Pioche


class Game:

    def __init__(self):
        self.pioche = Pioche()
        self.jeton = Jeton()
        self.joueur = Joueur(self.pioche.piocheJeton(), self.pioche.piocheJeton(), self.pioche.piocheJeton(), self.pioche.piocheJeton())
        self.joueurIA = JoueurIA(self.pioche.piocheJeton(), self.pioche.piocheJeton(), self.pioche.piocheJeton(), self.pioche.piocheJeton())

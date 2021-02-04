from App.src.Jeton import Jeton
from App.src.Joueur import Joueur
from App.src.Pioche import Pioche


class Game:

    def __init__(self):
        self.pioche = Pioche()
        self.jeton = Jeton()
        self.joueur = Joueur(self.pioche.piocheJeton(), self.pioche.piocheJeton(), self.pioche.piocheJeton(), self.pioche.piocheJeton())
        self.JoueurIA(self.pioche.piocheJeton(), self.pioche.piocheJeton(), self.pioche.piocheJeton(), self.pioche.piocheJeton())


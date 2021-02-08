# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 14:00:44 2021

@author: vallee
"""

import json
import random

from App.src.Jeton import Jeton


class Pioche:
    
    PIOCHE = []
    DEFAUSSE = []
    
    def __init__(self):
        #Tableau de toute les valeurs des jetons. C'est moche mais ça fonctionne pour le moment
        list = [[1,"Rouge"],[2,"Rouge"],[3,"Rouge"],[4,"Rouge"],[5,"Rouge"],[6,"Rouge"],[7,"Rouge"],[8,"Rouge"],[9,"Rouge"],[10,"Rouge"],[11,"Rouge"],[12,"Rouge"],[13,"Rouge"],[14,"Rouge"],[15,"Rouge"],[16,"Rouge"],[17,"Rouge"],[18,"Rouge"],[19,"Rouge"],[20,"Rouge"],[1,"jaune"],[2,"jaune"],[3,"jaune"],[4,"jaune"],[5,"jaune"],[6,"jaune"],[7,"jaune"],[8,"jaune"],[9,"jaune"],[10,"jaune"],[11,"jaune"],[12,"jaune"],[13,"jaune"],[14,"jaune"],[15,"jaune"],[16,"jaune"],[17,"jaune"],[18,"jaune"],[19,"jaune"],[20,"jaune"],[1,"vert"],[2,"vert"],[3,"vert"],[4,"vert"],[5,"vert"],[6,"vert"],[7,"vert"],[8,"vert"],[9,"vert"],[10,"vert"],[11,"vert"],[12,"vert"],[13,"vert"],[14,"vert"],[15,"vert"],[16,"vert"],[17,"vert"],[18,"vert"],[19,"vert"],[20,"vert"],[1,"violet"],[2,"violet"],[3,"violet"],[4,"violet"],[5,"violet"],[6,"violet"],[7,"violet"],[8,"violet"],[9,"violet"],[10,"violet"],[11,"violet"],[12,"violet"],[13,"violet"],[14,"violet"],[15,"violet"],[16,"violet"],[17,"violet"],[18,"violet"],[19,"violet"],[20,"violet"]]
        for i in range(len(list)):
            jeton = Jeton(list[i][0], list[i][1])
            self.PIOCHE.append(jeton)
    
    #fonction qui pioche un jeton dans la pioche et le retourne
    def piocheJeton(self):
        index = random.randrange(len(self.PIOCHE))
        return self.PIOCHE.pop(index)
        
    #fonction qui pioche un jeton donné dans la défausse
    def piocheDefausse(self, jeton):
        index = self.PIOCHE.index(jeton)
        
        return self.PIOCHE.pop(index)
    
    #fonction qui ajoute un jeton à la défausse
    def DefausseJeton(self, jeton):
        if jeton.number != 0:
            self.PIOCHE.append(jeton)

    # fonction qui pioche un jeton dans la pioche et le retourne
    def piocheJetonIA(self):
        if len(self.PIOCHE) != 0:
            index = random.randrange(len(self.PIOCHE))
            return self.PIOCHE.pop(index)
        else:
            index = random.randrange(len(self.DEFAUSSE))
            return self.DEFAUSSE.pop(index)
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
        list = [[1,"red"],[2,"red"],[3,"red"],[4,"red"],[5,"red"],[6,"red"],[7,"red"],[8,"red"],[9,"red"],[10,"red"],[11,"red"],[12,"red"],[13,"red"],[14,"red"],[15,"red"],[16,"red"],[17,"red"],[18,"red"],[19,"red"],[20,"red"],[1,"yellow"],[2,"yellow"],[3,"yellow"],[4,"yellow"],[5,"yellow"],[6,"yellow"],[7,"yellow"],[8,"yellow"],[9,"yellow"],[10,"yellow"],[11,"yellow"],[12,"yellow"],[13,"yellow"],[14,"yellow"],[15,"yellow"],[16,"yellow"],[17,"yellow"],[18,"yellow"],[19,"yellow"],[20,"yellow"],[1,"green"],[2,"green"],[3,"green"],[4,"green"],[5,"green"],[6,"green"],[7,"green"],[8,"green"],[9,"green"],[10,"green"],[11,"green"],[12,"green"],[13,"green"],[14,"green"],[15,"green"],[16,"green"],[17,"green"],[18,"green"],[19,"green"],[20,"green"],[1,"purple"],[2,"purple"],[3,"purple"],[4,"purple"],[5,"purple"],[6,"purple"],[7,"purple"],[8,"purple"],[9,"purple"],[10,"purple"],[11,"purple"],[12,"purple"],[13,"purple"],[14,"purple"],[15,"purple"],[16,"purple"],[17,"purple"],[18,"purple"],[19,"purple"],[20,"purple"]]
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
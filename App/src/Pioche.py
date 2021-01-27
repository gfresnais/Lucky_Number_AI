# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 14:00:44 2021

@author: vallee
"""

import json
import random

class Pioche:
    
    PIOCHE = []
    DEFAUSSE = []
    
    def __init__(self):
        with open("pioche.json", "r") as read_file:
            list = json.load(read_file)
        for i in range(len(list)):
            jeton = list[i]
            self.PIOCHE.append(jeton)
    
    #fonction qui pioche un jeton dans la pioche et le retourne
    def piocheJeton(self):
        index = random.randrange(len(self.PIOCHE))
        print(self.PIOCHE[index])
        return self.PIOCHE.pop(index)
        
    #fonction qui pioche un jeton donné dans la défausse
    def piocheDefausse(self, jeton):
        index = self.PIOCHE.index(jeton)
        
        return self.PIOCHE.pop(index)
    
    #fonction qui ajoute un jeton à la défausse
    def DefausseJeton(self, jeton):
        self.PIOCHE.append(jeton)
    
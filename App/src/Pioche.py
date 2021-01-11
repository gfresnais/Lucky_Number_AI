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
            
        self.PIOCHE = json.load('Assets/pioche.json')
        print(self.PIOCHE)
    
    
    #fonction qui pioche un jeton dans la pioche et le retourne
    def pioche(self):
        taille = len(self.PIOCHE)
        index = random.Random()*taille
        
        return self.PIOCHE.pop(index)
        
    #fonction qui pioche un jeton donné dans la défausse
    def defausse(self, jeton):
        index = self.PIOCHE.index(jeton)
        
        return self.PIOCHE.pop(index)
    
    #fonction qui ajoute un jeton à la défausse
    def ajoutDefausse(self, jeton):
        self.PIOCHE.append(jeton)
    
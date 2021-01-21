# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 14:53:05 2021

@author: vallee
"""
import numpy as np

class Joueur:
    
    OLD_PLATEAU = np.eye(4,4,int())
    JETON = 0
    
    def __init__(self, 
                 firstNumber, 
                 secondNumber, 
                 thirdNumber, 
                 fourthNumber):
        setDeJeton = np.array([firstNumber,secondNumber,thirdNumber,fourthNumber])
        setDeJeton.sort()
        self.OLD_PLATEAU[0,0] = setDeJeton[0]
        self.OLD_PLATEAU[1,1] = setDeJeton[1]
        self.OLD_PLATEAU[2,2] = setDeJeton[2]
        self.OLD_PLATEAU[3,3] = setDeJeton[3]
    
    
    def verification(self, newPlateau):
        for colone in range(4):
            for ligne in range(4):
                if(self.OLD_PLATEAU[colone,ligne] != newPlateau[colone, ligne]):
                    number = newPlateau[colone, ligne]
                    if(colone != 0):
                        if(number <= newPlateau[colone-1, ligne]):
                            return False
                    if(ligne != 0):
                        if(number <= newPlateau[colone, ligne-1]):
                            return False
                    if(colone != 3):
                        if(number <= newPlateau[colone+1, ligne]):
                            return False
                    if(ligne != 3):
                        if(number <= newPlateau[colone, ligne+1]):
                            return False
                    self.OLD_PLATEAU = newPlateau
                    return True
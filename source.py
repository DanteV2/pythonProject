# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 15:32:23 2023
@author: jaspe
"""
import numpy as np


class source(object):

    def __init__(self, X, Y, Z):
        self.sX = X
        self.sY = Y
        self.sZ = Z
        self.S = np.array([self.sX, self.sY, self.sZ])

    def set_source(self):
        self.sX = float(input("give X position of Speaker : "))
        self.sY = float(input("give y position of Speaker : "))
        self.sZ = float(input("give z position of Speaker : "))
        self.S = np.array([self.sX, self.sY, self.sZ])

    def get_source(self):
        return self.S

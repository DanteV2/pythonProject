# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 15:31:16 2023
@author: jaspe
"""
import numpy as np


class Mic(object):

    def __init__(self, X, Y, Z):
        self.mX = X
        self.mY = Y
        self.mZ = Z
        self.M = np.array([self.mX, self.mY, self.mZ])

    def set_mic(self):
        self.mX = float(input("give X position of microphone : "))
        self.mY = float(input("give y position of microphone : "))
        self.mZ = float(input("give z position of microphone : "))
        self.M = np.array([self.mX, self.mY, self.mZ])

    def get_mic(self):
        return self.M

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 16:02:28 2023
@author: jaspe
"""
from __future__ import print_function

import math

import numpy as np
import sounddevice as sd


class dB_meating(object):
    def __init__(self, desired_db, T_interval, Weighting):
        self.desired_db = desired_db
        self.T_interval = T_interval
        self.Weighting = Weighting

    def measure_dB(self):  # window, weighting

        T = self.T_interval  # duration in seconds
        desired_dB = self.desired_db
        weight = self.Weighting
        fs = 44100  # sampling rate
        sd.default.samplerate = fs
        sd.default.channels = 1  # mono recording
        amp = 10 ** (desired_dB / 20)
        f = 6000

        # Generate the signal
        t = np.linspace(0, T, int(T * fs), False)
        signal = amp * np.sin(2 * np.pi * f * t)

        # Play the signal through the loudspeaker and measure the dB level through the microphone
        recording = sd.playrec(signal, fs, channels=1, dtype='float32', blocking=True)
        dB = 20 * np.log10(np.max(np.abs(recording)))

        # wait for recording to finish
        sd.wait()

        # calculate the measured dB value
        rms = np.sqrt(np.mean(np.square(recording)))
        measured_db = 20 * math.log10(rms / 0.00002)

        # calculate the difference between input and measured dB values
        db_diff = desired_dB - measured_db
        print("Difference between input and measured dB: {:.2f}".format(db_diff))
        print('the measured amouned of dB is: {:.2f}'.format(measured_db))

        return db_diff
    # example usage
# meter1 = dB_meating(60, 4, 'a')
# desired_dB = 6
# dB_diff = meter1.measure_dB(desired_dB, 4, 'a')
# print("Difference between input and measured dB: {:.2f}".format(dB_diff))

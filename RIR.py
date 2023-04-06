# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 15:33:48 2023
@author: jaspe
"""
import math
import random

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal
# import pyroomacoustics as pra
# from source import source
# from Mic import Mic
import sounddevice as sd
import soundfile as sf


def Test_RIR():
    f1 = 20  # starting frequency (Hz)
    f2 = 20000  # ending frequency (Hz)
    T = 2  # duration (seconds)
    fs = 44100  # sampling frequency

    # Generate the sine sweep
    t = np.linspace(0, T, int(T * fs), False)
    sine_sweep = signal.chirp(t, f1, T, f2, method='logarithmic')

    # Normalize the signal to 70 dB SPL
    ref_rms = 20e-6  # reference RMS amplitude for 0 dB SPL
    ref_p = ref_rms ** 2  # reference sound pressure for 0 dB SPL
    amp = np.sqrt(10 ** ((70 - 94) / 10) * ref_p)  # amplitude for 70 dB SPL
    sine_sweep = sine_sweep * amp / np.max(np.abs(sine_sweep))
    # play it 2x
    Loop = [sine_sweep, sine_sweep]

    # Play loop through the loudspeaker and record it through the microphone
    recording = sd.playrec(Loop, fs, channels=1,
                           dtype='float32', blocking=True)

    # Save the recorded signal to a WAV file
    sf.write('recording.wav', recording, fs)

    # Load the recorded signal and the sine sweep
    recording2, fs = sf.read('recording.wav')
    sine_sweep2 = signal.chirp(np.linspace(
        0, 1, len(recording)), f1, T, f2, method='logarithmic')


# plot the recording


def Clc_RIR(xx, yy):
    leng = 44100 * 2

    X = np.fft.fft(xx[len(xx) - leng + 1: len(xx)])
    Y = np.fft.fft(yy[len(yy) - leng + 1: len(yy)])

    # calculate frequency response by deviding microphone signal with actual signal

    H = np.divide(Y, X.T)

    # back to the time domain

    h_est = np.fft.ifft(H)

    fig, axs = plt.subplots(2, 2)
    axs[0, 0].plot(X[0:len(X) // 2])
    axs[0, 0].set_title('fft of sweep')
    axs[0, 1].plot(yy, 'tab:orange')
    axs[0, 1].set_title('filtered mic signal')
    axs[1, 0].plot(Y[0:len(Y) // 2], 'tab:green')
    axs[1, 0].set_title('fft of mic signal')
    axs[1, 1].plot(xx, 'tab:red')
    axs[1, 1].set_title('generated sweep')

    fig, axs = plt.subplots(2)
    axs[0].plot(yy)
    axs[0].set_title('raw mic signal')
    axs[1].plot(xx, 'tab:red')
    axs[1].set_title('original signal')

    fig, axs = plt.subplots(2)
    axs[0].plot(Y[0:len(Y) // 2])
    axs[0].set_title('fft microphone signal')
    axs[1].plot(X[0:len(X) // 2], 'tab:red')
    axs[1].set_title('fft original signal')

    fig, axs = plt.subplots(2)
    axs[0].plot(h_est[0: 10000])
    axs[0].set_title('estemated RIR')
    axs[1].plot(h, 'tab:orange')
    axs[1].set_title('generated RIR')


def Test_s_RIR():
    f1 = 20  # starting frequency (Hz)
    f2 = 20000  # ending frequency (Hz)
    T = 2  # duration (seconds)
    fs = 44100  # sampling frequency
    N = 10000
    leng = T * fs

    # make chirp signal from 20Hz - 20kHz

    t = np.linspace(0, T, int(T * fs), False)
    sine_sweep = signal.chirp(t, f1, T, f2, method='logarithmic')

    # make white noise
    i = 0
    x = []

    while i < leng:
        noise = random.normalvariate(0, 1)
        x.append(noise)
        i += 1

    # loop through it 2x to prevent errors

    xx = np.hstack((sine_sweep, sine_sweep))

    loop = x + x
    xx_ = np.array(loop).T

    # generate Room Impulse Response that needs to be estemated

    i = 0
    h_ = []
    h_.clear()
    while i < N:
        r = random.normalvariate(0, 1) * math.exp(-0.001 * i)
        h_.append(r)
        i += 1
    h = np.array(h_)

    # plot h
    plt.figure()
    plt.plot(h)
    plt.xlabel('samples')
    plt.ylabel('Magnitude')
    plt.title('rir')

    # plot xx

    plt.figure()
    plt.plot(xx)
    plt.xlabel('time')
    plt.ylabel('Magnitude')
    plt.title('chirp')

    # filter the signal with the impulse response to obtain 'mic' signal

    yy = signal.lfilter(h, 1, xx)

    # compute the fourier transorms of the signals but take only the last few samples

    X = np.fft.fft(xx[len(xx) - leng + 1: len(xx)])
    Y = np.fft.fft(yy[len(yy) - leng + 1: len(yy)])

    # calculate frequency response by deviding microphone signal with actual signal

    H = np.divide(Y, X.T)

    # back to the time domain

    h_est = np.fft.ifft(H)
    error = []
    i = 0
    while i < N:
        e = np.linalg.norm(h[i] - h_est[i]) / np.linalg.norm(h)
        error.append(e)
        i += 1
    err = np.linalg.norm(h - h_est[0: N]) / np.linalg.norm(h)

    fig, axs = plt.subplots(2, 2)
    axs[0, 0].plot(X[0:len(X) // 2])
    axs[0, 0].set_title('fft of sweep')
    axs[0, 1].plot(yy, 'tab:orange')
    axs[0, 1].set_title('filtered mic signal')
    axs[1, 0].plot(Y[0:len(Y) // 2], 'tab:green')
    axs[1, 0].set_title('fft of mic signal')
    axs[1, 1].plot(xx, 'tab:red')
    axs[1, 1].set_title('generated sweep')

    fig, axs = plt.subplots(2)
    axs[0].plot(yy)
    axs[0].set_title('raw mic signal')
    axs[1].plot(xx, 'tab:red')
    axs[1].set_title('original signal')

    fig, axs = plt.subplots(2)
    axs[0].plot(Y[0:len(Y) // 2])
    axs[0].set_title('fft microphone signal')
    axs[1].plot(X[0:len(X) // 2], 'tab:red')
    axs[1].set_title('fft original signal')

    fig, axs = plt.subplots(2)
    axs[0].plot(h_est[0: 10000])
    axs[0].set_title('estemated RIR')
    axs[1].plot(h, 'tab:orange')
    axs[1].set_title('generated RIR')

    print(err)
    plt.figure()
    plt.plot(error)
    plt.xlabel('samples')
    plt.ylabel('Magnitude')
    plt.title('error')

"""
Created on Thu Mar 23 15:33:48 2023
@author: jaspe
"""
import matplotlib.pyplot as plt
import numpy as np
import pyroomacoustics as pra
import scipy.signal as signal
import sounddevice as sd
import soundfile as sf

from Mic import Mic
from source import source


class Room(object):
    def __init__(self, c1x, c1y, c2x, c2y, c3x, c3y, c4x, c4y, hight):
        self.c1x = c1x
        self.c1y = c1y

        self.c2x = c2x
        self.c2y = c2y

        self.c3x = c3x
        self.c3y = c3y

        self.c4x = c4x
        self.c4y = c4y
        self.hight = hight

        self.corner = np.array(
            [[self.c1x, self.c1y], [self.c2x, self.c2y], [self.c3x, self.c3y], [self.c4x, self.c4y]]).T
        self.room = pra.Room.from_corners(self.corner)

    def set_room(self):
        self.c1x = input("give X position of first corner: ")
        self.c1y = input("give y position of first corner: ")

        self.c2x = input("give X position of second corner: ")
        self.c2y = input("give y position of second corner: ")

        self.c3x = input("give X position of third corner: ")
        self.c3y = input("give y position of third corner: ")

        self.c4x = input("give X position of fourth corner: ")
        self.c4y = input("give y position of fourth corner: ")
        self.hight = input("hight of the room in m: ")
        self.corner = np.array(
            [[self.c1x, self.c1y], [self.c2x, self.c2y], [self.c3x, self.c3y], [self.c4x, self.c4y], ]).T

    def get_corner(self):
        return self.corner

    def get_RIR(size, absorption):
        if absorption == 'high':
            absor = 0.7
        elif absorption == 'medium':
            absor = 0.3
        elif absorption == 'low':
            absor = 0.1
        else:
            raise ValueError("The absorption parameter can only take values ['low', 'medium', 'high']")

        if size == 'large':
            size_coef = 5.
        elif size == 'medium':
            size_coef = 2.5
        elif size == 'small':
            size_coef = 1.
        else:
            raise ValueError("The size parameter can only take values ['small', 'medium', 'large']")

        # initialize room
        m = Mic(1, 1, 1)
        s = source(4, 3, 1)
        r = Room(0, 0, 0, 4, 4, 4, 4, 0, 3)

        # m.set_Mic()
        # s.set_source()
        # r.set_corner()

        r.room = size_coef * pra.Room.from_corners(r.corner)
        # r.room = pra.Room.from_corners(r.corner)
        # Create the 3D room by extruding the 2D by a specific height
        r.room.extrude(size_coef * 2.5, absorption=absor)
        # r.room.extrude(r.hight, absorption=absor)

        # add speaker
        r.room.add_source(size_coef * s.get_source())
        # r.room.add_source(s.get_source())

        # add microphone
        r.room.add_microphone_array(pra.MicrophoneArray(size_coef * [[m.M[0]], [m.M[1]]], r.room.fs))
        # r.room.add_microphone([[m.M[0]], [m.M[1]], [m.M[2]]], r.room.fs)

        # compute RIR
        r.room.compute_rir()
        print(r.room.compute_rir())
        r.room.plot()
        plt.title("3D shape of the room with microphone, source and images")
        plt.show()

        # Plot and apply the RIR on the audio file
        r.room.plot_rir()
        plt.title("Impulse response of room")
        plt.show()
        # r.room.plot_rir(FD = True)
        # plt.title("transfer function of room")
        # plt.show()
        # r.room.simulate()
        # r.room.mic_array.to_wav('aaa.wav', norm=True, bitdepth=np.int16)

    # # Display the audio file
    # fs_result, result = wavfile.read('aaa.wav')
    # IPython.display.display(IPython.display.Audio(result, rate=fs_result))


def Test_RIR():
    f1 = 20  # starting frequency (Hz)
    f2 = 20000  # ending frequency (Hz)
    T = 2  # duration (seconds)
    fs = 44100  # sampling frequency

    # Generate the sine sweep
    t = np.linspace(0, T, int(T * fs), False)
    sine_sweep = signal.chirp(t, f1, T, f2, method='logarithmic')

    # Play the sine sweep through the loudspeaker and record it through the microphone
    recording = sd.playrec(sine_sweep, fs, channels=1,
                           dtype='float32', blocking=True)

    # Save the recorded signal to a WAV file
    sf.write('recording.wav', recording, fs)

    # Load the recorded signal and the sine sweep
    recording2, fs = sf.read('recording.wav')
    sine_sweep2 = signal.chirp(np.linspace(
        0, 1, len(recording)), f1, T, f2, method='logarithmic')

    # plot the recording

    # Use the sweep-sine method to measure the RIR
    X = np.fft.fft(sine_sweep2)
    Y = np.fft.fft(recording2)
    H = Y / X
    rir = np.fft.ifft(H)

    # Normalize the RIR to have unit energy
    rir /= np.sqrt(np.sum(np.square(rir)))

    # Plot the RIR
    plt.title("rir")
    plt.xlabel("X axis")
    plt.ylabel("Y axis")
    plt.plot(t, rir, color="red")
    plt.show()

    fig, axs = plt.subplots(2, 2)
    axs[0, 0].plot(X[: len(X) // 2])
    axs[0, 0].set_title('fft of sweep')
    axs[0, 1].plot(t, recording2, 'tab:orange')
    axs[0, 1].set_title('recorded audio of sweep')
    axs[1, 0].plot(Y[: len(Y) // 2], 'tab:green')
    axs[1, 0].set_title('fft of recorded audio')
    axs[1, 1].plot(t, sine_sweep2, 'tab:red')
    axs[1, 1].set_title('generated sweep')

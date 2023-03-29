from __future__ import print_function

import math

import matplotlib.pyplot as plt
import numpy as np
import pyroomacoustics as pra
import sounddevice as sd
import soundfile as sf

from Mic import Mic
from Room import Room
from source import source


class RIR(object):
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
        # r.room.add_source(size_coef * s.get_source())
        # r.room.add_source(s.get_source())

        # add microphone
        # r.room.add_microphone_array(pra.MicrophoneArray(size_coef * [[m.M[0]], [m.M[1]]], r.room.fs))
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

    def Test_RIR(self):

        # Set up parameters
        fs = 44100  # Hz
        duration = 5  # seconds
        recording_file = 'recording.wav'

        # Generate an impulse signal chirp of multisinus (2x achter elkaar) is beter - fft voor impulse response
        impulse = np.zeros(int(fs * duration))
        i = 0
        while i < 100:
            if i % 2 == 0:
                impulse[i] = 100000
            else:
                impulse[i] = -100000

        # Play the impulse signal through the default audio output device
        sd.play(impulse, fs)

        # Record the resulting sound using a microphone
        recording = sd.rec(int(fs * duration), fs, channels=1)
        sd.wait()

        # Save the recording to a file
        sf.write(recording_file, recording, fs)

        # Load the recording from the file
        recording, fs = sf.read(recording_file)

        # Compute the impulse response
        impulse_response = np.correlate(recording.squeeze(), impulse, mode='full')

        # Save the impulse response to a file
        sf.write('impulse_response.wav', impulse_response, fs)
        impulse_response.plot


def measure_dB(desired_dB, T, weight):  # window, weighting

    duration = T  # duration in seconds
    fs = 44100  # sampling rate
    sd.default.samplerate = fs
    sd.default.channels = 1  # mono recording

    # record audio
    recording = sd.rec(int(duration * fs))

    # wait for recording to finish
    sd.wait()

    # calculate the measured dB value
    rms = np.sqrt(np.mean(np.square(recording)))
    measured_db = 20 * math.log10(rms / 0.00002)

    # calculate the difference between input and measured dB values
    db_diff = desired_dB - measured_db
    print(db_diff)
    print(measured_db)

    return db_diff


# example usage

desired_dB = 60
db_diff = measure_dB(desired_dB, 4, 'A')
print("Difference between input and measured dB: {:.2f}".format(db_diff))

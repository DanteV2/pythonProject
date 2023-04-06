import wave

import pyaudio


def record1(outputFile):
    fs = 44100  # sampling frequency
    Duration = 50  # 5sec

    audio = pyaudio.PyAudio()

    stream = audio.open(format=pyaudio.paInt32, channels=1, rate=fs, input=True, frames_per_buffer=1024)

    print("Recording...")

    frames = []

    for i in range(0, int(4410 / 1024 * Duration)):
        data = stream.read(1024)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    sound_file = wave.open(outputFile, 'wb')
    sound_file.setnchannels(1)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt32))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames))  # combining data into 1 big thing
    sound_file.close()


def play(file):
    fs = 4410
    wf = wave.open(file, 'rb')
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt32, channels=1, rate=fs, input=True, frames_per_buffer=1024)
    data = wf.readframes(1024)

    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(1024)

    stream.stop_stream()
    stream.close()
    audio.terminate()


play('test1.wav')

#from __future__ import print_function

import sys, os
import wave

import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import audioread
import contextlib

from pydub import AudioSegment

"""
FORMAT = pyaudio.paInt16                # We use 16bit format per sample
CHANNELS = 1
RATE = 44100
CHUNK = 1024                            # 1024bytes of data red from a buffer
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "file.wav"

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    #print(type(data))
    #print(type(frames))
    frames.append(data)
#print(frames)
bframes = bytes(frames)
#frames = ''.join(frames)

stream.stop_stream()
stream.close()
audio.terminate()

fig = plt.figure()
s = fig.add_subplot(111)
amplitude = numpy.fromstring(bframes, numpy.int16)
s.plot(amplitude)
fig.savefig('fig.png')
"""

def print_from_stream():
    #It works !
    FORMAT = pyaudio.paInt16  # We use 16bit format per sample
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024  # 1024bytes of data red from a buffer
    RECORD_SECONDS = 3
    #WAVE_OUTPUT_FILENAME = "file.wav"

    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)


    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        # print(type(data))
        # print(type(frames))
        frames.append(data)
    # print(frames)
    #bframes = bytes(frames)
    print(type(frames[0]))
    frames = b''.join(frames)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    fig = plt.figure()
    s = fig.add_subplot(111)
    amplitude = np.fromstring(frames, np.int16)
    s.plot(amplitude)
    # Only display positive y-values
    s.set_ylim(bottom=0.)
    fig.savefig("learn/static/learn/fig/teststream.png")

def print_from_mp3(file, lang):
    #It works !
    path = "learn/static/learn/audio/"+lang+"/"+file+".mp3"
    sound = AudioSegment.from_mp3(path)
    # get raw audio data as a bytestring
    raw_data = sound.raw_data
    # get the frame rate
    sample_rate = sound.frame_rate
    # get amount of bytes contained in one sample
    sample_size = sound.sample_width
    # get channels
    channels = sound.channels

    fig = plt.figure()
    s = fig.add_subplot(111)
    amplitude = np.fromstring(raw_data, np.int16)
    s.plot(amplitude)
    #Only display positive y-values
    s.set_ylim(bottom=0.)
    fig.savefig("learn/static/learn/fig/"+file+".png")


def decode(filename):


    AudioSegment.converter = "C:/Users/Foot/Softs/ffmpeg/bin/ffmpeg.exe"
    AudioSegment.ffmpeg = "C:/Users/Foot/Softs/ffmpeg/bin/ffmpeg.exe"

    #filename = "learn/static/learn/audio/hello-jp"
    #print(filename+".mp3")
    if not os.path.exists(filename+".mp3"):
        print('Pas de fichier')
        print("File not found.", file=sys.stderr)
        sys.exit(1)

    #sound = AudioSegment.from_mp3(filename+".mp3")


    sound = AudioSegment.from_mp3(filename+".mp3")
    sound.export(filename+".wav", format="wav")


def main():
    filename = "learn/static/learn/audio/hello-jp"
    #decode(filename)
    #print_from_mp3("goodbye-jp", 'jp')
    print_from_stream()



if __name__ == '__main__':
    main()
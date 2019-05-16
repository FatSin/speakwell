#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the streaming API.

NOTE: This module requires the additional dependency `pyaudio`. To install
using pip:

    pip install pyaudio

Example usage:
    python transcribe_streaming_mic.py
"""

# [START import_libraries]
from __future__ import division

import re, sys, io, os

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue

#from . import draw_graph as draw

# [END import_libraries]

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

#Media directory configuration

#if os.environ.get('ENV') == 'PRODUCTION':
#    MEDIA_DIR = 'speakwell/staticfiles/'
#else:
#    MEDIA_DIR = 'learn/static/'
MEDIA_DIR = 'learn/media/'

"""Draw Graph import"""

import sys, os
import wave

import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import audioread
import contextlib

from pydub import AudioSegment


def mp3_to_wav(file):
    sound = AudioSegment.from_ogg(file)
    wav_file = MEDIA_DIR+"learn/audio/user.wav"
    sound = sound.set_channels(1)
    sound = sound.set_frame_rate(16000)
    sound.export(wav_file, format="wav")
    return wav_file

def print_from_mp3(word, lang, is_from_mic):
    if is_from_mic:
        path = MEDIA_DIR+"learn/audio/user.mp3"
        fig_path = MEDIA_DIR+"learn/fig/user.png"
        sound = AudioSegment.from_ogg(path)
        label = 'You are here'
    else:
        path = MEDIA_DIR+"learn/audio/"+lang+"/"+word+"-"+lang+".mp3"
        if os.path.exists(path):
            sound = AudioSegment.from_mp3(path)
        else:
            path = MEDIA_DIR+"learn/audio/" + lang + "/" + word + "-" + lang + ".wav"
            if os.path.exists(path):
                sound = AudioSegment.from_wav(path)
            else:
                path = MEDIA_DIR+"learn/audio/" + lang + "/" + word + "-" + lang + ".ogg"
                if os.path.exists(path):
                    sound = AudioSegment.from_ogg(path)
                else:
                    sound = b''

        fig_path = MEDIA_DIR+"learn/fig/"+lang+"/"+word+"-"+lang+".png"
        label = 'Reference'


    #sound = AudioSegment.from_mp3(path)
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
    s.set_ylim(bottom=0.) #Only display positive y-values
    s.set_xticklabels([])
    s.set_yticklabels([])
    s.set_xlabel(label)
    fig.savefig(fig_path)


def print_from_wav(word, lang):
    path = MEDIA_DIR+"learn/audio/"+lang+"/"+word+"-"+lang+".wav"
    sound = AudioSegment.from_wav(path)
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
    fig.savefig(MEDIA_DIR+"learn/fig/"+lang+"/"+word+"-"+lang+".png")

def print_from_cloud(object):

    """
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
    """

    #stream.stop_stream()
    #stream.close()

    RECORD_SECONDS = 5

    #stream = object._audio_stream

    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        #We chose RECORD_SECONDS =
        data = object.read(CHUNK)
        # print(type(data))
        # print(type(frames))
        frames.append(data)
    # print(frames)
    # bframes = bytes(frames)
    print(type(frames[0]))
    frames = b''.join(frames)

    fig = plt.figure()
    s = fig.add_subplot(111)
    amplitude = np.fromstring(frames, np.int16)
    s.plot(amplitude)
    # Only display positive y-values
    s.set_ylim(bottom=0.)
    fig.savefig(MEDIA_DIR+"learn/fig/testcloud.png")



############################

def recognition_from_file(stream_file, lang):
    """Streams transcription of the given audio file."""
    stream_file = mp3_to_wav(stream_file)

    client = speech.SpeechClient()

    with io.open(stream_file, 'rb') as audio_file:
        content = audio_file.read()
        #print(content)

    # In practice, stream should be a generator yielding chunks of audio data.
    stream = [content]
    requests = (types.StreamingRecognizeRequest(audio_content=chunk)
                for chunk in stream)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=lang)
    streaming_config = types.StreamingRecognitionConfig(config=config)

    # streaming_recognize returns a generator.
    responses = client.streaming_recognize(streaming_config, requests)
    print(responses)

    for response in responses:
        # Once the transcription has settled, the first result will contain the
        # is_final result. The other results will be for subsequent portions of
        # the audio.
        print('Parsing responses')
        for result in response.results:
            print('Parsing results')
            print('Finished:')
            print(result.is_final)
            print('stability:')
            print(result.stability)
            #print('Finished: {}'.format(result.is_final))
            #print('Stability: {}'.format(result.stability))
            alternatives = result.alternatives
            # The alternatives are ordered from most likely to least.
            for alternative in alternatives:
                print('Confidence: {}'.format(alternative.confidence))
                print(u'Transcript: {}'.format(alternative.transcript))
        result = response.results[0]
        #print(result)
        transcript = result.alternatives[0].transcript
        score = str(result.alternatives[0].confidence * 100)
        print('Transcript: {0}, Score: {1}'.format(transcript, score))
        return [transcript, score]



#Réécriture du générateur 'requests' du main, pour pv en 1 seule boucle récup le son pour
# 1)pv le grapher 2) pv l'envoyer au cloud
def req_gen(gen, alist):
    for content in gen:
        alist.append(content)
        yield types.StreamingRecognizeRequest(audio_content=content)



class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):

        #Added
        #print(self.closed)
        #print_from_cloud(self._audio_stream) #not working here..
        #print("exiting")
        #print(self.closed)

        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            #yield b''.join(data)

            #Added

            frames = b''.join(data)

            yield frames
        """
        fig = plt.figure()
        s = fig.add_subplot(111)
        amplitude = np.fromstring(frames, np.int16)
        s.plot(amplitude)
        ## Only display positive y-values
        s.set_ylim(bottom=0.)
        fig.savefig("static/learn/fig/testcloud.png")
        #fig.savefig("testcloud.png")
        """



    #Attempt as a callback function
    def print_from_cloud_callb(self):
        RECORD_SECONDS = 5

        # stream = object._audio_stream

        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            # We chose RECORD_SECONDS =
            data = self._audio_stream.read(CHUNK)
            # print(type(data))
            # print(type(frames))
            frames.append(data)
        # print(frames)
        # bframes = bytes(frames)
        print(type(frames[0]))
        frames = b''.join(frames)

        fig = plt.figure()
        s = fig.add_subplot(111)
        amplitude = np.fromstring(frames, np.int16)
        s.plot(amplitude)
        # Only display positive y-values
        s.set_ylim(bottom=0.)
        fig.savefig(MEDIA_DIR+"learn/fig/testcloud.png")


# [END audio_stream]


def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        # changed
        # transcript = result.alternatives[0].transcript
        ##transcript = result.alternatives[0].transcript +" "+  str(result.alternatives[0].confidence*100)
        transcript = result.alternatives[0].transcript + " " + str(result.alternatives[0].confidence * 100)

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            # print(transcript.encode('utf-8').decode('utf-8') + overwrite_chars.encode('utf-8').decode('utf-8'))
            print(transcript + overwrite_chars)
            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            break

            ##if re.search(r'\b(exit|quit)\b', transcript, re.I):
            ##    print('Exiting..')
            ##    break

            num_chars_printed = 0


def listen_print_single(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        # changed
        # transcript = result.alternatives[0].transcript
        ##transcript = result.alternatives[0].transcript +" "+  str(result.alternatives[0].confidence*100)
        transcript = result.alternatives[0].transcript
        score = str(result.alternatives[0].confidence * 100)

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + " " + score + overwrite_chars + '\r')
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            # print(transcript.encode('utf-8').decode('utf-8') + overwrite_chars.encode('utf-8').decode('utf-8'))
            print(transcript + " " + score + overwrite_chars)
            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..')

            return [transcript, score]
            break
            #num_chars_printed = 0


def main():
    # See http://g.co/cloud/speech/docs/languages
    # for a list of supported languages.
    # changed
    # language_code = 'en-US'  # a BCP-47 language tag
    #language_code = 'en-US'
    #language_code = 'fr-FR'
    language_code = 'ja-JP'
    #language_code = 'ru-RU'

    client = speech.SpeechClient()
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
        #Added but might have to put disable for expressions
        single_utterance=True)

    frames = []

    with MicrophoneStream(RATE, CHUNK) as stream:
        print(stream.closed)
        audio_generator = stream.generator()


        ##requests = (types.StreamingRecognizeRequest(audio_content=content)
        ##            for content in audio_generator)
        requests = req_gen(audio_generator, frames)

        #frames = (content for content in audio_generator)


        responses = client.streaming_recognize(streaming_config, requests)


        print(stream.closed)
        # Now, put the transcription responses to use.

        #Added
        #stream.print_from_cloud_callb()
        #print_from_cloud(stream._audio_stream)

        data = listen_print_single(responses)
        print(stream.closed)


        #listen_print_loop(responses)

    #other_gen = list(audio_generator)

    print(len(frames))
    #frames = list(frames)
    frames = b''.join(frames)

    fig = plt.figure()
    s = fig.add_subplot(111)
    amplitude = np.fromstring(frames, np.int16)
    s.plot(amplitude)
    # Only display positive y-values
    s.set_ylim(bottom=0.)
    #Test from local
    #fig.savefig('static/learn/fig/testcloud.png')
    fig.savefig(MEDIA_DIR+"learn/fig/testcloud.png")

    print(type(requests))
    print(type(responses))
    print(type(audio_generator))
    print(stream._audio_stream)

    #print_from_cloud(stream)

    print(data)
    return data


if __name__ == '__main__':
    #main()
    stream_file = MEDIA_DIR+"learn/audio/user.mp3"
    lang = 'ja-JP'
    recognition_from_file(stream_file, lang)
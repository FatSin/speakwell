import io, wave
from pydub import AudioSegment
import matplotlib.pyplot as plt
import numpy as np
from pydub.utils import mediainfo


def mp3_to_wav(file):
    print(mediainfo(file))
    sound = AudioSegment.from_ogg(file)
    #flac_file = "learn/static/learn/audio/user.flac"
    wav_file = "learn/static/learn/audio/dest.wav"
    print(sound.frame_rate)
    print(sound.channels)

    sound = sound.set_channels(1)
    sound = sound.set_frame_rate(16000)

    sound.export(wav_file, format="wav")
    print(sound.frame_rate)
    print(sound.channels)

    #sound.export(flac_file, format="flac")
    #sound2 = AudioSegment.from_wav(wav_file)
    #sound2 = sound2.set_frame_rate(16000)
    #sound2 = sound2.set_channels(1)
    #print(sound2.frame_rate)
    #print(sound2.channels)
    #sound2.export(wav_file, format="wav")

    #with wave.open(wav_file, "rb") as wave_file:
    #    frame_rate = wave_file.getframerate()
    #    channels = wave_file.getnchannels()
    return wav_file


def recognition_from_file(stream_file):
    """Streams transcription of the given audio file."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types


    stream_file = mp3_to_wav(stream_file)

    client = speech.SpeechClient()

    with io.open(stream_file, 'rb') as audio_file:
        content = audio_file.read()

    # In practice, stream should be a generator yielding chunks of audio data.
    stream = [content]
    requests = (types.StreamingRecognizeRequest(audio_content=chunk)
                for chunk in stream)

    config = types.RecognitionConfig(
        #encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        #sample_rate_hertz=16000,
        #language_code='ja-JP')
        encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz = 16000,
        language_code = 'ja-JP')

    streaming_config = types.StreamingRecognitionConfig(config=config)

    # streaming_recognize returns a generator.
    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        # Once the transcription has settled, the first result will contain the
        # is_final result. The other results will be for subsequent portions of
        # the audio.
        for result in response.results:
            print('Finished: {}'.format(result.is_final))
            print('Stability: {}'.format(result.stability))
            alternatives = result.alternatives
            # The alternatives are ordered from most likely to least.
            for alternative in alternatives:
                print('Confidence: {}'.format(alternative.confidence))
                print(u'Transcript: {}'.format(alternative.transcript))


def print_from_wav():
    path = "learn/static/learn/audio/user.wav"
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
    fig.savefig("learn/static/learn/fig/user.png")

if __name__ == '__main__':
    #main()
    stream_file = 'learn/static/learn/audio/jp/hello-jp.mp3'
    lang = 'ja-JP'
    recognition_from_file('learn/static/learn/audio/user.mp3')
    #print_from_wav()
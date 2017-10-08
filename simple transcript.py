# import libraries
import argparse
import io
# import sounddevice as sd
# import numpy as np
# import scipy.io.wavfile as wav
import pyaudio
import wave
# end import libraries

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

def translate_audio(content):
    """Translate the given audio content."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(content = content)
    config = types.RecognitionConfig(
        encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz = 16000,
        language_code = 'cmn-Hans-CN')

    response = client.recognize(config, audio)

    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))

def get_audio():

    # fs = 44100
    # duration = 5
    # myrecording = sd.rec(duration * fs, samplerate = fs, channels = 2, dtype = 'float64')
    # print("Recoding Audio")
    # sd.wait()
    # print("Audio recording complete, Play Audio")
    # sd.play(myrecording, fs)
    # sd.wait()
    # print("Complete")

    p = pyaudio.pyAudio()
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK)
    print("* recording")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    return frames


if __name__ == '__main__':
    audio = get_audio()
    translate_audio(audio)
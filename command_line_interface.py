import argparse
import scipy.io.wavfile as wavfile
from scipy.io.wavfile import WavFileWarning
import numpy as np
import warnings
import logging
import sys
import os
import io
def inputSanityCheck(encode, decode):
    # bool flag to check if we are encoding or decoding
    is_encode = True

    # that the user has provided either .wav file or .bin file
    if not encode and not decode:
        logging.error('Please provide only one input file: .wav file to compress or .bin file to decompress')
        sys.exit(1)

    # the user has only provided either .wav file or .bin file as an input
    if encode and decode:
        logging.error('Please provide only one input file: .wav file to compress or .bin file to decompress')
        sys.exit(1)

    # checking if the user wants to compress or decompress and setting a flag variable
    if decode:
        is_encode = False

    # loading the .wav file
    if is_encode:
        try:
            # loading the file at the original sampling rate
            # changing the library to scipy as librosa does not support binary data as an import
            audio_wav_file_binary_data = sys.stdin.buffer.read()
            audio_frame_rate, audio_data = wavfile.read(io.BytesIO(audio_wav_file_binary_data))

            # error checking to see if the audio file is loaded correctly
            if audio_data is not None and len(audio_data) > 0:
                logging.info('Successfully loaded!')
            else:
                logging.info('File provided is empty!')

            # print(audio_data)
            return is_encode, audio_data, audio_frame_rate, None

        except FileNotFoundError:
            logging.error('File does not exist!')
            sys.exit(1)
        except Exception as e:
            logging.error('There was an error loading the file')
            logging.error('Details: ', e)
            sys.exit(1)

    # loading the .bin file
    else:
        try:
            bin_data = sys.stdin.buffer.read()

            if bin_data:
                logging.info('Successfully loaded!')
            else:
                logging.info('File provided is empty!')

            audio_data = np.frombuffer(bin_data, dtype=np.int16)  # converting to 16-bit PCM data for now
            audio_frame_rate = 22050  #44100  # to be changed based on the algorithm

            return is_encode, audio_data, audio_frame_rate, bin_data

        except FileNotFoundError:
            logging.error('File does not exist!')
            sys.exit(1)
        except Exception as e:
            logging.error('There was an error loading the file')
            logging.error('Details: ', e)
            sys.exit(1)


def save_audio_data(audio_frame_rate, audio_data):
    try:
        wavfile.write(sys.stdout.buffer, audio_frame_rate, audio_data)
        logging.info("Audio data successfully written to output file")
    except Exception as e:
        logging.error('There was an error writing the file')
        logging.error('Details: ', e)
        sys.exit(1)


"""
    The function takes the audio file data and save it in .bin

    Args:
        audio_data: data loaded from the input audio file
"""


def save_audio_as_binary(audio_data):
    try:
        sys.stdout.buffer.write(audio_data.tobytes())
        logging.info("Binary data successfully written to output file")
    except Exception as e:
        logging.error('There was an error writing the file')
        logging.error('Details: ', e)
        sys.exit(1)

import argparse
import warnings
import logging
import sys
import os
import io
import subprocess
import queue

"""
Flac.py- act as main file for Flac.py 

When encoding for Flac implementation, write in command line:
    python3 Flac.py --encode < input.wav > payload.bin
and when decoding, write in command line:
    python3 Flac.py --decode < payload.bin > output.wav

"""
"""
    STATUS:
        *writes some binary information into payload.bin file when encoding
        *writes output.wav file when decoding
        *HOWEVER, does not play output.wav file properly for some reason
    
    DEBUGGING SUGGESTIONS:
        *suspect something is wrong when reading payload.bin file into 
        audio data
            -may involve command_line_interface (~line 56)
            and Flac_Codec (~line 57-58)
    
    REFACTORING SUGGESTIONS: 
        *way to put arguments into command_line_interface.py

"""

#MODURLARISE SYSTEM
from command_line_interface import * #Same functions as Codec-UG2-main.py file
from Flac_Codec import * #main flac codec implementation


# removing the root option while logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")



if __name__ == '__main__':

    """Same issues with Codec-UG2-main.py where prints installation messages"""
    # try:
    #     subprocess.check_call([sys.executable, "setup-FLAC.py"])
    # except subprocess.CalledProcessError as e:
    #     print("Error installing dependencies:\t", e)

    # import scipy.io.wavfile as wavfile
    # from scipy.io.wavfile import WavFileWarning
    # import numpy as np
    # import soundfile as sf
    # import pyflac
    #

    """Passes argument the same as as Codec-UG2-main.py"""
    warnings.filterwarnings("ignore", category=WavFileWarning)
    print("All libraries are there", file=sys.stderr)

    parser = argparse.ArgumentParser()
    parser.add_argument('--encode', action='store_true',
                        help='Use this to show that you need to compress the file')
    parser.add_argument('--decode', action='store_true',
                        help='Use this to show that you need to decompress the file')
    args = parser.parse_args()

    is_encode, audio_data, audio_frame_rate, bWdata = inputSanityCheck(encode=args.encode, decode=args.decode)

    """USING FLAC IMPLEMENTATION (functions in Flac_Codec.py)"""
    #checks what is being passed through codec function
    print(audio_data, file=sys.stderr)
    print(audio_frame_rate, file=sys.stderr)
    codec=FlacCodec(audio_data, is_encode)

    #encodes/decode depending on is_encode variable
    if is_encode is not None:
        binary_data=codec.encode() #WITHIN FUNCTION encode(), prints binary output
    elif not is_encode:
        codec.decode() #writes output in wav file according to audio_data

    """Comment out how Codec-UG2-main.py saves to binary and writes to binary
      cause not the same for Flac"""
    # # loads the same file as a separate audio file given using CLI to check if it has been loaded correctly
    # if os.isatty(sys.stdout.fileno()): # if > is not provided in the terminal
    #     logging.error("Output stream not provided!")
    # elif is_encode and audio_data is not None:
    #     save_audio_as_binary(audio_data)
    # elif not is_encode and audio_data is not None and audio_frame_rate is not None:
    #     save_audio_data(audio_frame_rate, audio_data)



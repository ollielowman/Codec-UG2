import argparse
import warnings
import logging
import sys
import os
import io
import subprocess
import queue

from command_line_interface import *
from Flac_Codec import *

# removing the root option while logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")



if __name__ == '__main__':

    # try:
    #     subprocess.check_call([sys.executable, "setup-FLAC.py"])
    # except subprocess.CalledProcessError as e:
    #     print("Error installing dependencies:\t", e)

    # import scipy.io.wavfile as wavfile
    from scipy.io.wavfile import WavFileWarning
    import numpy as np
    import soundfile as sf
    import pyflac

    warnings.filterwarnings("ignore", category=WavFileWarning)
    print("All libraries are there", file=sys.stderr)

    parser = argparse.ArgumentParser()
    parser.add_argument('--encode', action='store_true',
                        help='Use this to show that you need to compress the file')
    parser.add_argument('--decode', action='store_true',
                        help='Use this to show that you need to decompress the file')
    args = parser.parse_args()

    is_encode, audio_data, audio_frame_rate, bin_data = inputSanityCheck(encode=args.encode, decode=args.decode)

    # loads the same file as a separate audio file given using CLI to check if it has been loaded correctly
    if os.isatty(sys.stdout.fileno()): # if > is not provided in the terminal
        logging.error("Output stream not provided!")
    elif is_encode and audio_data is not None:
        save_audio_as_binary(audio_data)
    elif not is_encode and audio_data is not None and audio_frame_rate is not None:
        save_audio_data(audio_frame_rate, audio_data)


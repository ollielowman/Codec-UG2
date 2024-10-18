#import install_packages

#install_packages.install_packages()

import argparse
import warnings
import logging
import sys
import os
import io
import subprocess
import tempfile
import scipy.io.wavfile as wavfile
from scipy.io.wavfile import WavFileWarning
import numpy as np
# import ffmpeg
# import opuslib

# removing the root option while logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# def inputSanityCheck(encode, decode):
#     is_encode = True
#     if not encode and not decode:
#         logging.error(
#             "Please provide only one input file: .wav file to compress or .bin file to decompress"
#         )
#         sys.exit(1)
#     if encode and decode:
#         logging.error(
#             "Please provide only one input file: .wav file to compress or .bin file to decompress"
#         )
#         sys.exit(1)
#     if decode:
#         is_encode = False

#     if is_encode:
#         try:
#             audio_wav_file_binary_data = sys.stdin.buffer.read()
#             audio_frame_rate, audio_data = wavfile.read(
#                 io.BytesIO(audio_wav_file_binary_data)
#             )
#             if audio_data is not None and len(audio_data) > 0:
#                 logging.info("Successfully loaded!")
#             else:
#                 logging.info("File provided is empty!")
#             return is_encode, audio_wav_file_binary_data, None
#         except FileNotFoundError:
#             logging.error("File does not exist!")
#             sys.exit(1)
#         except Exception as e:
#             logging.error("There was an error loading the file")
#             logging.error(f"Details 1: {e}")

#             # Log additional context
#             logging.error("Failed during WAV file read operation.")
#             logging.error(
#                 f"Input data length: {len(audio_wav_file_binary_data) if audio_wav_file_binary_data else 0} bytes"
#             )

#             # Optional: Log any specific attributes if you have more context (e.g., expected values)
#             # For example, you could log expected frame rate and block align values if known
#             expected_sample_rate = 44100
#             expected_block_align = (
#                 2  # Update this if you have different expected values
#             )
#             logging.error(
#                 f"Expected Sample Rate: {expected_sample_rate}, Expected Block Align: {expected_block_align}"
#             )

#             sys.exit(1)
#     else:
#         try:
#             bin_data = sys.stdin.buffer.read()
#             if bin_data:
#                 logging.info("Successfully loaded!")
#             else:
#                 logging.info("File provided is empty!")

#             # Check if the length is valid for np.int16
#             if len(bin_data) % 2 != 0:
#                 logging.error(
#                     "Binary data size is not a multiple of 2 bytes. Adjusting..."
#                 )
#                 bin_data = bin_data[
#                     : -(len(bin_data) % 2)
#                 ]  # Truncate the extra byte(s)

#             audio_data = np.frombuffer(bin_data, dtype=np.int16)
#             return is_encode, audio_data, bin_data
#         except FileNotFoundError:
#             logging.error("File does not exist!")
#             sys.exit(1)
#         except Exception as e:
#             logging.error("There was an error loading the file")
#             logging.error(f"Details 2: {e}")

#             # Log additional context for decode operation
#             logging.error("Failed during binary data read operation.")
#             logging.error(
#                 f"Input binary data length: {len(bin_data) if bin_data else 0} bytes"
#             )

#             sys.exit(1)


def encode_wav_to_opus(input_data, bitrate='16k'):
    print("Current working directory: {0}".format(os.getcwd()), file=sys.stderr)
    os.chdir('ffmpeg-essentials')
    os.chdir('bin')

    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav_file:
        temp_wav_file.write(input_data)
        temp_wav_path = temp_wav_file.name

    temp_opus_path = 'temp.opus'

    encode_command = [
        "ffmpeg", "-i", temp_wav_path, "-c:a", "libopus", "-b:a", bitrate, temp_opus_path
    ]

    result = subprocess.run(encode_command, capture_output=True, text=True)
    os.remove(temp_wav_path)

    if result.returncode != 0:
        logging.error(f"Error during encoding: {result.stderr}")
        return None

    with open(temp_opus_path, 'rb') as opus_file:
        opus_data = opus_file.read()

    opus_size = os.path.getsize(temp_opus_path)  # Get the size of the .opus file
    os.remove(temp_opus_path)

    os.chdir("../..")

    return opus_data, opus_size

def decode_opus_to_wav(input_data):
    print("Current working directory: {0}".format(os.getcwd()), file=sys.stderr)
    os.chdir('ffmpeg-essentials')
    os.chdir('bin')
    with tempfile.NamedTemporaryFile(suffix='.opus', delete=False) as temp_opus_file:
        temp_opus_file.write(input_data)
        temp_opus_path = temp_opus_file.name

    temp_wav_path = 'temp.wav'

    decode_command = [
        "ffmpeg", "-i", temp_opus_path, "-c:a", "pcm_s16le", "-ar", "44100", "-ac", "1", "-f", "wav", temp_wav_path
    ]

    result = subprocess.run(decode_command, capture_output=True, text=True)
    os.remove(temp_opus_path)

    if result.returncode != 0:
        logging.error(f"Error during decoding: {result.stderr}")
        return None

    with open(temp_wav_path, 'rb') as wav_file:
        wav_data = wav_file.read()

    os.remove(temp_wav_path)

    os.chdir("..")
    os.chdir("..")
    return wav_data

def save_audio_data(audio_data):
    try:
        sys.stdout.buffer.write(audio_data)
        logging.info("Audio data successfully written to output file")
    except Exception as e:
        logging.error('There was an error writing the file')
        logging.error(f"Details 3: {e}")
        sys.exit(1)

def save_audio_as_binary(audio_data):
    try:
        sys.stdout.buffer.write(audio_data)
        logging.info("Binary data successfully written to output file")
    except Exception as e:
        logging.error('There was an error writing the file')
        logging.error(f"Details 4: {e}")
        sys.exit(1)

def calculate_compression(original_size, compressed_size):
    compression = (1 - compressed_size / original_size ) * 100
    logging.info(f"compressed size: {compressed_size:.5f}")
    logging.info(f"original size: {original_size:.5f}")
    logging.info(f"Compression: {compression:.5f}%")

if __name__ == '__main__':
    # supress scipy warnings

    warnings.filterwarnings("ignore", category=WavFileWarning)

    parser = argparse.ArgumentParser()
    parser.add_argument('--encode', action='store_true',
                        help='Use this to show that you need to compress the file')
    parser.add_argument('--decode', action='store_true',
                        help='Use this to show that you need to decompress the file')
    args = parser.parse_args()

    # If encode is true, then we need to compress the file
    if args.encode:
        audio_data = sys.stdin.buffer.read()
        original_size = len(audio_data)
        encoded_data, encoded_size = encode_wav_to_opus(audio_data)
        save_audio_as_binary(encoded_data)
        calculate_compression(original_size, encoded_size)
    elif args.decode:
        bin_data = sys.stdin.buffer.read()
        decoded_data = decode_opus_to_wav(bin_data)
        save_audio_data(decoded_data)

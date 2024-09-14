import argparse
import scipy.io.wavfile as wavfile
from scipy.io.wavfile import WavFileWarning
import numpy as np
import warnings
import logging
import sys
import os
import io
import subprocess
import tempfile

# removing the root option while logging 
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# supress scipy warnings
warnings.filterwarnings("ignore", category=WavFileWarning)

"""
    The function takes the bool variable encode and decode and loads the data accordingly
    
    Args:
        encode: Argument to tell if we are encoding 
        decode: Argument to tell if we are decoding
    Return:
        is_encode: boolean value to tell whether the user wants to compress or decompress
        audio_data: loaded audio file
        audio_frame_rate: frame rates of the audio file provided
        bin_file: loaded binary file
"""
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
            return is_encode, audio_wav_file_binary_data, None
        
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

            audio_data = np.frombuffer(bin_data, dtype=np.int16) # converting to 16-bit PCM data for now
            # audio_frame_rate = 44100 # to be changed based on the algorithm

            return is_encode, audio_data, bin_data
        
        except FileNotFoundError:
            logging.error('File does not exist!')
            sys.exit(1)
        except Exception as e:
            logging.error('There was an error loading the file')
            logging.error('Details: ', e)
            sys.exit(1)
            
def encode_wav_to_opus(input_data, bitrate='64k'):
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav_file:
        temp_wav_file.write(input_data)
        temp_wav_path = temp_wav_file.name

    temp_opus_path = 'temp.opus'

    # Opus encoding command
    encode_command = [
        'ffmpeg', '-i', temp_wav_path, '-c:a', 'libopus', '-b:a', bitrate, temp_opus_path
    ]

    # Execute the encoding process
    result = subprocess.run(encode_command, capture_output=True, text=True)
    os.remove(temp_wav_path)  # Clean up the temporary file

    if result.returncode != 0:
        logging.error(f"Error during encoding: {result.stderr}")
        return None

    with open(temp_opus_path, 'rb') as opus_file:
        opus_data = opus_file.read()

    os.remove(temp_opus_path)  # Clean up the temporary .opus file
    return opus_data

def decode_opus_to_wav(input_data):
    with tempfile.NamedTemporaryFile(suffix='.opus', delete=False) as temp_opus_file:
        temp_opus_file.write(input_data)
        temp_opus_path = temp_opus_file.name

    temp_wav_path = 'temp.wav'

    # Opus decoding command to convert the .opus file back to .wav
    decode_command = [
        'ffmpeg', '-i', temp_opus_path, '-c:a', 'pcm_s16le', '-f', 'wav', temp_wav_path
    ]

    # Execute the decoding process
    result = subprocess.run(decode_command, capture_output=True, text=True)
    os.remove(temp_opus_path)  # Clean up the temporary .opus file

    if result.returncode != 0:
        logging.error(f"Error during decoding: {result.stderr}")
        return None

    with open(temp_wav_path, 'rb') as wav_file:
        wav_data = wav_file.read()

    os.remove(temp_wav_path)  # Clean up the temporary .wav file
    return wav_data


"""
    The function takes the audio frame rate and audio file data and save it in .wav
    
    Args:
        audio_frame_rate: frame rate of the input audio data
        audio_data: data loaded from the input audio file
"""    
def save_audio_data(audio_data):
    try:
        # wavfile.write(sys.stdout.buffer, audio_frame_rate, audio_data)
        sys.stdout.buffer.write(audio_data)
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
        sys.stdout.buffer.write(audio_data)
        logging.info("Binary data successfully written to output file")
    except Exception as e:
        logging.error('There was an error writing the file')
        logging.error('Details: ', e)
        sys.exit(1)

if __name__ == '__main__':
    # setting the argument parser to check whether the user wants to encode or decode a file and the path of the input file
    # use the input .wav file as args.encode and the input .bin file as args.decode
    parser = argparse.ArgumentParser()
    parser.add_argument('--encode', action='store_true',
                        help='Use this to show that you need to compress the file')
    parser.add_argument('--decode', action='store_true',
                        help='Use this to show that you need to decompress the file')
    args = parser.parse_args()
    
    # input file error checking 
    is_encode, audio_data, bin_data = inputSanityCheck(encode=args.encode, decode=args.decode)
    
    # loads the same file as a separate audio file given using CLI to check if it has been loaded correctly
    if os.isatty(sys.stdout.fileno()): # if > is not provided in the terminal
        logging.error("Output stream not provided!")
    elif is_encode and audio_data is not None:
        encoded_data = encode_wav_to_opus(audio_data)
        save_audio_as_binary(encoded_data)
    elif not is_encode and audio_data is not None:
        decoded_data = decode_opus_to_wav(bin_data)
        save_audio_data(decoded_data)

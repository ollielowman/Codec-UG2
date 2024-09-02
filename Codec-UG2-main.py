import argparse
import scipy.io.wavfile as wavfile
from scipy.io.wavfile import WavFileWarning
import warnings
import logging
import sys
import os
import io

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

            # print(bin_data)
            return is_encode, None, None, bin_data
        
        except FileNotFoundError:
            logging.error('File does not exist!')
            sys.exit(1)
        except Exception as e:
            logging.error('There was an error loading the file')
            logging.error('Details: ', e)
            sys.exit(1)
            

"""
    The function takes the audio frame rate and audio file data and save it in .wav
    
    Args:
        audio_frame_rate: frame rate of the input audio data
        decode: data loaded from the input audio file
"""    
def save_audio_data(audio_frame_rate, audio_data):
    try:
        wavfile.write(sys.stdout.buffer, audio_frame_rate, audio_data)
        logging.info("Audio data successfully written to output file")
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
    is_encode, audio_data, audio_frame_rate, bin_data = inputSanityCheck(encode=args.encode, decode=args.decode)
    
    # loads the same file as a separate audio file given using CLI to check if it has been loaded correctly
    if os.isatty(sys.stdout.fileno()): # if > is not provided in the terminal
        logging.error("Output stream not provided!")
    elif is_encode and audio_data is not None and audio_frame_rate is not None:
        save_audio_data(audio_frame_rate, audio_data)

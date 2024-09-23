import argparse
import sys
import subprocess

"""
    The function takes the path of the file provided by the user and checks whether it is a valid path
    
    Args:
        audio_wav_file: The path of the input file that the user wants to compress
        output_bin_file: The path of the binary file that the user wants to decompress
    Return:
        is_encode: boolean value to tell whether the user wants to compress or decompress
        audio_data: loaded audio file
        audio_frame_rate: frame rates of the audio file provided
        bin_file: loaded binary file
"""
def inputSanityCheck(audio_wav_file, output_bin_file):
    is_encode = True
    
    # that the user has provided either .wav file or .bin file
    if audio_wav_file is None and output_bin_file is None:
        print('Input error: Please provide either the .wav file to compress or .bin file to decompress as an input!')
        sys.exit(1)
    # the user has only provided either .wav file or .bin file as an input
    elif audio_wav_file is not None and output_bin_file is not None:
        print('Input error: Please provide either the .wav file to compress or .bin file to decompress as an input but not both!')
        sys.exit(1)
    
    # checking if the user wants to compress or decompress and setting a flag variable
    if output_bin_file is not None:
        is_encode = False
    
    # checking if the file provided is a .wav file or .bin file
    if is_encode == True and audio_wav_file[-4:] != '.wav':
        print('Filetype error: Please provide a .wav file as an input!')
        sys.exit(1)
    elif is_encode == False and output_bin_file[-4:] != '.bin':
        print('Filetype error: Please provide a .bin file as an input!')
        sys.exit(1)
    
    # loading the .wav file 
    if is_encode == True:
        try:    
            # loading the file at the original sampling rate
            audio_data, audio_frame_rate = librosa.load(audio_wav_file, sr=None) 
            
            # error checking to see if the audio file is loaded correctly
            if audio_data is not None and len(audio_data) > 0:
                print(audio_wav_file + ' loaded successfully!')
            else:  
                print(audio_wav_file + ' is an empty file!')
            
            return is_encode, audio_data, audio_frame_rate
        
        except FileNotFoundError:
            print('Input error: ' + audio_wav_file + ' does not exist!')
        except:
            print('File load error: there was an error loading the file!')
    
    # loading the .bin file
    else:
        try:
            with open(output_bin_file, 'rb') as bin_file:
                bin_data = bin_file.read()
                
                if bin_data:
                    print(output_bin_file + ' loaded successfully!')
                else:
                    print(output_bin_file + ' is an empty file!')

                return is_encode, output_bin_file
        
        except FileNotFoundError:
            print('Input error: ' + output_bin_file + ' does not exist!')
        except:
            print('File load error: there was an error loading the file!')

if __name__ == '__main__':
    # Downloading & install the dependencies by calling the script "setup-FLAC.py"
    try:
        subprocess.check_call([sys.executable, "setup-FLAC.py"])
    except subprocess.CalledProcessError as e:
        print("Error installing dependencies:\t", e)

    import librosa

    # setting the argument parser to check whether the user wants to encode or decode a file and the path of the input file
    # use the input .wav file as args.encode and the input .bin file as args.decode
    parser = argparse.ArgumentParser()
    parser.add_argument('--encode', type=str, nargs='?',
                        help='Enter the path of a .wav file you want to compress')
    parser.add_argument('--decode', type=str, nargs='?',
                        help='Enter the path of a .bin file you want to decompress')
    args = parser.parse_args()

    # input file error checking
    inputSanityCheck(audio_wav_file=args.encode, output_bin_file=args.decode)

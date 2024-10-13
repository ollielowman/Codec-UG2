import argparse
import warnings
import logging
import sys
import os
import io
import subprocess
import tempfile

# removing the root option while logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def download_dependencies():
    """
    Use this function to download dependencies (For dev team only)
    Comment out download_dependencies() when testing
    """
    with open("trash.txt", "w") as f:  # Redirecting output to trash.txt
        try:
            subprocess.check_call(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "download",
                    "scipy",
                    "opuslib",  # For OPUS codec
                    # "pyflac", # For FLAC codec
                    # "wheel",  # For FLAC codec
                    # "setuptools"  # For FLAC codec
                ],
                stdout=f,  # Redirect stdout to the file
                stderr=f,  # Redirect stderr to the file as well
            )
        except subprocess.CalledProcessError as e:
            print("Error installing dependencies:\t", e, file=sys.stderr)


def install_dependencies():
    """
    This installs the downloaded dependencies
    """
    with open("trash.txt", "w") as f:  # Redirecting output to trash.txt
        try:
            subprocess.check_call(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--no-index",
                    "--find-links",
                    ".",
                    "scipy",
                    "opuslib",  # For OPUS codec
                    # "pyflac", # For FLAC codec
                    # "wheel",  # For FLAC codec
                    # "setuptools"  # For FLAC codec
                ],
                stdout=f,  # Redirect stdout to the file
                stderr=f,  # Redirect stderr to the file as well
            )
        except subprocess.CalledProcessError as e:
            print("Error installing dependencies:\t", e, file=sys.stderr)


def inputSanityCheck(encode, decode):
    is_encode = True
    if not encode and not decode:
        logging.error('Please provide only one input file: .wav file to compress or .bin file to decompress')
        sys.exit(1)
    if encode and decode:
        logging.error('Please provide only one input file: .wav file to compress or .bin file to decompress')
        sys.exit(1)
    if decode:
        is_encode = False
    if is_encode:
        try:
            audio_wav_file_binary_data = sys.stdin.buffer.read()

            # Log WAV file headers in a separate try block
            try:
                with wave.open(
                    io.BytesIO(audio_wav_file_binary_data), "rb"
                ) as wav_file:
                    num_channels = wav_file.getnchannels()
                    sample_width = wav_file.getsampwidth()
                    frame_rate = wav_file.getframerate()
                    num_frames = wav_file.getnframes()
                    compression_type = wav_file.getcomptype()
                    compression_name = wav_file.getcompname()

                    # Log header information to error log
                    logging.error("WAV File Headers:")
                    logging.error(f"Number of Channels: {num_channels}")
                    logging.error(f"Sample Width (bytes): {sample_width}")
                    logging.error(f"Frame Rate (Sample Rate, Hz): {frame_rate}")
                    logging.error(f"Number of Frames (Samples): {num_frames}")
                    logging.error(f"Compression Type: {compression_type}")
                    logging.error(f"Compression Name: {compression_name}")
            except Exception as e:
                logging.error("There was an error reading the WAV headers")
                logging.error(f"Details (Header Read): {e}")
                sys.exit(1)

            audio_frame_rate, audio_data = wavfile.read(io.BytesIO(audio_wav_file_binary_data))
            if audio_data is not None and len(audio_data) > 0:
                logging.info('Successfully loaded!')
            else:  
                logging.info('File provided is empty!')
            return is_encode, audio_wav_file_binary_data, None
        except FileNotFoundError:
            logging.error('File does not exist!')
            sys.exit(1)
        except Exception as e:
            logging.error('There was an error loading the file to encode')
            logging.error(f"Details 1: {e}")
            sys.exit(1)
    else:
        try:
            bin_data = sys.stdin.buffer.read()
            if bin_data:
                logging.info('Successfully loaded!')
            else:
                logging.info('File provided is empty!')

            # Check if the length is valid for np.int16
            if len(bin_data) % 2 != 0:
                logging.error("Binary data size is not a multiple of 2 bytes. Adjusting...")
                # You can either pad with zeros or truncate:
                bin_data = bin_data[:-(len(bin_data) % 2)]  # Truncate the extra byte(s)

            audio_data = np.frombuffer(bin_data, dtype=np.int16)
            return is_encode, audio_data, bin_data
        except FileNotFoundError:
            logging.error('File does not exist!')
            sys.exit(1)
        except Exception as e:
            logging.error('There was an error loading the file to decode')
            logging.error(f"Details 2: {e}")
            sys.exit(1)

def encode_wav_to_opus(input_data, bitrate='16k'):
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_wav_file:
        temp_wav_file.write(input_data)
        temp_wav_path = temp_wav_file.name

    temp_opus_path = 'temp.opus'

    encode_command = [
        'ffmpeg', '-i', temp_wav_path, '-c:a', 'libopus', '-b:a', bitrate, "-ac", "1", temp_opus_path
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
    return opus_data, opus_size

def decode_opus_to_wav(input_data):
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
    import wave

    # download_dependencies()
    install_dependencies()

    import scipy.io.wavfile as wavfile
    from scipy.io.wavfile import WavFileWarning
    import numpy as np

    # supress scipy warnings
    warnings.filterwarnings("ignore", category=WavFileWarning)

    parser = argparse.ArgumentParser()
    parser.add_argument('--encode', action='store_true',
                        help='Use this to show that you need to compress the file')
    parser.add_argument('--decode', action='store_true',
                        help='Use this to show that you need to decompress the file')
    args = parser.parse_args()

    is_encode, audio_data, bin_data = inputSanityCheck(encode=args.encode, decode=args.decode)

    if os.isatty(sys.stdout.fileno()):
        logging.error("Output stream not provided!")
    elif is_encode and audio_data is not None:
        original_size = len(audio_data)  # Original WAV file size in bytes
        encoded_data, encoded_size = encode_wav_to_opus(audio_data)
        save_audio_as_binary(encoded_data)
        calculate_compression(original_size, encoded_size)
    elif not is_encode and audio_data is not None:
        decoded_data = decode_opus_to_wav(bin_data)
        save_audio_data(decoded_data)

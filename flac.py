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
import wave

# removing the root option while logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def analyze_wav_properties(input_data):
    """Extract properties like sample rate, channels (mono/stereo), bit depth, and sample count from the WAV file."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav_file:
        temp_wav_file.write(input_data)
        temp_wav_path = temp_wav_file.name

    try:
        with wave.open(temp_wav_path, mode="rb") as wave_reader:
            channels = wave_reader.getnchannels()
            sample_rate = wave_reader.getframerate()
            sample_width = wave_reader.getsampwidth() * 8  # Convert to bits
            sample_count = wave_reader.getnframes()

            # Determine if mono or stereo
            audio_format = "MONO" if channels == 1 else "STEREO"
            logging.info(f"WAV file is {audio_format}")
            logging.info(f"WAV file sample rate = {sample_rate} Hz")
            logging.info(f"WAV file samples are {sample_width}-bit")
            logging.info(
                f"WAV file is {sample_count} samples long ({sample_count / sample_rate:.2f} seconds)"
            )
    except wave.Error as err:
        logging.error(f"ERROR: Failed to read WAV file: {err}")
        sys.exit(1)
    finally:
        os.remove(temp_wav_path)


def encode_wav_to_flac(input_data, bitrate="16k"):
    """Convert WAV input data to flac format using ffmpeg."""
    os.chdir("ffmpeg-essentials")
    os.chdir("bin")

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav_file:
        temp_wav_file.write(input_data)
        temp_wav_path = temp_wav_file.name

    temp_flac_path = "temp.flac"

    encode_command = [
        "ffmpeg",
        "-i",
        temp_wav_path,
        "-c:a",
        "flac",
        "-b:a",
        bitrate,
        temp_flac_path,
    ]

    result = subprocess.run(encode_command, capture_output=True, text=True)
    os.remove(temp_wav_path)

    if result.returncode != 0:
        logging.error(f"Error during encoding: {result.stderr}")
        return None

    with open(temp_flac_path, "rb") as flac_file:
        flac_data = flac_file.read()

    flac_size = os.path.getsize(temp_flac_path)  # Get the size of the .flac file
    os.remove(temp_flac_path)

    os.chdir("../..")

    return flac_data, flac_size


def decode_flac_to_wav(input_data):
    """Convert flac input data to WAV format using ffmpeg."""
    os.chdir("ffmpeg-essentials")
    os.chdir("bin")

    with tempfile.NamedTemporaryFile(suffix=".flac", delete=False) as temp_flac_file:
        temp_flac_file.write(input_data)
        temp_flac_path = temp_flac_file.name

    temp_wav_path = "temp.wav"

    decode_command = [
        "ffmpeg",
        "-i",
        temp_flac_path,
        "-c:a",
        "pcm_s16le",
        "-ar",
        "44100",
        "-ac",
        "1",
        "-f",
        "wav",
        temp_wav_path,
    ]

    result = subprocess.run(decode_command, capture_output=True, text=True)
    os.remove(temp_flac_path)

    if result.returncode != 0:
        logging.error(f"Error during decoding: {result.stderr}")
        return None

    with open(temp_wav_path, "rb") as wav_file:
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
        logging.error("There was an error writing the file")
        logging.error(f"Details: {e}")
        sys.exit(1)


def save_audio_as_binary(audio_data):
    try:
        sys.stdout.buffer.write(audio_data)
        logging.info("Binary data successfully written to output file")
    except Exception as e:
        logging.error("There was an error writing the file")
        logging.error(f"Details: {e}")
        sys.exit(1)


def calculate_compression(original_size, compressed_size):
    compression = (1 - compressed_size / original_size) * 100
    logging.info(f"compressed size: {compressed_size:.5f}")
    logging.info(f"original size: {original_size:.5f}")
    logging.info(f"Compression: {compression:.5f}%")


if __name__ == "__main__":
    # suppress scipy warnings
    warnings.filterwarnings("ignore", category=WavFileWarning)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--encode", action="store_true", help="Use this to compress the file"
    )
    parser.add_argument(
        "--decode", action="store_true", help="Use this to decompress the file"
    )
    parser.add_argument(
        "--analyze", action="store_true", help="Analyze the properties of the WAV file"
    )
    args = parser.parse_args()

    # Handle different command options
    if args.encode:
        audio_data = sys.stdin.buffer.read()
        original_size = len(audio_data)
        encoded_data, encoded_size = encode_wav_to_flac(audio_data)
        save_audio_as_binary(encoded_data)
        calculate_compression(original_size, encoded_size)
    elif args.decode:
        bin_data = sys.stdin.buffer.read()
        decoded_data = decode_flac_to_wav(bin_data)
        save_audio_data(decoded_data)
    elif args.analyze:
        audio_data = sys.stdin.buffer.read()
        analyze_wav_properties(audio_data)

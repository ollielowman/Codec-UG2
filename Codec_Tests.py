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

#logging.basicConfig(level=logging.WARNING)
def encode_opus(input_file, output_file):
    try:
        with open(input_file, 'rb') as infile, open(output_file,'wb') as outfile:
            encode_opus=["python3","Opus.py", "--encode"]
            subprocess.run(encode_opus, check=True, text=True, stdin=infile, stdout=outfile)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error: {e.stderr}")
        logging.error(f"Return code: {e.returncode}")
    except FileNotFoundError as fnf_error:
        logging.error(f"Error: {fnf_error}")
    except Exception as ex:
        logging.error(f"An error occured: {ex}")

def decode_opus(input_file, output_file):
    try:
        with open(input_file, 'rb') as infile, open(output_file,'wb') as outfile:
            encode_opus=["python3","Opus.py", "--decode"]
            subprocess.run(encode_opus, check=True, text=True, stdin=infile, stdout=outfile)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error: {e.stderr}")
        logging.error(f"Return code: {e.returncode}")
    except FileNotFoundError as fnf_error:
        logging.error(f"Error: {fnf_error}")
    except Exception as ex:
        logging.error(f"An error occured: {ex}")

def encode_flac(input_file,output_file):
    try:
        with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
            encode_opus = ["python3", "flac.py", "--encode"]
            subprocess.run(encode_opus, check=True, text=True, stdin=infile, stdout=outfile)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error: {e.stderr}")
        logging.error(f"Return code: {e.returncode}")
    except FileNotFoundError as fnf_error:
        logging.error(f"Error: {fnf_error}")
    except Exception as ex:
        logging.error(f"An error occured: {ex}")

def decode_flac(input_file,output_file):
    try:
        with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
            encode_opus = ["python3", "flac.py", "--decode"]
            subprocess.run(encode_opus, check=True, text=True, stdin=infile, stdout=outfile)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error: {e.stderr}")
        logging.error(f"Return code: {e.returncode}")
    except FileNotFoundError as fnf_error:
        logging.error(f"Error: {fnf_error}")
    except Exception as ex:
        logging.error(f"An error occured: {ex}")


if __name__ == "__main__":
    compress_opus = []
    compress_flac= []
    for i in range(1,6):
        enc_in="-"+str(i)+".wav"
        encode_input="archive/test"+enc_in
        enc_out="-"+str(i)+".bin"
        encode_output="payloads/payload"+enc_out
        encode_opus(encode_input,encode_output)
        dec_in="-"+str(i)+".bin"
        decode_input="payloads/payload"+dec_in
        dec_out="-"+str(i)+".wav"
        decode_output="output_wav/output"+dec_out
        decode_opus(decode_input,decode_output)
        with open('compressions.txt', 'r') as f:
            compression = f.read()
            compress_opus.append(compression)

    for i in range(1, 6):
        enc_in = "-" + str(i) + ".wav"
        encode_input = "archive/test" + enc_in
        enc_out = "-" + str(i) + ".bin"
        encode_output = "payloads/payload" + enc_out
        encode_flac(encode_input, encode_output)
        dec_in = "-" + str(i) + ".bin"
        decode_input = "payloads/payload" + dec_in
        dec_out = "-" + str(i) + ".wav"
        decode_output = "output_wav/output" + dec_out
        decode_flac(decode_input, decode_output)
        with open('compressions.txt', 'r') as f:
            compression = f.read()
            compress_flac.append(compression)

    #print(f"{compress_list}", file=sys.stderr)
    compress_opus=[float(num) for num in compress_opus]
    compress_flac=[float(num) for num in compress_flac]
    print(f"Average Opus Compression: {sum(compress_opus)/len(compress_opus)}", file=sys.stderr)
    print(f"Average Flac Compression: {sum(compress_flac)/len(compress_flac)}", file=sys.stderr)




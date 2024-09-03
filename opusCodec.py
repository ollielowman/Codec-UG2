import subprocess
import os
import sys

def encode_wav_to_opus(input_wav_path, output_bin_path, bitrate='64k'):
    temp_opus_path = 'temp.opus'
    
    # Opus encoding command
    encode_command = [
        'ffmpeg', '-i', input_wav_path, '-c:a', 'libopus', '-b:a', bitrate, temp_opus_path
    ]
    
    # Execute the encoding process
    result = subprocess.run(encode_command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error during encoding: {result.stderr}")
        return False
    
    # Rename the .opus file to .bin
    os.rename(temp_opus_path, output_bin_path)
    
    # Check the size of the payload.bin
    encoded_file_size = os.path.getsize(output_bin_path)
    return True

def decode_opus_to_wav(input_bin_path, output_wav_path):
    # Opus decoding command to convert the .bin back to .wav
    decode_command = [
        'ffmpeg', '-i', input_bin_path, '-c:a', 'pcm_s16le', '-f', 'wav', output_wav_path
    ]
    
    # Execute the decoding process
    result = subprocess.run(decode_command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error during decoding: {result.stderr}")
        return False
    
    return True

def main():
    if len(sys.argv) < 4:
        print("Usage:")
        print("  To encode: script_name --encode <input.wav> <output.bin>")
        print("  To decode: script_name --decode <input.bin> <output.wav>")
        return
    
    command = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    if command == '--encode':
        if not input_file.endswith('.wav'):
            print("Error: The input file must be a .wav file.")
            return
        success = encode_wav_to_opus(input_file, output_file)
        if success:
            print(f"Encoded {input_file} to {output_file} successfully.")
    elif command == '--decode':
        if not input_file.endswith('.bin'):
            print("Error: The input file must be a .bin file.")
            return
        success = decode_opus_to_wav(input_file, output_file)
        if success:
            print(f"Decoded {input_file} to {output_file} successfully.")
    else:
        print("Invalid command. Use --encode or --decode.")

if __name__ == '__main__':
    main()
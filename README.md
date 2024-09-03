# Codec-UG2

*This CODEC was designed on ubuntu, using python 3.12.4, to run with Ubuntu & MS Azure linux images, in Anaconda, Miniconda or python venv environments*

**Dependencies Installation**
- For the purpose of streamlining dependency installation, setup scripts have been included for both OPUS and FLAC codecs.
- To install dependencies, run the command `python3 setup-<Codec>.py` in your CLI, replacing `<Codec>` with either `OPUS` or `FLAC`.
- _Note:  Dependencies have been pre-downloaded into their respective dependency directories to facilitate offline installation._
 
Run the file using the following command in CLI:

**For encoding**

`python Codec-UG2-main.py --encode < dataset/input.wav` should load the file successfully. To check if the input audio file is being loaded correctly, use the command `python Codec-UG2-main.py --encode < dataset/input.wav > dataset/output.wav`. This would create a new audio file in the `dataset` folder. You can play both input and output audio files to verify they sound the same and the code loads and saves the files correctly using `<` and `>` tokens in CLI.

**For decoding**

`python Codec-UG2-main.py --decode < dataset/payload.bin` and this would display the contents of `payload.bin` in the terminal. You can verify by checking the file to the terminal output to confirm that the load has happened successfully.

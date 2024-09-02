# Codec-UG2

*This CODEC was designed on ubuntu, designed to run with MS Azure linux images.*

**Libraries**
- `scipy` - Please install `scipy` before running the program.
  - For *Anaconda* or *miniconda* install:  `conda install scipy`
  - Otherwise, please follow the following steps:
    - Change directory to where you would like to create a environment.
    - Create the environment with `python3 -m venv <environment_name>`
    - Activate the environment with `source <environment_name>/bin/activate`
    - Finally, install `scipy` with `pip install scipy`
 
Run the file using the following command in CLI:

**For encoding**

`python Codec-UG2-main.py --encode < dataset/input.wav` should load the file successfully. To check if the input audio file is being loaded correctly, use the command `python Codec-UG2-main.py --encode < dataset/input.wav > dataset/output.wav`. This would create a new audio file in the `dataset` folder. You can play both input and output audio files to verify they sound the same and the code loads and saves the files correctly using `<` and `>` tokens in CLI.

**For decoding**

`python Codec-UG2-main.py --decode < dataset/payload.bin` and this would display the contents of `payload.bin` in the terminal. You can verify by checking the file to the terminal output to confirm that the load has happened successfully.

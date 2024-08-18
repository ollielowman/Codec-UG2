# Codec-UG2

*This CODEC was designed on ubuntu, designed to run with MS Azure linux images.*

**Libraries**
- `librosa` - Please install `librosa` before running the program.
  - For *Anaconda* or *miniconda* install:  `conda install -c conda-forge librosa`
  - Otherwise, please follow the followin steps:
    - Change directory to where you would like to create a environment.
    - Create the environment with `python3 -m venv <environment_name>`
    - Activate the environment with `source <environment_name>/bin/activate`
    - Finally, install `librosa` with `pip install librosa`
 
Run the file using the following command in CLI:

**For encoding**

`python initial_code_UG2.py --encode dataset/input.wav`

**For decoding**

`python initial_code_UG2.py --decode dataset/payload.bin`

"""
import this script and run the install_packages() function before any import calls. 

Steps:
- create an empty packages folder
- open a suitable python terminal, I used anaconda prompt to replicate mapteks.
    You can use any terminal but make sure you terminal is of:
    - pip version 24.0          you can check this by running pip --version in your terminal
    - python 3.12.4             you can check this by running python --version
- make sure your code works when running using python 3.12.4
- pip download your dependencies into the packages folder
- Done!
"""

import subprocess
import sys
import os

def install_packages():

    relative_path = "packages"
    absolute_path = os.path.abspath(relative_path)
    if os.path.isdir(absolute_path):
        print("valid directory", file=sys.stderr)

    print(f"Trying to install packages from: {absolute_path}", file=sys.stderr)
    
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-index", "--find-links=" + absolute_path, "opuslib", "ffmpeg"], stdout=sys.stderr, stderr=sys.stderr)
    """
    Replace package1 and package2 with the packages you need!
    """


    package_path = r"C:\Windows\ServiceProfiles\LocalService\AppData\Roaming\Python\Python312\site-packages"
    if package_path not in sys.path:
        sys.path.append(package_path)
        print("Adding: ", package_path, file=sys.stderr)

    print("COMPLETE INSTALLATION", file=sys.stderr)

    """try test importing your function to see if it works with the system"""
    # import your_function

"""
Uncomment the below code to make this a standalone file
then you can submit just this file to the leaderboard to check if everything is working!
"""
if __name__ == "__main__":
    install_packages()
import sys
import subprocess


def download_dependencies():
    """
    Use this function to download dependencies (For dev team only)
    Comment out download_dependencies() when testing
    """
    try:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "download",
                "-d",
                "dependencies-FLAC",
                "scipy",
                "pyflac",
                "librosa",
                "setuptools",
                "wheel"
            ]
        )
        print(
            "=====================================\n"
            + "Dependencies downloaded successfully!\n"
            + "=====================================",
            file=sys.stderr
        )
    except subprocess.CalledProcessError as e:
        print("Error installing dependencies:\t", e, file=sys.stderr)


def install_dependencies():
    """
    This installs the downloaded dependencies
    """
    try:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--no-index",
                "--find-links",
                "dependencies-FLAC",
                "scipy",
                "pyflac",
                "librosa",
                "setuptools",
                "wheel"
            ]
        )
        print(
            "=====================================\n"
            + "Dependencies installed successfully!\n"
            + "=====================================", file=sys.stderr
        )
    except subprocess.CalledProcessError as e:
        print("Error installing dependencies:\t", e, file=sys.stderr)


def main():
    # Downloading & install the dependencies by calling the script "setup-FLAC.py"
    download_dependencies()
    install_dependencies()


if __name__ == "__main__":
    main()

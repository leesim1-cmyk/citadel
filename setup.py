import os
import subprocess
import sys

def install_requirements(requirements_path="requirements.txt"):
    # Ensure the requirements file exists before trying to install
    if not os.path.exists(requirements_path):
        print(f"Error: {requirements_path} not found.")
        return

    print(f"Installing dependencies from {requirements_path}...")
    try:
        # sys.executable ensures we use the current Python environment's pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
        print("Installation successful!")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during installation: {e}")

if __name__ == "__main__":
    # Path to your requirements.txt
    install_requirements("requirements.txt")


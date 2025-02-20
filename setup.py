import os
import sys
import subprocess
from pathlib import Path


basepath = Path(os.path.dirname(__file__)) / "requirements"
yolov10_req = basepath / "yolov10_requirements.txt"


def create_env(env_name, req_file, python_v, env_dir="environments"):

    """
    Creates a new Conda environment with the specified name, Python version, 
    and installs dependencies from a requirements file.

    Parameters:
    env_name (str): The name of the Conda environment.
    req_file (str): Path to the requirements file containing the dependencies.
    python_v (str): The version of Python to be installed (e.g., "3.9").

    Returns:
    None
    """

    env_path = Path(env_dir)

    if not env_path.exists():
        env_path.mkdir(parents=True)

    full_path = env_path / env_name

    try:

        print(f"Creating Conda environment: {env_name}")
        
        subprocess.run([
            "conda", "create", "-y", "-p", str(full_path), f"python={python_v}"
        ], check=True)

        pip_path = full_path / ("Scripts" if os.name == "nt" else "bin") / "pip"

        print(f"Installing requirements for {env_name}")

        subprocess.run([
            str(pip_path), "install", "-r", str(req_file)
        ], check=True)

        print(f"Environment {env_name} successfully created and requirements installed at {str(full_path)}")
    
    except subprocess.CalledProcessError as e:

        print(f"Failed to create {env_name}: {e}")
        sys.exit(1)


def main():
    
    create_env("yolov10_env_conda", yolov10_req, "3.10")



if __name__ == "__main__":
    main()
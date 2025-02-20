import os
import sys
import json
import shutil
import argparse
import subprocess
from pathlib import Path

model_config_path = Path("model_config.json")

def input_handling(model_path, test_file_path, weights_path, req_path, model_name):

    model_path = Path(model_path)
    test_file_path = Path(test_file_path)
    weights_path = Path(weights_path)
    req_path = Path(req_path)

    if not model_path.exists():

        print(f"Model Path not found at {model_path}")
        sys.exit(0)

    path_list = [test_file_path, weights_path, req_path]

    try:
        for path in path_list:
            path.exists()

    except FileNotFoundError as e:

        print(f"File not found: {e}")
        sys.exit(0)
    
    try:
        test_file_path.relative_to(model_path)

    except ValueError:

        print(f"Inference_file {test_file_path} not found in {model_path}")
        sys.exit(0)

    with model_config_path.open("r") as model_config_file:
        model_config = json.load(model_config_file)

    if model_name in model_config.keys():

        print(f"Model name {model_name} already in model_paths_config.json")
        sys.exit(0)

def create_env(name, req_path, python_v):

    """
    Creates a new Conda environment for a project, installs the specified Python version 
    and dependencies.

    Parameters:
    name (str): Name of the environment.
    req_path (str): Path to the requirements file containing the dependencies.
    python_v (str): Python version to use in the environment (e.g., "3.9").

    Returns:
    None
    """

    req_path = Path(req_path)
    env_dir = Path("environments") / f"{name}_env_conda"

    if env_dir.exists():
        print(f"Environment for {name} already exists at {str(env_dir)}")
        sys.exit(0)
    else:
        env_dir.mkdir(parents=True)

    try:
        print(f"Creating Conda environment: {name} at {str(env_dir)}")
        
        subprocess.run([
            "conda", "create", "-y", "-p", str(env_dir), f"python={python_v}"
        ], check=True)

        pip_path = env_dir / ("Scripts" if os.name == "nt" else "bin") / "pip"

        print(f"Installing requirements for {name}")
        subprocess.run([
            str(pip_path), "install", "-r", str(req_path)
        ], check=True)

        print(f"Environment for {name} successfully created and requirements installed at {str(env_dir)}")
    
    except subprocess.CalledProcessError as e:
        print(f"Failed to create environment for {name}: {e}")
        sys.exit(1)

def add_paths_to_config(model_name, test_file_path):

    """
    Adds a model entry in the configuration file with paths to its environment 
    and test script.

    Parameters:
    model_name (str): Name of the model to add or update in the configuration file.
    test_file_path (str): Path to the test script associated with the model.

    Returns:
    None

    Notes:
    - The function creates an entry in mode_config.json with the following keys:
      - "env": Path to the Conda environment for the model.
      - "script": Path to the test script.
    """

    test_file_path = Path(test_file_path)

    with model_config_path.open("r") as model_config:
        config = json.load(model_config)

    config[model_name] = {
        "env": str(Path("environments") / f"{model_name}_env_conda"),
        "script": str(test_file_path)
    }

    with model_config_path.open("w") as model_config:
        json.dump(config, model_config, indent=4)
    
    print(f"Successfully added entry for {model_name} to model_config")

def copy_files(source_path, target_path):

    """
    Copies a file or directory from the source path to the target path.

    Parameters:
    source_path (str): Path to the source file or directory.
    target_path (str): Path to the destination.

    Returns:
    None
    """

    source_path = Path(source_path)
    target_path = Path(target_path)

    try:

        if source_path.is_file():
            
            shutil.copy(source_path, target_path)

            print(f"Copied file: {source_path} to {target_path}")

        elif source_path.is_dir():
            
            shutil.copytree(source_path, target_path, dirs_exist_ok=True)

            print(f"Copied directory: {source_path} to {target_path}")
        
    except Exception as e:
        print(f"Error while copying {source_path} to {target_path}: {e}")


def main():

    parser = argparse.ArgumentParser(description="Add your model")
    parser.add_argument("--model_path", required=True, help="The directory with all model architecture files")
    parser.add_argument("--inference_path", required=True, help="Path to the file to initialize the model and run inference")
    parser.add_argument("--weights_path", required=True, help="Path to the models weights file")
    parser.add_argument("--requirements_path", required=True, help="Path to the requirements file")
    parser.add_argument("--python_version", required=True, help="Python version for the model")
    parser.add_argument("--name", required=True, help="The name of the model")


    args = parser.parse_args()

    model_path = args.model_path
    test_file_path = args.inference_path
    weights_path = args.weights_path
    req_path = args.requirements_path
    python_v = args.python_version
    model_name = args.name

    input_handling(model_path, test_file_path, weights_path, req_path, model_name)

    relative_test_file_path = Path(test_file_path).relative_to(model_path)
    final_test_file_path = Path("models") / model_name / relative_test_file_path

    create_env(model_name, req_path, python_v)

    copy_files(req_path, Path("requirements") / f"{model_name}_{Path(req_path).name}")
    copy_files(weights_path, Path("pretrained_weights") / f"{model_name}_{Path(weights_path).name}")
    copy_files(model_path, Path("models") / model_name)

    add_paths_to_config(model_name, final_test_file_path)





if __name__ == "__main__":
    main()
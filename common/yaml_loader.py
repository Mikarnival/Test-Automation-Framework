from os import PathLike 
from pathlib import Path
from typing import Any

import yaml

def load_yaml(file_path: str | PathLike[str]) -> list[dict[str, Any]]:
    """
    Load a YAML file and return its contents as a list of dictionaries.

    Args:
        file_path (str | PathLike[str]): The path to the YAML file.

    Returns:
        list[dict[str, Any]]: The contents of the YAML file as a list of dictionaries.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if not isinstance(data, list):
        raise ValueError(f"The YAML file '{file_path}' must contain a list of dictionaries.")

    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Item at index {index} in the YAML file '{file_path}' is not a dictionary.")
    
    return data
import os
from pathlib import Path

project_name = "network_security"

files = [
    ".github/workflows/main.yml",
    f"{project_name}/__init__.py",
    f"{project_name}/cloud/__init__.py",
    f"{project_name}/components/__init__.py",
    f"{project_name}/constants/__init__.py",
    f"{project_name}/entity/__init__.py",
    f"{project_name}/utils/__init__.py",
    f"{project_name}/pipeline/__init__.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/logging/__init__.py",
    "Network_Data/.gitkeep",
    "notebooks/.gitkeep",
    "requirements.txt",
    "DockerFile",
    "setup.py",
    ".env"
]

for file in files:
    filepath = Path(file)
    filedir = filepath.parent

    # Create the directory if it doesn't exist
    if filedir:
        os.makedirs(filedir, exist_ok=True)

    # Create the file if it doesn't exist
    if not filepath.exists():
        filepath.touch()

"""Module for handling the read-in of config.yaml values"""
from pathlib import Path

import yaml


CONFIG_PATH = Path.cwd() / "config.yaml"

with open(CONFIG_PATH, "r") as f:
    CONFIG = yaml.safe_load(f)

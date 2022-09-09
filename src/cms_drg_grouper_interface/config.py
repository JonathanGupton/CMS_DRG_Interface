"""Module for handling the read-in of config.yaml values"""
from pathlib import Path

import tomli

from default import DEFAULTS


def load_config():
    directory = Path.cwd()
    pyproject_toml = "pyproject.toml"
    return read_config_file(directory, pyproject_toml)


def read_config_file(directory, filename):
    with open(directory / filename, "rb") as f:
        config = tomli.load(f)
    return extract_config_from_toml(config)


def extract_config_from_toml(config: dict) -> dict:
    config = config["tool"]["drg-grouper"]
    return config


CONFIG = load_config()
for key in DEFAULTS:
    CONFIG[key] = CONFIG.get(key, DEFAULTS[key])

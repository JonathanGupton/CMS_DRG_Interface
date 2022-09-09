"""

- Create __all__ imports
- Read in pyproject.toml vs read in defaults
- Instantiate classes with defaults
- Figure out how to initialize the fields without hard-coding the fields or
  batch requirements
- Check if grouper exists on path
"""
from pathlib import Path

from cms_drg_grouper_interface.config import CONFIG


if not Path(CONFIG["grouper_path"]).exists():
    raise FileExistsError(f"Grouper path {CONFIG['grouper_path']} not found")

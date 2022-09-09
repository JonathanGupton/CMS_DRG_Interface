import contextlib
import os
import subprocess
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from subprocess import CompletedProcess
from typing import Optional

from cms_drg_grouper_interface.config import CONFIG
from cms_drg_grouper_interface.batch import Batch
from cms_drg_grouper_interface.parameter import GrouperParameter


@contextlib.contextmanager
def working_directory(path):
    """Changes working directory and returns to previous on exit.
    h/t https://stackoverflow.com/a/42441759/5411579
    """
    prev_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


class MSDRGGrouperSoftwareOption(Enum):
    """Command line arguments used by the CMS MS-DRG Grouper software"""

    Input = "-i"
    FormattedOutput = "-o"
    SingleLineOutput = "-u"


class MSDRGGrouperSoftwareParameter(GrouperParameter):
    """
    Class containing the required parameters for grouping a batch with the
    CMS MS-DRG Grouper Software
    """

    def __init__(
        self,
        *args,
        batch: Batch,
        batchfile_path: Optional[Path] = None,
        output_type: MSDRGGrouperSoftwareOption = MSDRGGrouperSoftwareOption.SingleLineOutput,
        output_destination: Optional[Path] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.batch = batch
        self.batchfile_path = (
            batchfile_path if batchfile_path else Path.cwd() / "input.txt"
        )
        self.output_type = output_type
        self.output_destination = (
            output_destination if output_destination else Path.cwd() / "output.txt"
        )

    def __repr__(self):
        return f"{self.__class__.__name__}({self.batchfile_path}, {self.output_type}, {self.output_destination})"

    def __iter__(self):
        yield MSDRGGrouperSoftwareOption.Input.value
        yield str(self.batchfile_path)
        yield self.output_type.value
        yield str(self.output_destination)


class GrouperInterface(ABC):
    """Base class for interfacing with the Grouper software"""

    @abstractmethod
    def group(self, params) -> bool:
        pass


class MSDRGGrouperSoftwareInterface(GrouperInterface):
    """Class responsible for directly calling the MS-DRG Grouper program"""

    msgmce = "msgmce.bat"

    def __init__(self, grouper_directory: Path = None) -> None:
        if grouper_directory is not None:
            self.grouper_directory = grouper_directory
        else:
            self.grouper_directory = Path(CONFIG["grouper_path"])

    def group(self, params: MSDRGGrouperSoftwareParameter) -> CompletedProcess:
        command = [self.msgmce, *params]
        with working_directory(self.grouper_directory):
            proc = subprocess.run(command)
        return proc

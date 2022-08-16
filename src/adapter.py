import contextlib
import os
import subprocess
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path


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


class MSDRGGrouperSoftwareOptions(Enum):
    """Command line arguments used by the CMS MS-DRG Grouper software"""
    Input = "-i"
    FormattedOutput = "-o"
    SingleLineOutput = "-u"


class MSDRGGrouperSoftwareParameters:
    """
    Class containing the required parameters for grouping a batch with the
    CMS MS-DRG Grouper Software
    """
    def __init__(
        self,
        batchfile: Path,
        output_type: MSDRGGrouperSoftwareOptions,
        output_destination: Path,
    ):
        self.batchfile = batchfile
        self.output_type = output_type
        self.output_destination = output_destination

    def __repr__(self):
        return f"{self.__class__.__name__}({self.batchfile}, {self.output_type}, {self.output_destination})"

    def __iter__(self):
        yield MSDRGGrouperSoftwareOptions.Input.value
        yield str(self.batchfile)
        yield self.output_type.value
        yield str(self.output_destination)


class GrouperInterface(ABC):
    """Base class for interfacing with the Grouper software"""
    @abstractmethod
    def group(self, *args, **kwargs) -> bool:
        pass


class MSDRGGrouperSoftwareInterface(GrouperInterface):
    """Class responsible for calling the MS-DRG Grouper program"""

    msgmce = "msgmce.bat"

    def __init__(self, grouper_directory: Path) -> None:
        self.grouper_filepath = grouper_directory

    def group(self, params: MSDRGGrouperSoftwareParameters) -> bool:
        command = [self.msgmce, *params]
        with working_directory(self.grouper_filepath):
            subprocess.Popen(command)
        return True

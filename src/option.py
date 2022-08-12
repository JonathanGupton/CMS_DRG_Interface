from abc import ABC, abstractmethod
from typing import Sequence, Optional


class Option(ABC):
    """Base class for the CMS Grouper Options"""

    @abstractmethod
    def __str__(self):
        pass


class InputFileOption(Option):
    def __init__(self, input_filepath):
        self.input_filepath = input_filepath

    def __str__(self):
        return f" -i {self.input_filepath}"

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.input_filepath}")'


class OutputFileOption(Option):
    def __init__(self, output_filepath):
        self.output_filepath = output_filepath

    def __str__(self):
        return f" -o {self.output_filepath}"

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.output_filepath}")'


class UploadFileOption(Option):
    def __init__(self, upload_filepath):
        self.upload_filepath = upload_filepath

    def __str__(self):
        return f" -u {self.upload_filepath}"

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.upload_filepath}")'


class Options:
    """Collection of Grouper Options"""

    def __init__(self, options: Optional[Sequence[Option]] = None) -> None:
        self.options = list(options) if options else list()

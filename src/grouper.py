from abc import ABC, abstractmethod
from typing import Optional, Type

from src.adapter import MSDRGGrouperSoftwareInterface, MSDRGGrouperSoftwareParameter
from src.parameter import GrouperParameter
from src.config import CONFIG
from src.record import OutputRecord, load_output_from_file


class GrouperProcessorBase(ABC):
    """Base object for the handling of grouping beginning to end."""

    @abstractmethod
    def group(self, params: GrouperParameter) -> list[OutputRecord]:
        pass


class MSDRGGrouperSoftwareGrouper(GrouperProcessorBase):
    """
    Class responsible for handling the standing up of the input file, grouping,
    and tearing down of the output file as part of the grouping process with the
    CMS MS-DRG Grouper.
    """

    grouper_interface = MSDRGGrouperSoftwareInterface

    def __init__(self):
        self._interface: MSDRGGrouperSoftwareInterface = self.grouper_interface()

    @staticmethod
    def _standup(params: MSDRGGrouperSoftwareParameter):
        """Write the batchfile to disk"""
        params.batch.to_file(params.batchfile_path)

    @staticmethod
    def _teardown(params: MSDRGGrouperSoftwareParameter):
        """Remove any unneeded files after grouping"""
        if params.delete_input_file:
            params.batchfile_path.unlink()
        if params.delete_output_file:
            params.output_destination.unlink()

    def group(self, params: MSDRGGrouperSoftwareParameter):
        self._standup(params)
        self._interface.group(params)
        output = load_output_from_file(params.output_destination)
        self._teardown(params)
        return output


GROUPER_MAP = {"CMS_MCE_GROUPER": MSDRGGrouperSoftwareGrouper}


class Grouper:
    """
    Main class for calling the grouper.  This instantiates with the default
    grouper in the config file if not otherwise specified.
    """

    grouper_default: Type[GrouperProcessorBase] = GROUPER_MAP[
        CONFIG["DEFAULTS"]["grouper"]
    ]

    def __init__(self, grouper: Optional[GrouperProcessorBase] = None):
        if grouper is None:
            self.grouper = self.grouper_default()
        else:
            self.grouper = grouper

    def group(self, params: GrouperParameter) -> list[OutputRecord]:
        return self.grouper.group(params)

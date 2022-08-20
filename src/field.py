from abc import ABC, abstractmethod


class Field(ABC):
    """Base Class used for all record fields"""

    @abstractmethod
    def __str__(self):
        raise NotImplementedError

    def __len__(self):
        return len(str(self))

    @classmethod
    @abstractmethod
    def extract_from_output(cls, output):
        """Method to extract the field information from a grouped output string"""
        raise NotImplementedError

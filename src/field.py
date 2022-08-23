from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


class Field(ABC):
    """Base Class used for all record fields"""

    field_length = 0
    position = 0
    occurrence = 0

    def __init__(self, value) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    def __len__(self) -> int:
        return len(str(self))

    @classmethod
    def new_from_output_string(cls, output: str) -> Field:
        """Method to extract the field information from a grouped output string"""
        field_string = cls.isolate_field_str(output)
        return cls(cls.parse_field_string(field_string))

    @classmethod
    @abstractmethod
    def parse_field_string(cls, field_str: str) -> Any:
        """Convert the string slice extracted from the output file to the
        field's value type."""
        raise NotImplementedError

    @classmethod
    def isolate_field_str(cls, output: str) -> str:
        """Extract the field specific string from the output string"""
        return output[cls.position : cls.position + cls.field_length]

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable, Iterator, Optional, Type


from src.record import Record


class Batch:
    """Object containing records for the CMS Batch grouper"""

    def __init__(self, records: Optional[Iterable[Record]]) -> None:
        if not records:
            self.records = []
        else:
            self.records = list(records)

    def __iter__(self) -> Iterator[Record]:
        return iter(self.records)

    def __len__(self) -> int:
        return len(self.records)

    def __str__(self) -> str:
        return "\n".join(map(str, self))

    def __repr__(self) -> str:
        return str(self)

    def add_record(self, record) -> None:
        self.records.append(record)


class BatchFileObject(ABC):
    """Base class specifying the file type used to store the batch data"""

    def __init__(self, filepath):
        self.filepath = Path(filepath)

    def write(self, batch) -> None:
        with open(self.filepath, "w") as f:
            f.write(str(batch))

    @abstractmethod
    def cleanup(self):
        pass

class BatchFile(BatchFileObject):
    """Create a permanent batch data file"""
    def __init__(self, filepath):
        super().__init__(filepath)

    def cleanup(self):
        pass


class TemporaryBatchFile(BatchFileObject):
    """Create a temporary batch data file that will be deleted after closing"""
    def __init__(self, filepath):
        super().__init__(filepath)

    def cleanup(self):
        self.filepath.unlink()


class BatchFileHandler:
    """Object used to handle the writing and clean up of batch data files"""

    def __init__(self, filepath, batch_file_object: Type[BatchFileObject] = TemporaryBatchFile) -> None:
        self.batch_file = batch_file_object(filepath)

    def write(self, batch):
        """
        Write the batch data to file
        """
        self.batch_file.write(batch)

    def cleanup(self):
        self.batch_file.cleanup()

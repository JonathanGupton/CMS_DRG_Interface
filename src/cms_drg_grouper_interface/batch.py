from pathlib import Path
from typing import Iterable, Iterator, Optional

from record import InputRecord


class Batch:
    """Object containing records for the CMS Batch grouper"""

    def __init__(self, records: Optional[Iterable[InputRecord]]) -> None:
        if not records:
            self.records = []
        else:
            self.records = list(records)

    def __iter__(self) -> Iterator[InputRecord]:
        return iter(self.records)

    def __len__(self) -> int:
        return len(self.records)

    def __str__(self) -> str:
        return "\n".join(map(str, self))

    def __repr__(self) -> str:
        return str(self)

    def add_record(self, record) -> None:
        self.records.append(record)

    def to_file(self, filepath: Path) -> None:
        with open(filepath, "w") as f:
            f.write(str(self))

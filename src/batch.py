from typing import Iterable, Iterator, Optional

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
        return "".join(map(str, self))

    def add_record(self, record) -> None:
        self.records.append(record)

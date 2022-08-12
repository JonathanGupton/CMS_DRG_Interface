from batch import Batch
from option import Options


class Grouper:
    """
    Adapter for the CMS DRG Grouper
    """
    def __init__(self, grouper_path: str) -> None:
        self.grouper_path = grouper_path

    def __enter__(self):
        # check that the grouper exists
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def group(self, batch: Batch, options: Options):
        pass

from pathlib import Path

from src.batch import Batch, BatchFile
from src.filehandler import FileHandler


def test_batch(example_record):
    batch = Batch([example_record])
    assert len(batch) == 1
    assert len(str(batch)) == 835

    batch.add_record(example_record)
    assert len(batch) == 2
    assert len(str(batch)) == 835 * 2


def test_batchwriter_write_to_tempfile(example_record):
    batch = Batch([example_record])

    filepath = Path.cwd() / Path("input.txt")
    batch_handler = FileHandler(filepath=filepath)
    assert not filepath.exists()
    batch_handler.write(batch)
    assert filepath.exists()
    batch_handler.cleanup()
    assert not filepath.exists()


def test_batchwriter_write_to_file(example_record):
    batch = Batch([example_record])

    filepath = Path.cwd() / Path("input.txt")
    batch_handler = FileHandler(filepath=filepath, batch_file_object=BatchFile)
    assert not filepath.exists()
    batch_handler.write(batch)
    assert filepath.exists()
    batch_handler.cleanup()
    assert filepath.exists()
    filepath.unlink()  # clean up file
    assert not filepath.exists()

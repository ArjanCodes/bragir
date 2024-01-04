import pytest

from bragir.file import calculate_file_size


def test_calculate_file_size_nonexistent_file():
    # Test the calculate_file_size function with a non-existent file path
    with pytest.raises(FileNotFoundError):
        calculate_file_size("nonexistent_file.txt")

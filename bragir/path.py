import os

from bragir.constants import BLACKLISTED_FILES


def get_files_in_directory(path: str) -> list[str]:
    directory_file_paths: list[str] = []
    for root, _dirs, nested_files in os.walk(path):
        for nested_file in nested_files:
            if nested_file not in BLACKLISTED_FILES:
                # Create the full path to the file
                directory_file_paths.append(os.path.join(root, nested_file))
    return directory_file_paths

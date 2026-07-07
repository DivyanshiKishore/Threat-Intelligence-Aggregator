"""
Feed discovery utilities.
"""

from pathlib import Path
from typing import List


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".csv",
    ".json",
}

class FeedLoader:
    """
    Discovers IOC feed filed from the projects.
    """
    def __init__(self, base_directory: Path):
        self.base_directory = base_directory

    def discover(self) -> List[Path]:
        """
        Discover all supported feed files.
        """
        discovered = []

        for folder in ("remote", "local"):
            feed_directory = self.base_directory / folder

            if not feed_directory.exists():
                continue

            for file in feed_directory.iterdir():
                if (
                    file.is_file()
                    and file.suffix.lower() in SUPPORTED_EXTENSIONS
                ):
                    discovered.append(file)

        return sorted(discovered)
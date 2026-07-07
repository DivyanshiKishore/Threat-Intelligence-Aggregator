"""
Base parser interface for all IOC parsers.
"""

from abc import ABC, abstractmethod
from pathlib import Path


class BaseParser(ABC):
    """
    Abstract base class for IOC parsers.
    """

    @abstractmethod
    def parse(self, file_path: Path) -> list[str]:
        """
        Parse a feed file and return extracted IOC values.

        Args:
            file_path: Path to the feed file.

        Returns:
            A list of extracted IOC strings.
        """
        raise NotImplementedError
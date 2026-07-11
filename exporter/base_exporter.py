from abc import ABC, abstractmethod
from pathlib import Path
from typing import Sequence

from normalizer.schema import IOC


class BaseExporter(ABC):
    """
    Abstract base class for IOC exporters.
    """

    @abstractmethod
    def export(self, iocs: Sequence[IOC], output_path: Path) -> None:
        """
        Export IOCs to the specified output file.

        Args:
            iocs: Collection of IOC objects.
            output_path: Destination file path.
        """
        raise NotImplementedError
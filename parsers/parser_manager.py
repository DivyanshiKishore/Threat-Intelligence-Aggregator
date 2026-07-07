from pathlib import Path
from typing import Dict, List

from normalizer.schema import IOC
from parsers.base_parser import BaseParser
from parsers.csv_parser import CSVParser
from parsers.json_parser import JSONParser
from parsers.txt_parser import TXTParser
from utils.logger import get_logger

logger = get_logger(__name__)


class ParserManager:
    """
    Selects the appropriate parser based on file extension.
    """

    def __init__(self) -> None:
        self._parsers: Dict[str, BaseParser] = {
            ".txt": TXTParser(),
            ".csv": CSVParser(),
            ".json": JSONParser(),
        }

    def parse(self, file_path: Path) -> List[IOC]:
        """
        Parse a file using the appropriate parser.

        Args:
            file_path: Path to the feed file.

        Returns:
            List of IOC objects.

        Raises:
            ValueError: If the file extension is unsupported.
        """

        extension = file_path.suffix.lower()

        parser = self._parsers.get(extension)

        if parser is None:
            logger.error("Unsupported file type: %s", extension)
            raise ValueError(f"Unsupported file type: {extension}")

        logger.info(
            "Using %s for %s",
            parser.__class__.__name__,
            file_path.name,
        )

        return parser.parse(file_path)
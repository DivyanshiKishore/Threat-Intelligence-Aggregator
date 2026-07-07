"""
TXT parser for IOC feeds.
"""

from pathlib import Path
from typing import List

from normalizer.schema import IOC
from parsers.base_parser import BaseParser
from utils.logger import get_logger


logger = get_logger(__name__)


class TXTParser(BaseParser):
    """
    Parser for plain text IOC feeds.

    Expected format:
        One IOC per line

    Example:
        8.8.8.8
        example.com
    """

    def parse(self, file_path: Path) -> List[IOC]:
        """
        Read a TXT file and convert entries into IOC objects.

        Args:
            file_path: Path to TXT feed.

        Returns:
            List of IOC objects.
        """

        iocs: List[IOC] = []

        try:
            with file_path.open(
                "r",
                encoding="utf-8"
            ) as file:

                for line in file:
                    value = line.strip()

                    if not value:
                        continue

                    iocs.append(
                        IOC(
                            type="unknown",
                            value=value,
                            source=file_path.name,
                        )
                    )

        except Exception as exc:
            logger.exception(
                "Failed parsing TXT file %s: %s",
                file_path,
                exc,
            )
            return []

        logger.info(
            "Parsed %d IOCs from %s",
            len(iocs),
            file_path.name,
        )

        return iocs
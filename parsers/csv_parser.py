"""
CSV parser for IOC feeds.
"""

import csv
from pathlib import Path
from typing import List

from normalizer.schema import IOC
from parsers.base_parser import BaseParser
from utils.logger import get_logger


logger = get_logger(__name__)


class CSVParser(BaseParser):
    """
    Parser for CSV IOC feeds.

    Supported CSV formats:

    Format 1:
        type,value

    Example:
        ip,8.8.8.8
        domain,example.com


    Format 2:
        indicator

    Example:
        8.8.8.8
        example.com
    """

    def parse(self, file_path: Path) -> List[IOC]:
        """
        Read a CSV feed and convert entries into IOC objects.

        Args:
            file_path: Path to CSV feed.

        Returns:
            List of IOC objects.
        """

        iocs: List[IOC] = []

        try:
            with file_path.open(
                "r",
                encoding="utf-8",
                newline=""
            ) as file:

                lines = []

                for line in file:
                    stripped = line.strip()

                    if not stripped:
                        continue

                    if stripped.startswith("#"):
                        header = stripped.lstrip("#").strip()

                        # URLhaus header
                        if header.startswith("id,"):
                            lines.append(header)

                        continue
                    
                    lines.append(line)

                reader = csv.DictReader(lines)

                if not reader.fieldnames:
                    logger.warning(
                        "CSV file has no headers: %s",
                        file_path,
                    )
                    return []

                for row in reader:

                    ioc_type = row.get("type")
                    value = row.get("value")

                    # Support indicator-only feeds
                    if not value:
                        value = row.get("indicator")

                    # Support URLhaus feeds
                    if not value:
                        value = row.get("url")

                    # Infer IOC type for URLhaus
                    if value and not ioc_type and row.get("url"):
                        ioc_type = "url"

                    if not value:
                        continue

                    iocs.append(
                        IOC(
                            type=ioc_type or "unknown",
                            value=value,
                            sources=[file_path.name],
                        )
                    )

        except Exception as exc:
            logger.exception(
                "Failed parsing CSV file %s: %s",
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
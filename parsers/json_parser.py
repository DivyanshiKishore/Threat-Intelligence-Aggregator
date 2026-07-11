import json
from pathlib import Path
from typing import List

from normalizer.schema import IOC
from parsers.base_parser import BaseParser
from utils.logger import get_logger

logger = get_logger(__name__)


class JSONParser(BaseParser):
    """
    Parses JSON-based threat intelligence feeds.

    Supported formats:
        - List of IOC dictionaries
        - {"iocs": [...]}
        - Single IOC dictionary
    """

    def parse(self, file_path: Path) -> List[IOC]:
        """
        Parse a JSON feed into IOC objects.

        Args:
            file_path: Path to JSON feed.

        Returns:
            List of IOC objects.
        """

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

        except json.JSONDecodeError:
            logger.error("Invalid JSON: %s", file_path)
            return []

        except Exception as exc:
            logger.exception("Failed parsing %s: %s", file_path, exc)
            return []

        records = []

        if isinstance(data, list):
            records = data

        elif isinstance(data, dict):

            if "iocs" in data and isinstance(data["iocs"], list):
                records = data["iocs"]

            elif "type" in data and "value" in data:
                records = [data]

            else:
                logger.warning(
                    "Unsupported JSON structure: %s",
                    file_path
                )
                return []

        else:
            logger.warning("Unexpected JSON type in %s", file_path)
            return []

        parsed: List[IOC] = []

        for record in records:

            if not isinstance(record, dict):
                continue

            ioc_type = record.get("type")
            value = record.get("value")

            if not ioc_type or not value:
                continue

            parsed.append(
                IOC(
                    type=str(ioc_type),
                    value=str(value),
                    sources=file_path.name,
                )
            )

        logger.info(
            "Parsed %d IOCs from %s",
            len(parsed),
            file_path.name,
        )

        return parsed
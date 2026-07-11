import json
from pathlib import Path
from typing import Sequence

from exporter.base_exporter import BaseExporter
from normalizer.schema import IOC


class JSONExporter(BaseExporter):
    """
    Exports IOCs to a JSON file.
    """

    def export(self, iocs: Sequence[IOC], output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        data = [
            {
                "type": ioc.type,
                "value": ioc.value,
                "sources": ioc.sources,
                "confidence": ioc.confidence,
                "tags": ioc.tags,
                "first_seen": ioc.first_seen,
                "last_seen": ioc.last_seen,
            }
            for ioc in iocs
        ]

        with output_path.open("w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)
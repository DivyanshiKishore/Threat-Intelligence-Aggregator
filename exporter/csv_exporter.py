import csv
from pathlib import Path
from typing import Sequence

from exporter.base_exporter import BaseExporter
from normalizer.schema import IOC


class CSVExporter(BaseExporter):
    """
    Exports IOCs to a CSV file.
    """

    def export(self, iocs: Sequence[IOC], output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as csv_file:
            writer = csv.writer(csv_file)

            writer.writerow(
                [
                    "type",
                    "value",
                    "sources",
                    "confidence",
                    "tags",
                    "first_seen",
                    "last_seen",
                ]
            )

            for ioc in iocs:
                writer.writerow(
                    [
                        ioc.type,
                        ioc.value,
                        ",".join(ioc.sources),
                        ioc.confidence,
                        ",".join(ioc.tags),
                        ioc.first_seen,
                        ioc.last_seen,
                    ]
                )
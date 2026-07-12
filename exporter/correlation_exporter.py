from csv import DictWriter
from pathlib import Path
from typing import Sequence

from exporter.base_exporter import BaseExporter
from normalizer.schema import IOC


class CorrelationExporter(BaseExporter):
    """
    Exports IOC correlation data to a CSV file.
    """

    def export(
        self,
        iocs: Sequence[IOC],
        output_path: Path,
    ) -> None:
        """
        Export IOC correlation report.

        Args:
            iocs: Deduplicated IOC collection.
            output_path: Destination CSV file.
        """

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        sorted_iocs = sorted(
            iocs,
            key=lambda ioc: (
                -len(ioc.sources),
                ioc.type,
                ioc.value,
            ),
        )

        with output_path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as csv_file:

            writer = DictWriter(
                csv_file,
                fieldnames=[
                    "ioc",
                    "type",
                    "feed_count",
                    "sources",
                    "confidence",
                ],
            )

            writer.writeheader()

            for ioc in sorted_iocs:
                writer.writerow(
                    {
                        "ioc": ioc.value,
                        "type": ioc.type,
                        "feed_count": len(ioc.sources),
                        "sources": ", ".join(ioc.sources),
                        "confidence": ioc.confidence,
                    }
                )
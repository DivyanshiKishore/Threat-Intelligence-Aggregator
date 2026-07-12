from collections import Counter
from pathlib import Path
from typing import Sequence

from exporter.base_exporter import BaseExporter
from normalizer.schema import IOC


class ReportExporter(BaseExporter):
    """
    Exports a Threat Intelligence summary report.
    """

    def export(
        self,
        iocs: Sequence[IOC],
        output_path: Path,
    ) -> None:
        """
        Export a human-readable Threat Intelligence report.

        Args:
            iocs: Deduplicated IOC collection.
            output_path: Destination report file.
        """

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        type_counts = Counter(
            ioc.type for ioc in iocs
        )

        top_indicators = sorted(
            iocs,
            key=lambda ioc: (
                -len(ioc.sources),
                ioc.type,
                ioc.value,
            ),
        )[:10]

        with output_path.open(
            "w",
            encoding="utf-8",
        ) as report:

            report.write("=" * 70 + "\n")
            report.write("Threat Intelligence Aggregator Report\n")
            report.write("=" * 70 + "\n\n")

            report.write(
                f"Total IOCs: {len(iocs)}\n\n"
            )

            report.write("IOC Type Distribution\n")
            report.write("-" * 70 + "\n")

            for ioc_type in sorted(type_counts):
                report.write(
                    f"{ioc_type:<15}: {type_counts[ioc_type]}\n"
                )

            report.write("\n")

            report.write("Top Correlated Indicators\n")
            report.write("-" * 70 + "\n")

            if not top_indicators:
                report.write("No indicators available.\n")
            else:
                for ioc in top_indicators:
                    report.write(
                        f"{ioc.value}\n"
                    )
                    report.write(
                        f"  Type        : {ioc.type}\n"
                    )
                    report.write(
                        f"  Feed Count  : {len(ioc.sources)}\n"
                    )
                    report.write(
                        f"  Sources     : {', '.join(ioc.sources)}\n"
                    )
                    report.write(
                        f"  Confidence  : {ioc.confidence}\n\n"
                    )
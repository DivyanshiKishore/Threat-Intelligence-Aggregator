from pathlib import Path
from typing import Sequence

from exporter.base_exporter import BaseExporter
from normalizer.schema import IOC


class BlocklistExporter(BaseExporter):
    """
    Exports deployment-ready IOC blocklists.
    """

    def export(
        self,
        iocs: Sequence[IOC],
        output_directory: Path,
    ) -> None:
        """
        Export IOC blocklists grouped by type.

        Args:
            iocs: Deduplicated IOC collection.
            output_directory: Directory where blocklists will be written.
        """

        output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        blocklists = {
            "ipv4": [],
            "ipv6": [],
            "domain": [],
            "url": [],
            "md5": [],
            "sha1": [],
            "sha256": [],
        }

        for ioc in iocs:
            if ioc.type in blocklists:
                blocklists[ioc.type].append(ioc.value)

        for ioc_type, values in blocklists.items():
            output_file = output_directory / f"{ioc_type}_blocklist.txt"

            with output_file.open(
                "w",
                encoding="utf-8",
            ) as file:

                for value in sorted(set(values)):
                    file.write(f"{value}\n")
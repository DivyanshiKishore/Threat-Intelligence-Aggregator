"""
Utilities for formatting threat intelligence reports.
"""

from typing import Dict


class Summary:
    """
    Formats statistical data into a human-readable report.
    """

    @staticmethod
    def generate(statistics: Dict) -> str:
        """
        Generate a formatted threat intelligence summary.

        Args:
            statistics: Dictionary containing report statistics.

        Returns:
            A formatted report string.
        """

        lines = []

        lines.append("Threat Intelligence Summary")
        lines.append("=" * 30)
        lines.append("")

        lines.append(f"Total IOCs: {statistics['total']}")
        lines.append("")

        lines.append("IOC Types")
        lines.append("-" * 20)

        for ioc_type, count in statistics["types"].items():
            lines.append(f"{ioc_type:<15} : {count}")

        lines.append("")

        lines.append("Sources")
        lines.append("-" * 20)

        for source, count in statistics["sources"].items():
            lines.append(f"{source:<15} : {count}")

        lines.append("")

        lines.append("Confidence Distribution")
        lines.append("-" * 25)

        for bucket, count in statistics["confidence"].items():
            lines.append(f"{bucket:<15} : {count}")

        lines.append("")

        lines.append("Tags")
        lines.append("-" * 20)

        for tag, count in statistics["tags"].items():
            lines.append(f"{tag:<15} : {count}")

        return "\n".join(lines)
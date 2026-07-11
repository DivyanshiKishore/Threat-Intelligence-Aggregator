"""
Report generation utilities.
"""

from pathlib import Path
from typing import List

from normalizer.schema import IOC
from reports.statistics import Statistics
from reports.summary import Summary


class ReportGenerator:
    """
    Generates threat intelligence reports from IOC collections.
    """

    @staticmethod
    def generate(iocs: List[IOC]) -> str:
        """
        Generate a formatted threat intelligence report.

        Args:
            iocs: List of IOC objects.

        Returns:
            Formatted report string.
        """

        statistics = {
            "total": Statistics.total_iocs(iocs),
            "types": Statistics.count_by_type(iocs),
            "sources": Statistics.count_by_source(iocs),
            "confidence": Statistics.confidence_distribution(iocs),
            "tags": Statistics.tag_statistics(iocs),
        }

        return Summary.generate(statistics)

    @staticmethod
    def save(report: str, output_file: str) -> None:
        """
        Save a report to a text file.

        Args:
            report: Report text.
            output_file: Destination file path.
        """

        output_path = Path(output_file)
        output_path.write_text(report, encoding="utf-8")
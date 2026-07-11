"""
Statistical analysis utilities for IOC collections.
"""
from collections import Counter
from typing import Dict, List

from normalizer.schema import IOC


class Statistics:
    """
    Provides statistical summaries for collections of IOCs.
    """

    @staticmethod
    def total_iocs(iocs: List[IOC]) -> int:
        """
        Return the total number of IOCs.
        """
        return len(iocs)

    @staticmethod
    def count_by_type(iocs: List[IOC]) -> Dict[str, int]:
        """
        Count IOCs grouped by type.

        Returns:
            Dictionary mapping IOC type to count.
        """
        counter = Counter()

        for ioc in iocs:
            counter[ioc.type] += 1

        return dict(counter)

    @staticmethod
    def count_by_source(iocs: List[IOC]) -> Dict[str, int]:
        """
        Count occurrences of each data source.

        Since one IOC may originate from multiple sources,
        every source is counted individually.
        """
        counter = Counter()

        for ioc in iocs:
            for source in ioc.sources:
                counter[source] += 1

        return dict(counter)

    @staticmethod
    def confidence_distribution(iocs: List[IOC]) -> Dict[str, int]:
        """
        Group confidence scores into ranges.

        Buckets:
            0-25
            26-50
            51-75
            76-100
        """
        distribution = {
            "0-25": 0,
            "26-50": 0,
            "51-75": 0,
            "76-100": 0,
        }

        for ioc in iocs:
            confidence = ioc.confidence

            if 0 <= confidence <= 25:
                distribution["0-25"] += 1
            elif 26 <= confidence <= 50:
                distribution["26-50"] += 1
            elif 51 <= confidence <= 75:
                distribution["51-75"] += 1
            elif 76 <= confidence <= 100:
                distribution["76-100"] += 1

        return distribution

    @staticmethod
    def tag_statistics(iocs: List[IOC]) -> Dict[str, int]:
        """
        Count occurrences of IOC tags.
        """
        counter = Counter()

        for ioc in iocs:
            for tag in ioc.tags:
                counter[tag] += 1

        return dict(counter)
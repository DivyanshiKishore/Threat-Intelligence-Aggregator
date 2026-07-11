"""
IOC deduplication utilities.
"""

from copy import deepcopy
from typing import Dict, List, Tuple

from normalizer.schema import IOC
from utils.logger import get_logger

logger = get_logger(__name__)


class IOCDeduplicator:
    """
    Merge duplicate IOCs into a single IOC.

    Two IOCs are considered duplicates if they share the
    same (type, value) pair.
    """

    def deduplicate(self, iocs: List[IOC]) -> List[IOC]:
        """
        Deduplicate a list of IOCs.

        Args:
            iocs: List of IOC objects.

        Returns:
            List of deduplicated IOC objects.
        """

        deduplicated: Dict[Tuple[str, str], IOC] = {}

        for ioc in iocs:
            key = (ioc.type, ioc.value)

            if key not in deduplicated:
                deduplicated[key] = deepcopy(ioc)
            else:
                self._merge_iocs(
                    deduplicated[key],
                    ioc,
                )

        logger.info(
            "Deduplicated %d IOCs into %d unique IOCs.",
            len(iocs),
            len(deduplicated),
        )

        return list(deduplicated.values())

    def _merge_iocs(
        self,
        existing: IOC,
        new: IOC,
    ) -> None:
        """
        Merge duplicate IOC data into the existing IOC.

        Args:
            existing: IOC already stored.
            new: Duplicate IOC to merge.
        """

        # Keep the highest confidence score.
        existing.confidence = max(
            existing.confidence,
            new.confidence,
        )

        # Merge tags uniquely.
        existing.tags = sorted(
            set(existing.tags) | set(new.tags)
        )

        # Merge sources uniquely.
        existing.sources = sorted(
            set(existing.sources) | set(new.sources)
        )

        # Preserve the first available first_seen.
        if existing.first_seen is None:
            existing.first_seen = new.first_seen

        # Preserve the first available last_seen.
        if existing.last_seen is None:
            existing.last_seen = new.last_seen
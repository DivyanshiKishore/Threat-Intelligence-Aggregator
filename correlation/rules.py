"""
Correlation rules.
"""

from abc import ABC, abstractmethod

from correlation.models import Relationship
from normalizer.schema import IOC


class BaseCorrelationRule(ABC):
    """
    Base class for all IOC correlation rules.
    """

    @abstractmethod
    def apply(
        self,
        iocs: list[IOC],
    ) -> list[Relationship]:
        """
        Apply the correlation rule.

        Args:
            iocs:
                List of normalized IOCs.

        Returns:
            List of discovered relationships.
        """
        raise NotImplementedError


class SharedTagRule(BaseCorrelationRule):
    """
    Correlates IOCs that share one or more tags.
    """

    def apply(
        self,
        iocs: list[IOC],
    ) -> list[Relationship]:
        """
        Find relationships between IOCs
        with common tags.
        """

        relationships: list[Relationship] = []

        for index, source in enumerate(iocs):
            for target in iocs[index + 1:]:

                shared_tags = (
                    set(source.tags)
                    & set(target.tags)
                )

                if not shared_tags:
                    continue

                relationships.append(
                    Relationship(
                        source=source,
                        target=target,
                        relation="shared_tag",
                        confidence=min(
                            source.confidence,
                            target.confidence,
                        ),
                    )
                )

        return relationships

class SharedSourceRule(BaseCorrelationRule):
    """
    Correlates IOCs that originate from one or more common sources.
    """

    def apply(
        self,
        iocs: list[IOC],
    ) -> list[Relationship]:
        """
        Find relationships between IOCs
        with common sources.
        """

        relationships: list[Relationship] = []

        for index, source in enumerate(iocs):
            for target in iocs[index + 1:]:
                shared_sources = (
                    set(source.sources)
                    & set(target.sources)
                )

                if not shared_sources:
                    continue

                relationships.append(
                    Relationship(
                        source=source,
                        target=target,
                        relation="shared_source",
                        confidence=min(
                            source.confidence,
                            target.confidence,
                        ),
                    )
                )

        return relationships
"""
Data models for IOC correlation.
"""

from dataclasses import dataclass

from normalizer.schema import IOC


@dataclass(slots=True)
class Relationship:
    """
    Represents a relationship between two IOCs.
    """

    source: IOC
    target: IOC
    relation: str
    confidence: int = 0
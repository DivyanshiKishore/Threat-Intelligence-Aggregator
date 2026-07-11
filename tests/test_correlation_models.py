"""
Unit tests for correlation models.
"""

from correlation.models import Relationship
from normalizer.schema import IOC


def test_relationship_creation() -> None:
    """
    Test Relationship object creation with default confidence.
    """
    source = IOC(
        type="domain",
        value="example.com",
        sources=["FeedA"],
    )

    target = IOC(
        type="url",
        value="https://example.com/login",
        sources=["FeedA"],
    )

    relationship = Relationship(
        source=source,
        target=target,
        relation="contains_domain",
    )

    assert relationship.source == source
    assert relationship.target == target
    assert relationship.relation == "contains_domain"
    assert relationship.confidence == 0


def test_relationship_custom_confidence() -> None:
    """
    Test Relationship object creation with custom confidence.
    """
    source = IOC(
        type="ip",
        value="8.8.8.8",
        sources=["FeedA"],
    )

    target = IOC(
        type="domain",
        value="example.com",
        sources=["FeedA"],
    )

    relationship = Relationship(
        source=source,
        target=target,
        relation="related_to",
        confidence=90,
    )

    assert relationship.confidence == 90
"""
Unit tests for correlation rules.
"""

from correlation.rules import (
    SharedSourceRule,
    SharedTagRule,
)
from normalizer.schema import IOC


def test_shared_tag_rule_creates_relationship() -> None:
    """
    Test that two IOCs sharing a tag are correlated.
    """
    rule = SharedTagRule()

    ioc1 = IOC(
        type="ip",
        value="1.1.1.1",
        sources=["FeedA"],
        confidence=80,
        tags=["phishing"],
    )

    ioc2 = IOC(
        type="domain",
        value="example.com",
        sources=["FeedB"],
        confidence=90,
        tags=["phishing"],
    )

    relationships = rule.apply([ioc1, ioc2])

    assert len(relationships) == 1

    relationship = relationships[0]

    assert relationship.relation == "shared_tag"
    assert relationship.source == ioc1
    assert relationship.target == ioc2
    assert relationship.confidence == 80


def test_shared_tag_rule_no_relationship() -> None:
    """
    Test that unrelated IOCs produce no relationships.
    """
    rule = SharedTagRule()

    ioc1 = IOC(
        type="ip",
        value="1.1.1.1",
        sources=["FeedA"],
        tags=["malware"],
    )

    ioc2 = IOC(
        type="domain",
        value="example.com",
        sources=["FeedB"],
        tags=["phishing"],
    )

    relationships = rule.apply([ioc1, ioc2])

    assert relationships == []

def test_shared_source_rule_creates_relationship() -> None:
    """
    Test that IOCs sharing a source are correlated.
    """

    rule = SharedSourceRule()

    ioc1 = IOC(
        type="ip",
        value="8.8.8.8",
        sources=["AlienVault"],
        confidence=90,
    )

    ioc2 = IOC(
        type="domain",
        value="example.com",
        sources=["AlienVault"],
        confidence=70,
    )

    relationships = rule.apply([ioc1, ioc2])

    assert len(relationships) == 1

    relationship = relationships[0]

    assert relationship.relation == "shared_source"
    assert relationship.confidence == 70


def test_shared_source_rule_no_relationship() -> None:
    """
    Test that different sources create no relationship.
    """

    rule = SharedSourceRule()

    ioc1 = IOC(
        type="ip",
        value="8.8.8.8",
        sources=["AlienVault"],
    )

    ioc2 = IOC(
        type="domain",
        value="example.com",
        sources=["URLHaus"],
    )

    relationships = rule.apply([ioc1, ioc2])

    assert relationships == []
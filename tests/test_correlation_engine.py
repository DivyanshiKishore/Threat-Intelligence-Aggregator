from correlation.correlation_engine import CorrelationEngine
from correlation.rules import SharedTagRule, SharedSourceRule
from normalizer.schema import IOC


def test_correlation_engine_executes_multiple_rules():

    ioc1 = IOC(
        type="domain",
        value="example.com",
        sources=["AlienVault"],
        tags=["phishing"],
    )

    ioc2 = IOC(
        type="ip",
        value="8.8.8.8",
        sources=["AlienVault"],
        tags=["phishing"],
    )

    engine = CorrelationEngine(
        [
            SharedTagRule(),
            SharedSourceRule(),
        ]
    )

    relationships = engine.correlate(
        [
            ioc1,
            ioc2,
        ]
    )

    assert len(relationships) == 2

    relation_types = {
        relationship.relation
        for relationship in relationships
    }

    assert "shared_tag" in relation_types
    assert "shared_source" in relation_types
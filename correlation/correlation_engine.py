"""
Correlation engine.
"""

from correlation.models import Relationship
from correlation.rules import BaseCorrelationRule
from normalizer.schema import IOC


class CorrelationEngine:
    """
    Executes all configured correlation rules.
    """

    def __init__(
        self,
        rules: list[BaseCorrelationRule],
    ) -> None:
        self._rules = rules

    def correlate(
        self,
        iocs: list[IOC],
    ) -> list[Relationship]:
        """
        Apply every configured rule.
        """
        relationships: list[Relationship] = []

        for rule in self._rules:
            relationships.extend(rule.apply(iocs))

        return relationships
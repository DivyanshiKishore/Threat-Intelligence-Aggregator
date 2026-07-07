"""
IOC normalization utilities.
"""

from copy import deepcopy
from urllib.parse import urlsplit, urlunsplit

from normalizer.schema import IOC


class IOCNormalizer:
    """
    Normalizes IOC objects into a consistent format.

    The normalizer standardizes IOC values but does NOT
    determine whether they are valid. Validation is handled
    separately by the validator module.
    """

    def normalize(self, ioc: IOC) -> IOC:
        """
        Return a normalized copy of an IOC.

        Args:
            ioc: IOC object.

        Returns:
            Normalized IOC object.
        """

        normalized = deepcopy(ioc)

        normalized.type = normalized.type.strip().lower()
        normalized.value = normalized.value.strip()

        if normalized.type in {"domain", "hostname"}:
            normalized.value = normalized.value.lower()

        elif normalized.type == "url":
            normalized.value = self._normalize_url(
                normalized.value
            )

        return normalized

    @staticmethod
    def _normalize_url(url: str) -> str:
        """
        Normalize URL while preserving path.

        Example:
            HTTPS://Example.COM/Login/

        becomes:

            https://example.com/Login/
        """

        parts = urlsplit(url)

        return urlunsplit(
            (
                parts.scheme.lower(),
                parts.netloc.lower(),
                parts.path,
                parts.query,
                parts.fragment,
            )
        )
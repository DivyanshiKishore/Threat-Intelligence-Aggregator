"""
IOC validation utilities.
"""

import ipaddress
import re
from urllib.parse import urlparse

from normalizer.schema import IOC


DOMAIN_REGEX = re.compile(
    r"^(?!-)(?:[A-Za-z0-9-]{1,63}\.)+[A-Za-z]{2,63}$"
)


def is_ipv4(value: str) -> bool:
    """Return True if value is a valid IPv4 address."""
    try:
        return isinstance(
            ipaddress.ip_address(value),
            ipaddress.IPv4Address,
        )
    except ValueError:
        return False


def is_ipv6(value: str) -> bool:
    """Return True if value is a valid IPv6 address."""
    try:
        return isinstance(
            ipaddress.ip_address(value),
            ipaddress.IPv6Address,
        )
    except ValueError:
        return False
    
def is_ipv4_network(value: str) -> bool:
    """Return True if value is a valid IPv4 CIDR network."""
    try:
        return isinstance(
            ipaddress.ip_network(
                value,
                strict=False,
            ),
            ipaddress.IPv4Network,
        )
    except ValueError:
        return False                  

def is_domain(value: str) -> bool:
    """Return True if value is a valid domain."""
    return bool(DOMAIN_REGEX.fullmatch(value))


def is_url(value: str) -> bool:
    """Return True if value is a valid URL."""

    parsed = urlparse(value)

    return (
        parsed.scheme in ("http", "https")
        and bool(parsed.netloc)
    )


def is_md5(value: str) -> bool:
    """Return True if value is MD5 hash."""

    return bool(
        re.fullmatch(
            r"[A-Fa-f0-9]{32}",
            value,
        )
    )


def is_sha1(value: str) -> bool:
    """Return True if value is SHA1 hash."""

    return bool(
        re.fullmatch(
            r"[A-Fa-f0-9]{40}",
            value,
        )
    )


def is_sha256(value: str) -> bool:
    """Return True if value is SHA256 hash."""

    return bool(
        re.fullmatch(
            r"[A-Fa-f0-9]{64}",
            value,
        )
    )


def detect_ioc_type(value: str) -> str | None:
    """
    Detect IOC type.
    """

    if is_ipv4(value) or is_ipv4_network(value):
        return "ipv4"
    
    if is_ipv6(value):
        return "ipv6"
    
    if is_url(value):
        return "url"

    if is_domain(value):
        return "domain"

    if is_md5(value):
        return "md5"

    if is_sha1(value):
        return "sha1"

    if is_sha256(value):
        return "sha256"

    return None


class IOCValidator:
    """
    Validator class for IOC objects.

    Provides an object-oriented interface
    over validation utilities.
    """

    def validate(
        self,
        ioc: IOC,
    ) -> bool:
        """
        Validate IOC object.

        Returns:
            True if IOC is valid.
        """

        detected_type = detect_ioc_type(
            ioc.value
        )

        if detected_type is None:
            return False

        ioc.type = detected_type

        return True
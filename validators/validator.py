"""

IOC validation utilities
"""

import ipaddress
import re
from urllib.parse import urlparse


DOMAIN_REGEX = re.compile(
    r"^(?!-)(?:[A-Za-z0-9-]{1,63}\.)+[A-Za-z]{2,63}$"
)


def is_ipv4(value: str) -> bool:
    """Return True if the value is a valid IPv4 address."""
    try:
        return isinstance(ipaddress.ip_address(value), ipaddress.IPv4Address)
    except ValueError:
        return False


def is_ipv6(value: str) -> bool:
    """Return True if the value is a valid IPv6 address."""
    try:
        return isinstance(ipaddress.ip_address(value), ipaddress.IPv6Address)
    except ValueError:
        return False


def is_domain(value: str) -> bool:
    """Return True if the value is a valid domain name."""
    return bool(DOMAIN_REGEX.fullmatch(value))


def is_url(value: str) -> bool:
    """Return True if the value is a valid HTTP or HTTPS URL."""
    parsed = urlparse(value)
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


def is_md5(value: str) -> bool:
    """Return True if the value looks like an MD5 hash."""
    return bool(re.fullmatch(r"[A-Fa-f0-9]{32}", value))


def is_sha1(value: str) -> bool:
    """Return True if the value looks like a SHA-1 hash."""
    return bool(re.fullmatch(r"[A-Fa-f0-9]{40}", value))
    

def is_sha256(value: str) -> bool:
    """Return True if the value looks like a SHA-256 hash."""
    return bool(re.fullmatch(r"[A-Fa-f0-9]{64}", value))


def detect_ioc_type(value: str) -> str | None:
    """
    Detect the IOC type from the given value.
    Returns the IOC type or None if unsupported.
    """

    if is_ipv4(value):
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
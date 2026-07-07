from normalizer.normalizer import IOCNormalizer
from normalizer.schema import IOC


def test_domain_normalization():
    normalizer = IOCNormalizer()

    original = IOC(
        type="DOMAIN",
        value="  GOOGLE.COM  ",
        source="test.txt",
    )

    normalized = normalizer.normalize(original)

    assert normalized.type == "domain"
    assert normalized.value == "google.com"

    # Original object should remain unchanged
    assert original.type == "DOMAIN"
    assert original.value == "  GOOGLE.COM  "


def test_url_normalization():
    normalizer = IOCNormalizer()

    original = IOC(
        type="URL",
        value="HTTPS://Example.COM/Login",
        source="test.txt",
    )

    normalized = normalizer.normalize(original)

    assert normalized.type == "url"
    assert normalized.value == "https://example.com/Login"


def test_ip_normalization():
    normalizer = IOCNormalizer()

    original = IOC(
        type="IP",
        value="   8.8.8.8   ",
        source="test.txt",
    )

    normalized = normalizer.normalize(original)

    assert normalized.type == "ip"
    assert normalized.value == "8.8.8.8"


def test_tags_are_preserved():
    normalizer = IOCNormalizer()

    original = IOC(
        type="DOMAIN",
        value="Example.COM",
        source="feed.txt",
        tags=["malware", "phishing"],
        confidence=90,
    )

    normalized = normalizer.normalize(original)

    assert normalized.tags == ["malware", "phishing"]
    assert normalized.confidence == 90
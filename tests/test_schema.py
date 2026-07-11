from normalizer.schema import IOC


def test_ioc_creation():
    ioc = IOC(
        type="ipv4",
        value="8.8.8.8",
        sources=["AlienVault"],
        confidence=90,
        tags=["malware", "botnet"],
    )

    assert ioc.type == "ipv4"
    assert ioc.value == "8.8.8.8"
    assert ioc.sources == ["AlienVault"]
    assert ioc.confidence == 90
    assert ioc.tags == ["malware", "botnet"]
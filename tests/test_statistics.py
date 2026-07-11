from normalizer.schema import IOC
from reports.statistics import Statistics


def create_ioc(
    ioc_type: str,
    value: str,
    sources=None,
    confidence=0,
    tags=None,
):
    return IOC(
        type=ioc_type,
        value=value,
        sources=sources or [],
        confidence=confidence,
        tags=tags or [],
    )


def test_total_iocs():
    iocs = [
        create_ioc("ipv4", "1.1.1.1"),
        create_ioc("domain", "example.com"),
    ]

    assert Statistics.total_iocs(iocs) == 2


def test_count_by_type():
    iocs = [
        create_ioc("ipv4", "1.1.1.1"),
        create_ioc("ipv4", "8.8.8.8"),
        create_ioc("domain", "example.com"),
    ]

    result = Statistics.count_by_type(iocs)

    assert result == {
        "ipv4": 2,
        "domain": 1,
    }


def test_count_by_source():
    iocs = [
        create_ioc(
            "ipv4",
            "1.1.1.1",
            sources=["AlienVault", "Abuse.ch"],
        ),
        create_ioc(
            "domain",
            "example.com",
            sources=["AlienVault"],
        ),
    ]

    result = Statistics.count_by_source(iocs)

    assert result == {
        "AlienVault": 2,
        "Abuse.ch": 1,
    }


def test_confidence_distribution():
    iocs = [
        create_ioc("ipv4", "1", confidence=10),
        create_ioc("ipv4", "2", confidence=30),
        create_ioc("ipv4", "3", confidence=70),
        create_ioc("ipv4", "4", confidence=90),
    ]

    result = Statistics.confidence_distribution(iocs)

    assert result == {
        "0-25": 1,
        "26-50": 1,
        "51-75": 1,
        "76-100": 1,
    }


def test_tag_statistics():
    iocs = [
        create_ioc(
            "ipv4",
            "1",
            tags=["malware", "botnet"],
        ),
        create_ioc(
            "domain",
            "example.com",
            tags=["malware"],
        ),
    ]

    result = Statistics.tag_statistics(iocs)

    assert result == {
        "malware": 2,
        "botnet": 1,
    }


def test_empty_ioc_list():
    iocs = []

    assert Statistics.total_iocs(iocs) == 0
    assert Statistics.count_by_type(iocs) == {}
    assert Statistics.count_by_source(iocs) == {}
    assert Statistics.tag_statistics(iocs) == {}

    assert Statistics.confidence_distribution(iocs) == {
        "0-25": 0,
        "26-50": 0,
        "51-75": 0,
        "76-100": 0,
    }
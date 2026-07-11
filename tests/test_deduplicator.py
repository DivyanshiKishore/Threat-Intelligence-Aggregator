from deduplication.deduplicator import IOCDeduplicator
from normalizer.schema import IOC


def test_deduplicate_empty_list():
    deduplicator = IOCDeduplicator()

    result = deduplicator.deduplicate([])

    assert result == []


def test_deduplicate_no_duplicates():
    deduplicator = IOCDeduplicator()

    iocs = [
        IOC(
            type="ip",
            value="8.8.8.8",
            sources=["FeedA"],
        ),
        IOC(
            type="domain",
            value="example.com",
            sources=["FeedB"],
        ),
    ]

    result = deduplicator.deduplicate(iocs)

    assert len(result) == 2


def test_deduplicate_merges_duplicates():
    deduplicator = IOCDeduplicator()

    iocs = [
        IOC(
            type="ip",
            value="8.8.8.8",
            sources=["FeedA"],
        ),
        IOC(
            type="ip",
            value="8.8.8.8",
            sources=["FeedB"],
        ),
    ]

    result = deduplicator.deduplicate(iocs)

    assert len(result) == 1


def test_highest_confidence_is_kept():
    deduplicator = IOCDeduplicator()

    iocs = [
        IOC(
            type="ip",
            value="8.8.8.8",
            confidence=20,
            sources=["FeedA"],
        ),
        IOC(
            type="ip",
            value="8.8.8.8",
            confidence=80,
            sources=["FeedB"],
        ),
    ]

    result = deduplicator.deduplicate(iocs)

    assert len(result) == 1
    assert result[0].confidence == 80


def test_tags_are_merged():
    deduplicator = IOCDeduplicator()

    iocs = [
        IOC(
            type="ip",
            value="8.8.8.8",
            tags=["malware"],
            sources=["FeedA"],
        ),
        IOC(
            type="ip",
            value="8.8.8.8",
            tags=["botnet"],
            sources=["FeedB"],
        ),
    ]

    result = deduplicator.deduplicate(iocs)

    assert sorted(result[0].tags) == [
        "botnet",
        "malware",
    ]


def test_sources_are_merged():
    deduplicator = IOCDeduplicator()

    iocs = [
        IOC(
            type="ip",
            value="8.8.8.8",
            sources=["FeedA"],
        ),
        IOC(
            type="ip",
            value="8.8.8.8",
            sources=["FeedB"],
        ),
    ]

    result = deduplicator.deduplicate(iocs)

    assert sorted(result[0].sources) == [
        "FeedA",
        "FeedB",
    ]


def test_same_value_different_types_not_merged():
    deduplicator = IOCDeduplicator()

    iocs = [
        IOC(
            type="domain",
            value="example.com",
            sources=["FeedA"],
        ),
        IOC(
            type="url",
            value="example.com",
            sources=["FeedB"],
        ),
    ]

    result = deduplicator.deduplicate(iocs)

    assert len(result) == 2


def test_first_seen_and_last_seen():
    deduplicator = IOCDeduplicator()

    iocs = [
        IOC(
            type="ip",
            value="8.8.8.8",
            first_seen="2024-01-01",
            sources=["FeedA"],
        ),
        IOC(
            type="ip",
            value="8.8.8.8",
            last_seen="2024-12-31",
            sources=["FeedB"],
        ),
    ]

    result = deduplicator.deduplicate(iocs)

    assert result[0].first_seen == "2024-01-01"
    assert result[0].last_seen == "2024-12-31"
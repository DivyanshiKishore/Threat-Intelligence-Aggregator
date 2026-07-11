import pytest

from src.feeds.models import FeedConfiguration
from src.feeds.exceptions import FeedConfigurationError


def test_valid_feed_configuration_creation():

    feed = FeedConfiguration(
        name="test_feed",
        url="https://example.com/feed.txt",
        parser_type="txt",
        enabled=True,
        update_interval=3600,
        tags=["malware", "phishing"]
    )

    assert feed.name == "test_feed"
    assert feed.parser_type == "txt"
    assert feed.enabled is True


def test_feed_name_cannot_be_empty():

    with pytest.raises(FeedConfigurationError):

        FeedConfiguration(
            name="",
            url="https://example.com/feed.txt",
            parser_type="txt"
        )


def test_feed_url_must_be_valid():

    with pytest.raises(FeedConfigurationError):

        FeedConfiguration(
            name="test_feed",
            url="invalid_url",
            parser_type="txt"
        )


def test_parser_type_must_be_supported():

    with pytest.raises(FeedConfigurationError):

        FeedConfiguration(
            name="test_feed",
            url="https://example.com/feed.xml",
            parser_type="xml"
        )


def test_update_interval_must_be_positive():

    with pytest.raises(FeedConfigurationError):

        FeedConfiguration(
            name="test_feed",
            url="https://example.com/feed.txt",
            parser_type="txt",
            update_interval=0
        )


def test_tags_must_be_list():

    with pytest.raises(FeedConfigurationError):

        FeedConfiguration(
            name="test_feed",
            url="https://example.com/feed.txt",
            parser_type="txt",
            tags="malware"
        )
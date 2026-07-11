import pytest

from src.feeds.models import FeedConfiguration
from src.feeds.registry import FeedRegistry
from src.feeds.exceptions import FeedRegistryError


@pytest.fixture
def sample_feed():

    return FeedConfiguration(
        name="test_feed",
        url="https://example.com/feed.txt",
        parser_type="txt",
        enabled=True,
        update_interval=3600,
        tags=["malware"]
    )


def test_add_feed(sample_feed):

    registry = FeedRegistry()

    registry.add(sample_feed)

    assert registry.count() == 1


def test_duplicate_feed_not_allowed(sample_feed):

    registry = FeedRegistry()

    registry.add(sample_feed)

    with pytest.raises(FeedRegistryError):
        registry.add(sample_feed)


def test_get_feed(sample_feed):

    registry = FeedRegistry()

    registry.add(sample_feed)

    feed = registry.get("test_feed")

    assert feed.name == "test_feed"


def test_remove_feed(sample_feed):

    registry = FeedRegistry()

    registry.add(sample_feed)

    registry.remove("test_feed")

    assert registry.count() == 0


def test_get_enabled_feeds():

    registry = FeedRegistry()

    enabled_feed = FeedConfiguration(
        name="enabled_feed",
        url="https://example.com/enabled.txt",
        parser_type="txt",
        enabled=True
    )

    disabled_feed = FeedConfiguration(
        name="disabled_feed",
        url="https://example.com/disabled.txt",
        parser_type="txt",
        enabled=False
    )

    registry.add(enabled_feed)
    registry.add(disabled_feed)

    feeds = registry.get_enabled_feeds()

    assert len(feeds) == 1
    assert feeds[0].name == "enabled_feed"
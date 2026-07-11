from pathlib import Path
from unittest.mock import MagicMock

from src.feeds.models import FeedConfiguration
from src.feeds.registry import FeedRegistry
from src.feeds.scheduler import FeedScheduler

def create_feed(
    name: str = "test_feed",
    enabled: bool = True,
) -> FeedConfiguration:
    return FeedConfiguration(
        name=name,
        url="https://example.com/feed.json",
        parser_type="json",
        enabled=enabled,
    )


def create_scheduler():
    registry = FeedRegistry()

    downloader = MagicMock()
    pipeline = MagicMock()

    scheduler = FeedScheduler(
        registry,
        downloader,
        pipeline,
    )

    return (
        scheduler,
        registry,
        downloader,
        pipeline,
    )


def test_scheduler_runs_enabled_feed():
    scheduler, registry, downloader, pipeline = create_scheduler()

    registry.add(create_feed())

    downloader.download_json_feed.return_value = True
    pipeline.process_file.return_value = [
        "ioc1",
        "ioc2",
    ]

    results = scheduler.run()

    assert len(results) == 1
    assert results[0].success is True
    assert results[0].feed_name == "test_feed"
    assert results[0].ioc_count == 2

    downloader.download_json_feed.assert_called_once()
    pipeline.process_file.assert_called_once()


def test_scheduler_skips_disabled_feed():
    scheduler, registry, downloader, pipeline = create_scheduler()

    registry.add(
        create_feed(
            enabled=False
        )
    )

    results = scheduler.run()

    assert results == []

    downloader.download_json_feed.assert_not_called()
    pipeline.process_file.assert_not_called()


def test_scheduler_handles_download_failure():
    scheduler, registry, downloader, pipeline = create_scheduler()

    registry.add(create_feed())

    downloader.download_json_feed.return_value = False

    results = scheduler.run()

    assert len(results) == 1
    assert results[0].success is False
    assert results[0].ioc_count == 0
    assert "download" in results[0].error.lower()

    pipeline.process_file.assert_not_called()


def test_scheduler_isolates_feed_failures():
    scheduler, registry, downloader, pipeline = create_scheduler()

    registry.add(create_feed("feed_one"))
    registry.add(create_feed("feed_two"))

    downloader.download_json_feed.side_effect = [
        False,
        True,
    ]

    pipeline.process_file.return_value = [
        "ioc1"
    ]

    results = scheduler.run()

    assert len(results) == 2

    assert results[0].success is False
    assert results[1].success is True
    assert results[1].ioc_count == 1